# Exasol JSON over WebSockets API

###### Please note that this is an open source project which is officially supported by Exasol. For any question, you can contact our support team.

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
* [WebSocket API v3](docs/WebsocketAPIV3.md) support has been added in Exasol 7.1.
* [WebSocket API v2](docs/WebsocketAPIV2.md) support has been added in Exasol 7.0.

## Supported versions
| | WebSocket API v1 | WebSocket API v2 | WebSocket API v3 |
| --- | --- | --- | --- |
| **Exasol 7.1** | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| **Exasol 7.0** | :heavy_check_mark: | :heavy_check_mark: | :x: |
| **Exasol 6.2** | :heavy_check_mark: | :x: | :x: |

## Protocol Specifications
* [WebSocket protocol v3 API specification](docs/WebsocketAPIV3.md)
* [WebSocket protocol v2 API specification](docs/WebsocketAPIV2.md)
* [WebSocket protocol v1 API specification](docs/WebsocketAPIV1.md)

## Provided Implementations
* [Python native driver implementation](python/)
* [JavaScript native driver implementation](javascript/)
* [Go native driver implementation](https://github.com/exasol/exasol-driver-go)
