# -*- coding: utf-8 -*-

import sys, datetime, platform, getpass, base64, time, zlib
from websocket import create_connection
from pprint import pprint as pp
from json import loads, dumps

paramstyle = 'qmark'
thredsafety = 1
apilevel = '2.0'

CLIENT_NAME = 'Python EXASOL DBI'
CLIENT_VERSION = '0.1'
DRIVER_NAME = 'Python DBI 2.0'
DEBUG_OUTPUT = False
CRYPTO_LIB = 'rsa'

if CRYPTO_LIB == 'rsa':
    import rsa
elif CRYPTO_LIB == 'Crypto':
    from Crypto.Cipher import PKCS1_v1_5
    from Crypto.PublicKey import RSA
else: raise RuntimeError('Crypto library %s is not supported' % repr(CRYPTO_LIB))

class Error(Exception): pass
class Warning(Exception): pass
class InterfaceError(Error): pass
class DatabaseError(Error): pass
class InternalError(DatabaseError): pass
class OperationalError(DatabaseError): pass
class ProgrammingError(DatabaseError): pass
class IntegrityError(DatabaseError): pass
class DataError(DatabaseError): pass
class NotSupportedError(DatabaseError): pass

Date = datetime.date
Time = datetime.time
Timestamp = datetime.datetime
Binary = None

class attributes:
    def __init__(self, attrs):
        for k, v in attrs.items():
            self.__dict__[k] = v
    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, repr(self.__dict__))
    def __getitem__(self, key):
        return self.__dict__[key]

class timerpause:
    def __init__(self, timer):
        self.timer = timer
    def __enter__(self):
        self.timer.pause()
    def __exit__(self, type, value, traceback):
        self.timer.resume()

class timer:
    def __init__(self, ws, name):
        self._ws = ws
        self._name = name
    def __enter__(self):
        self._t, self._c = time.time(), time.clock()
        self._pti, self._pci = 0, 0
        return self
    def __exit__(self, type, value, traceback):
        t, c = time.time(), time.clock()
        x, y = self._ws._timers.get(self._name, (0, 0))
        self._ws._timers[self._name] = (x + (t - self._t - self._pti), y + (c - self._c - self._pci))
    def pausing(self):
        return timerpause(self)
    def pause(self):
        self._pt, self._pc = time.time(), time.clock()
    def resume(self):
        pt, pc = time.time(), time.clock()
        self._pti += pt - self._pt
        self._pci += pc - self._pc

