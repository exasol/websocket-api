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

At present, an example implementation of a native Python driver utilizing this WebSocket API is available. This serves merely as a starting point, illustrating how you can directly connect Python with Exasol without the necessity for a pyodbc bridge. The use of PyODBC is less than optimal, given its dependency on an ODBC driver manager and limitations regarding data type conversions. It's important to note that these implementations are provided as examples to inspire the development of your own drivers. For a list of officially supported WebSocket drivers, please refer to the bottom of this page.

## Changes
* Autocommit was enabled by default for sessions in Exasol 7.1+.
* [WebSocket API v3](docs/WebsocketAPIV3.md) support has been added in Exasol 7.1.
* [WebSocket API v2](docs/WebsocketAPIV2.md) support has been added in Exasol 7.0.

## Supported versions
| | WebSocket API v1 | WebSocket API v2 | WebSocket API v3 |
| --- | --- | --- | --- |
| **Exasol V8** | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| **Exasol 7.1** | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| **Exasol 7.0** | :heavy_check_mark: | :heavy_check_mark: | :x: |
| **Exasol 6.2** | :heavy_check_mark: | :x: | :x: |

## Protocol Specifications
* [WebSocket protocol v3 API specification](docs/WebsocketAPIV3.md)
* [WebSocket protocol v2 API specification](docs/WebsocketAPIV2.md)
* [WebSocket protocol v1 API specification](docs/WebsocketAPIV1.md)

## Existing Official Supported WebSocket Drivers
* [Python native driver implementation](https://github.com/exasol/pyexasol)
* [Go native driver implementation](https://github.com/exasol/exasol-driver-go)

* ## Example Driver Implementations
* [Python native driver implementation](python/)
* [JavaScript native driver implementation](javascript/)

