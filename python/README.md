# Introduction

This is an implementation of PEP 249 (https://www.python.org/dev/peps/pep-0249/)
"Python Database API Specification v2.0" for EXASOL.

This driver uses the EXASOL Websocket API protocol with JSON 
as serialization format. It is usable as a drop-in replacement 
for PyODBC and similar ODBC based packages and does not require 
any driver manager.


# Installation

To install this driver with `pip` enter following command:
```shell
$> pip install 'git+http://github.com/EXASOL/websocket-api.git#egg=exasol-ws-api&subdirectory=python'
```

# Usage

Small example, which shows how to create a connection and execute some query:
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

