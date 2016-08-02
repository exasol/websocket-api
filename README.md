# EXASOL DB 6 - Native Drivers

## Python DB API v2.0 Compatible Driver

In directory `python` is a implementation of PEP 249
(https://www.python.org/dev/peps/pep-0249/) - Python Database API
Specification v2.0 for the EXASOL DB 6.

This drivers uses the Websocket API based communication protocol to
the EXASOL DB with JSON as serialization format.

### Installation

To install it with `pip` enter following command:
```shell
$> pip install 'git+http://github.com/EXASOL/websocket-api.git#egg=exasol-ws-api&subdirectory=python'
```

### Usage

Small example, which shows how to create a connection and execute some query:
```python
import EXASOL

with EXASOL.connect('ws://10.10.1.1:8563') as connection:
     with connection.cursor() as cursor:
          cursor.execute('SELECT * FROM someschema.sometable')
          for row in cursor:
              print row
```


Please reffer Python DB API v2.0 documentation for details:
https://www.python.org/dev/peps/pep-0249/

## Javascript

TBD