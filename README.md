# EXASOL native drivers

This repository is used to develop, maintain and publish native open
source EXASOL drivers.

## Python DB API v2.0 compatible driver

In directory `python`, you'll find an implementation of PEP 249
(https://www.python.org/dev/peps/pep-0249/) "Python Database API
Specification v2.0" for developed for EXASOL.

This driver uses the Websocket API based communication protocol to
EXASOL with JSON as serialization format. It is usable as a drop-in 
replacement for PyODBC and similar ODBC based packages and does
not require and driver manager.

## Javascript

TBD
