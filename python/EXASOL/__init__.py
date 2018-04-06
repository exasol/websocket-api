# -*- coding: utf-8 -*-

import sys, datetime, platform, getpass, base64, time, zlib
from websocket import create_connection
from pprint import pprint as pp
from json import loads, dumps

paramstyle = 'qmark'
thredsafety = 1
apilevel = '2.0'

CLIENT_NAME = 'Python EXASOL DBI'
CLIENT_VERSION = '6.0.0'
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

def defaultTypeMapper(column, data):
    return data

class cursor(object):
    """Cursor for EXASOL DB result sets

    It can be used as iterator and in 'with' context for automatic
    close. Available variables:

    description: result set schema
    rowcount: number of rows in result set
    connection: connection to be used
    fetchbytes: maximal number of bytes to fetch at once, but at least 1 row

    """

    description = None
    rowcount = None
    arraysize = 1
    connection = None
    fetchbytes = 128*1024
    optimal_arraysize = None

    def callproc(self, procname, *parameters):
        raise NotSupportedError()

    def close(self):
        """Close cursor"""
        if self.__dict__.get('_result') is not None:
            if self._result.get('resultSetHandle', -3) >= 0:
                self.connection._req(command = 'closeResultSet',
                                     resultSetHandles = [self._result['resultSetHandle']])
            self._result = None
            self._fetch_reset()

    def execute(self, operation, *parameters):
        """Execute SQL command, possibly with parameters."""
        if parameters is None or len(parameters) == 0:
            return self._execute_simple(operation)
        if self.connection.columnar_mode:
            seq_of_parameters = [(x,) for x in parameters]
        else: seq_of_parameters = [parameters]
        return self.executemany(operation, seq_of_parameters)

    def executemany(self, operation, seq_of_parameters):
        """Execute multiple SQL commands with given parameters"""
        rep = self.connection._req(command = 'createPreparedStatement', sqlText = operation)
        try:
            if not self.connection.columnar_mode:
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
        """Fetch one row of result"""
        ret = self.fetchmany(size = 1)
        if ret is None: return None
        if self.connection.columnar_mode:
            ret = list(zip(*ret))
        return ret[0]

    def fetchmany(self, size = None):
        """Fetch many lines of result

        size is amount of rows to fetch, can be None or 'default' to use a default value.
        """
        if size is None or size == 'default':
            rsize = self.arraysize
        else: rsize = size
        with timer(self.connection, 'fdat') as tr:
            if self._resdata is None:
                with tr.pausing():
                    self._fetch()
            if size == 'optimal':
                rest = self._resdata['numRows']
            else: rest = rsize
            if rest == 0: data = []
            else: data = self._resdata['data']
            ret = None
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
            cols = self.description
            typm = self.connection._type_mapper
            for i in range(len(ret)):
                ret[i] = typm(cols[i], ret[i])
            if not self.connection.columnar_mode:
                ret = list(zip(*ret))
        return ret

    def fetchall(self):
        """Fetch all result set rows"""
        return self.fetchmany(size = self.rowcount)

    def nextset(self):
        """Fetch next resultset, not supported by EXASOL DB"""
        raise NotSupportedError("multiple resultsets not supported")

    def next(self):
        """Return next row"""
        return self.__next__()
    
    def __next__(self):
        """Return next row"""
        row = self.fetchone()
        if row is None:
            raise StopIteration
        return row

    def __iter__(self):
        """Returns current cursor as iterator"""
        return self

    def __len__(self):
        """Returns row count of current result set""" 
        if self.rowcount is None:
            return 0
        return self.rowcount

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def setinputsizes(self, sizes):
        """Set input sizes is not supported."""
        pass
    def setoutputsize(self, size, column):
        """Set output sizes is not supported."""
        pass

    def _execute_simple(self, operation, rep = None):
        if rep is None:
            rep = self.connection._req(command = 'execute', sqlText = operation)
        if len(rep.get('results', [])) != 1:
            raise NotSupportedError('only single result querys supported, got %d resuts' % rep.get('numResults', 0))
        res = rep['results'][0]
        if res['resultType'] == 'rowCount':
            self._fetch_reset()
            self.rowcount = res['rowCount']
            return self.rowcount
        if res['resultType'] == 'resultSet':
            self._result = res['resultSet']
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
    """Connection to EXASOL DB

    Python DB API 2.0 compatible connection to a EXASOL DB through the
    Websocket based API.

    Columnar mode can be enabled with .columnar_mode = True, then the
    cursors well be faster and the data will we structured in columns
    instead of rows. EXASOL DB is column oriented DB and this mode
    works better and faster, but is not compatible with Python DB API
    and is not expected by tools. Per default ist colmnar mode
    offline.

    """

    columnar_mode = False # in columnar mode executemany expects list of columns as parameters
                          # and fetchmany returns list of columns instead list of rows

    def __init__(self, url, username, password,
                 autocommit = False,
                 queryTimeout = 60,
                 useCompression = False,
                 typeMapper = defaultTypeMapper,
                 **options):
        """Create the connection

        Parameters:
        url: websocket url, example: ws://10.10.1.1:8563
        username, password: authentication information
        autocommit: enable or disable autocommit on connection
        queryTimeout: wait maximal givent time for an answer
        useCompression: enable or disable compressed communication
        options: custom websocket options (see https://github.com/websocket-client/websocket-client)
        """
        self._timers = {}
        self._url = url
        self._session_id = None
        self._username = username
        self._password = password
        self._autocommit = autocommit
        self._queryTimeout = queryTimeout
        self._attributes = None
        self._compression = useCompression
        self._inconnect = False
        self._type_mapper = typeMapper
        self._options = options
        self._connect()
        self._login()

    def close(self):
        """Close the connection"""
        self._req(command = 'disconnect')
        self.__ws = None

    def commit(self):
        """Send a COMMIT command"""
        with self.cursor() as c:
            c.execute('COMMIT');

    def rollback(self):
        """Send a ROLLBACK command"""
        with self.cursor() as c:
            c.execute('ROLLBACK');

    def cursor(self):
        """Create a cursor"""
        c = cursor()
        c.connection = self
        c._fetch_reset()
        return c

    def execute(self, operation, *parameters):
        """Execute given SQL command, possibly with parameters"""
        c = self.cursor()
        c.execute(operation, *parameters)
        return c

    def executemany(self, operation, seq_of_parameters):
        """Execute given SQL command multiple times with given parameters"""
        c = self.cursor()
        c.executemany(operation, seq_of_parameters)
        return c

    def attributes(self, attrs = None):
        """Get or set the session attributes"""
        if attrs is not None or self._attributes is None:
            if attrs is not None:
                # HACK, should be removed
                del attrs.__dict__['openTransaction']
                self._req(command = 'setAttributes', attributes = attrs.__dict__)
            self._attributes = attributes(self._req(command = 'getAttributes'))
        return self._attributes

    def timers(self):
        """Returns current performance timers"""
        return self._timers

    def timersreset(self):
        """Reset performance timers"""
        self._timers = {}

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def _req(self, **req):
        try:
            with timer(self, 'dump'): send_data = dumps(req, separators=(',',':'))
            #sys.stderr.write(">>> %s\n" % send_data)
            with timer(self, 'send'): self._ws_send(send_data)
            with timer(self, 'recv'): recv_data = self._ws_recv()
            #sys.stderr.write("<<< %s\n" % recv_data)
            with timer(self, 'load'): rep = loads(recv_data)
        except Exception as err:
            if not self._inconnect:
                self._connect()
                self._login()
            rep = {'status': 'unknown', 'exceptionText': repr(err)}
        if DEBUG_OUTPUT:
            pp((req, rep), stream = sys.stderr)
        if rep['status'] == 'ok':
            if 'exception' in rep:
                raise DatabaseError('[%s] %s' % (rep['exception']['sqlCode'], rep['exception']['text']))
            return rep.get('responseData', rep.get('attributes', None))
        if rep['status'] == 'error':
            raise OperationalError('%s [%s] %s' % ('database error',
                                                   rep['exception']['sqlCode'],
                                                   rep['exception']['text']))
        raise OperationalError('internal error: %s' % repr(rep))

    def _connect(self):
        with timer(self, 'conn'):
            try:
                self._inconnect = True
                self.__ws = create_connection(self._url, **self._options)
                self._ws_send = self.__ws.send
                self._ws_recv = self.__ws.recv
                ret = self._req(command = 'login', protocolVersion = 1)
                if CRYPTO_LIB == 'rsa':
                    if sys.version_info.major >= 3:
                        pk = rsa.PublicKey.load_pkcs1(bytes(ret['publicKeyPem'], 'utf-8'))
                        self._encrypt = lambda t: base64.b64encode(rsa.encrypt(t.encode('utf-8'), pk)).decode('utf-8')
                    else:
                        pk = rsa.PublicKey.load_pkcs1(ret['publicKeyPem'])
                        self._encrypt = lambda t: base64.b64encode(rsa.encrypt(t.encode('utf-8'), pk))
                elif CRYPTO_LIB == 'Crypto':
                    pk = PKCS1_v1_5.new(RSA.importKey(ret['publicKey']))
                    self._encrypt = lambda t: pk.encrypt(t.encode('utf-8'))
                else: raise RuntimeError('Crypto library %s not supported' % repr(CRYPTO_LIB))
            finally:
                self._inconnect = False

    def _login(self):
        with timer(self, 'auth'):
            args = {'username': self._username,
                    'password': self._encrypt(self._password),
                    'clientName': CLIENT_NAME,
                    'driverName': DRIVER_NAME,
                    'clientOs': '%s %s %s' % (platform.system(), platform.release(), platform.version()),
                    'useCompression': self._compression,
                    'clientOsUsername': getpass.getuser(),
                    'clientVersion': CLIENT_VERSION,
                    'clientRuntime': 'Python %s' % platform.python_version()}
            if self._session_id is not None:
                args['sessionId'] = self._session_id
            ret = self._req(**args)
            self._session_id = ret['sessionId']
            if self._compression:
                self._ws_send = lambda x: self.__ws.send_binary(zlib.compress(x.encode('utf-8')))
                self._ws_recv = lambda: zlib.decompress(self.__ws.recv())
            attr = self.attributes()
            attr.autocommit = self._autocommit
            attr.queryTimeout = self._queryTimeout
            self.attributes(attr)
        self._connection = ret

__all__ = ('Error', 'Warning', 'InterfaceError', 'DatabaseError', 'InternalError', 'OperationalError',
           'ProgrammingError', 'IntegrityError', 'DataError', 'NotSupportedError', 'Date', 'Time',
           'Timestamp', 'Binary', 'connect', 'timer', 'paramstyle', 'thredsafety', 'apilevel')
