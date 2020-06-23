# Introduction

This is an implementation of PEP 249 (https://www.python.org/dev/peps/pep-0249/)
"Python Database API Specification v2.0" for Exasol.

This driver uses the Exasol Websocket API protocol with JSON 
as serialization format. It is usable as a drop-in replacement 
for PyODBC and similar ODBC based packages and does not require 
any driver manager.


# Installation

To install this driver with `pip` enter following command:
```shell
$> pip install 'git+http://github.com/EXASOL/websocket-api.git#egg=exasol-ws-api&subdirectory=python'
```

# Usage

A small example, which shows how to create a connection and execute some query:
```python
import EXASOL

with EXASOL.connect('ws://10.10.1.1:8563', 'user', 'pwd') as connection:
     with connection.cursor() as cursor:
          cursor.execute('SELECT * FROM someschema.sometable')
          for row in cursor:
              print(row)
```
Please see also Python DB API v2.0 documentation for further details:
https://www.python.org/dev/peps/pep-0249/

### Secure connections

To create a secure WebSocket connection, simply specify `wss://` instead of `ws://` in the URL.
```python
with EXASOL.connect('wss://10.10.1.1:8563', 'user', 'pwd') as connection:
     with connection.cursor() as cursor:
          cursor.execute('SELECT * FROM someschema.sometable')
          for row in cursor:
              print(row)
```

### Specification of connection options

Optional connection details can be specified as keyword arguments in `EXASOL.connect()`. These are passed to the `websocket_client` module, which is used as a low-level WebSocket client.  For details on the possible connection options, please see https://github.com/websocket-client/websocket-client.

For example, to disable SSL certificate validation while creating a secure connection, `sslopt={"cert_reqs": ssl.CERT_NONE}` should be specified.
```python
import EXASOL
import ssl

with EXASOL.connect('wss://10.10.1.1:8563', 'user', 'pwd', sslopt={"cert_reqs": ssl.CERT_NONE}) as connection:
     with connection.cursor() as cursor:
          cursor.execute('SELECT * FROM someschema.sometable')
          for row in cursor:
              print(row)
```
