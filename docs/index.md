# Exasol WebSockets API

**:information_source: Info**

Please note that this is an open source project which is officially supported by Exasol. For any question, you can contact our support team.

## Why a WebSockets API?

The JSON over WebSockets client-server protocol allows customers to 
implement their own drivers for all kinds of platforms using a 
connection-based web protocol. 

The main advantages are performance improvements from lock-free metadata calls, flexibility regarding the programming languages 
you want to integrate Exasol into, and a more native access compared to 
the standardized ways of communicating with a database, such as JDBC, 
ODBC or ADO.NET, which are mostly old and static standards and create
additional complexity due to the necessary driver managers.

## Client support

Currently a native Python driver using this WebSocket API has been
implemented. By that you don't need any pyodbc bridge anymore, but 
can connect your Python directly with Exasol. PyODBC is not ideal due
to the need for an ODBC driver manager and certain restrictions in 
data type conversions.

Further languages will be added in the future, and we encourage you
to provide us feedback what languages you are interested in, and 
maybe you are even keen to support our community with own developments. 
It would then be nice if you could share your work with us, and 
we will of course help you by any means. 

## Changes
* Autocommit was enabled by default for sessions in Exasol 7.1+.
* [WebSocket API v3](WebsocketAPIV3.md) support has been added in Exasol 7.1.
* [WebSocket API v2](WebsocketAPIV2.md) support has been added in Exasol 7.0.

## Supported versions
| | WebSocket API v1   | WebSocket API v2   | WebSocket API v3   |
| --- |:------------------:|:------------------:|:------------------:|
| **Exasol 7.1** | :white_check_mark: | :white_check_mark: | :white_check_mark: |
| **Exasol 7.0** | :white_check_mark: | :white_check_mark: | :x:                |
| **Exasol 6.2** | :white_check_mark: | :x:                | :x:                |

## Protocol Specifications
* [WebSocket protocol v3 API specification](WebsocketAPIV3.md)
* [WebSocket protocol v2 API specification](WebsocketAPIV2.md)
* [WebSocket protocol v1 API specification](WebsocketAPIV1.md)

## Officially Supported Implementations

## Python
* [exasol-websocket-api](https://github.com/exasol/websocket-api/tree/master/python)
* [Pyexasol](https://github.com/exasol/pyexasol)

## Javascript
* [exasol-websocket-api](https://github.com/exasol/websocket-api/tree/master/javascript)

## Go
* [Go native driver implementation](https://github.com/exasol/exasol-driver-go)