class cursor(object):
    description = None
    rowcount = None
    arraysize = 1
    connection = None
    #fetchbytes = 33554432 # 32 MiB
    #fetchbytes = 16777216 # 16 MiB
    #fetchbytes = 2*1024*1024
    #fetchbytes = 1*1024*1024
    #fetchbytes = 512*1024
    fetchbytes = 128*1024
    #fetchbytes = 64*1024
    #fetchbytes = 1024*2
    columnar_mode = False # in columnar mode executemany expects list of columns as parameters
                          # and fetchmany returns list of columns instead list of rows
    optimal_arraysize = None

    def callproc(self, procname, *parameters):
        raise NotSupportedError()

    def close(self):
        if self.__dict__.get('_result') is not None:
            if self._result.get('resultSetHandle', -3) >= 0:
                self.connection._req(command = 'closeResultSet',
                                     resultSetHandles = [self._result['resultSetHandle']])
            self._result = None
            self._fetch_reset()

    def execute(self, operation, *parameters):
        if parameters is None or len(parameters) == 0:
            return self._execute_simple(operation)
        if self.columnar_mode:
            seq_of_parameters = [(x,) for x in parameters]
        else: seq_of_parameters = [parameters]
        return self.executemany(operation, seq_of_parameters)

    def executemany(self, operation, seq_of_parameters):
        rep = self.connection._req(command = 'createPreparedStatement', sqlText = operation)
        try:
            if not self.columnar_mode:
                numrows = len(seq_of_parameters)
                seq_of_parameters = list(zip(*seq_of_parameters))
            else: numrows = len(seq_of_parameters[0])
            exp = self.connection._req(command = 'executePreparedStatement',
                                       statementHandle = rep['statementHandle'],
                                       numColumns = rep['parameterData']['numColumns'],
                                       numRows = numrows,
                                       columns = rep['parameterData']['columns'],
                                       data = seq_of_parameters)
            return self._execute_simple(None, rep = exp)
        finally:
            self.connection._req(command = 'closePreparedStatement',
                                 statementHandle = rep['statementHandle'])

    def fetchone(self):
        ret = self.fetchmany(size = 1)
        if ret is None: return None
        if self.columnar_mode:
            ret = list(zip(*ret))
        return ret[0]

    def fetchmany(self, size = None):
        if size is None or size == 'optimal':
            rsize = self.arraysize
        else: rsize = size
        with timer(self.connection, 'fdat') as tr:
            if self._resdata is None:
                with tr.pausing():
                    self._fetch()
            if size == 'optimal':
                rest = self._resdata['numRows']
            else: rest = rsize
            data = self._resdata['data']; ret = None
            while True:
                if rest == 0 or self._realpos >= self.rowcount:
                    break
                if self._currow >= self._resdata['numRows']:
                    with tr.pausing():
                        self._fetch()
                    data = self._resdata['data']
                restfetch = min(self._resdata['numRows'] - self._currow, rest)
                if self._currow == 0 and restfetch == self._resdata['numRows']:
                    if ret is None:
                        ret = data
                    else:
                        for col in range(len(data)):
                            ret[col].extend(data[col])
                else:
                    if ret is None:
                        ret = [[] for col in range(len(data))]
                    for col in range(len(data)):
                        ret[col].extend(data[col][self._currow:self._currow+restfetch])
                rest -= restfetch
                self._currow += restfetch
                self._realpos += restfetch
            if ret is None: return None
            if not self.columnar_mode:
                ret = list(zip(*ret))
        return ret

    def fetchall(self):
        return self.fetchmany(size = self.rowcount)

    def nextset(self):
        raise NotSupportedError("multiple resultsets not supported")

    def next(self):
        return self.__next__()
    
    def __next__(self):
        row = self.fetchone()
        if row is None:
            raise StopIteration
        return row

    def __iter__(self):
        return self

    def __len__(self):
        if self.rowcount is None:
            return 0
        return self.rowcount

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def setinputsizes(self, sizes): pass
    def setoutputsize(self, size, column): pass

    def _execute_simple(self, operation, rep = None):
        if rep is None:
            rep = self.connection._req(command = 'execute', sqlText = operation)
        if rep['resultType'] == 'rowCount':
            self._fetch_reset()
            self.rowcount = rep['numRows']
            return self.rowcount
        if rep['resultType'] == 'resultSet':
            if rep.get('numResults', 0) > 1:
                raise NotSupportedError('only single result querys supported, got %d resuts' % rep.get('numResuts', 0))
            self._result = rep['resultSets'][0]
            self.rowcount = self._result['numRows']
            self.description = []
            for col in self._result['columns']:
                self.description.append((col['name'],
                                         col['dataType']['type'],
                                         col['dataType'].get('size', None),
                                         col['dataType'].get('size', None),
                                         col['dataType'].get('precision', None),
                                         col['dataType'].get('scale', None),
                                         True))
            self._fetch_reset()
            return self.rowcount
        raise NotSupportedError('result type %s not supported' % repr(rep['resultType']))

    def _fetch(self):
        if self.__dict__.get('_result') is None:
            raise InterfaceError('result set is closed')
        elif self._result.get('resultSetHandle', -3) == -3:
            self._resdata = self._result
        else: self._resdata = self.connection._req(command = 'fetch',
                                                   resultSetHandle = self._result['resultSetHandle'],
                                                   startPosition = self._respos,
                                                   numBytes = self.fetchbytes)
        self._respos += self._resdata['numRows']
        self._currow = 0

    def _fetch_reset(self):
        self._respos = self._currow = self._realpos = 0
        self._resdata = None

class connect(object):
    def __init__(self, url, username, password, autocommit = False, queryTimeout = 60):
        self._timers = {}
        self._connect(url)
        self._login(username, password, autocommit, queryTimeout)
        self._attributes = None

    def close(self):
        self._req(command = 'disconnect')
        self.__ws = None

    def commit(self):
        with self.cursor() as c:
            c.execute('COMMIT');

    def rollback(self):
        with self.cursor() as c:
            c.execute('ROLLBACK');

    def cursor(self):
        c = cursor()
        c.connection = self
        c._fetch_reset()
        return c

    def execute(self, operation, *parameters):
        c = self.cursor()
        c.execute(operation, *parameters)
        return c

    def executemany(self, operation, seq_of_parameters):
        c = self.cursor()
        c.executemany(operation, seq_of_parameters)
        return c

    def attributes(self, attrs = None):
        if attrs is not None or self._attributes is None:
            if attrs is None:
                attrs = {}
            else: attrs = attrs.__dict__
            self._req(command = 'setAttributes', attributes = attrs)
            self._attributes = attributes(self._req(command = 'getAttributes'))
        return self._attributes

    def timers(self):
        return self._timers

    def timersreset(self):
        self._timers = {}

    def _req(self, **req):
        try:
            with timer(self, 'dump'): send_data = dumps(req, separators=(',',':'))
            with timer(self, 'send'): self.__ws.send(send_data)
            with timer(self, 'recv'): recv_data = self.__ws.recv()
            with timer(self, 'load'): rep = loads(recv_data)
        except Exception as err:
            rep = {'status': 'unknown', 'exceptionText': repr(err)}
        if DEBUG_OUTPUT:
            pp((req, rep))
        if rep['status'] == 'ok':
            if 'exception' in rep:
                raise DatabaseError('[%s] %s' % (rep['exception']['sqlCode'], rep['exception']['text']))
            return rep.get('responseData', rep.get('attributes', None))
        if rep['status'] == 'error':
            raise OperationalError('%s [%s] %s' % ('database error',
                                                   rep['exception']['sqlCode'],
                                                   rep['exception']['text']))
        raise OperationalError('internal error: %s' % repr(rep))

    def _connect(self, url):
        with timer(self, 'conn'):
            self.__ws = create_connection(url)
            ret = self._req(command = 'login', protocolVersion = 14)
            if CRYPTO_LIB == 'rsa':
                if sys.version_info.major >= 3:
                    pk = rsa.PublicKey.load_pkcs1(bytes(ret['publicKeyPem'], 'utf-8'))
                    self._encrypt = lambda t: base64.b64encode(rsa.encrypt(t.encode('utf-8'), pk)).decode('utf-8')
                else:
                    pk = rsa.PublicKey.load_pkcs1(ret['publicKey'])
                    self._encrypt = lambda t: base64.b64encode(rsa.encrypt(t.encode('utf-8'), pk))
            elif CRYPTO_LIB == 'Crypto':
                pk = PKCS1_v1_5.new(RSA.importKey(ret['publicKey']))
                self._encrypt = lambda t: pk.encrypt(t.encode('utf-8'))
            else: raise RuntimeError('Crypto library %s not supported' % repr(CRYPTO_LIB))

    def _login(self, username, password, autocommit, queryTimeout):
        with timer(self, 'auth'):
            ret = self._req(username = username,
                            password = self._encrypt(password),
                            clientName = CLIENT_NAME,
                            driverName = DRIVER_NAME,
                            clientOs = '%s %s %s' % (platform.system(), platform.release(), platform.version()),
                            clienOsUsername = getpass.getuser(),
                            clientVersion = CLIENT_VERSION,
                            clientRuntime = 'Python %s' % platform.python_version(),
                            attributes = {'autocommit': autocommit,
                                          'queryTimeout': queryTimeout})
        self._connection = ret

__all__ = ('Error', 'Warning', 'InterfaceError', 'DatabaseError', 'InternalError', 'OperationalError',
           'ProgrammingError', 'IntegrityError', 'DataError', 'NotSupportedError', 'Date', 'Time',
           'Timestamp', 'Binary', 'connect', 'timer', 'paramstyle', 'thredsafety', 'apilevel')
