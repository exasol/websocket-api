# Exasol JSON over WebSockets API

###### This repository is dedicated solely to protocol documentation and does not provide any WebSocket drivers or driver support. However, it includes some implementation examples and a list of officially supported drivers at the bottom of the page. This content will be integrated into the official Exasol documentation.

## Why a WebSockets API?

The JSON over WebSockets client-server protocol allows customers to 
implement their own drivers for all kinds of platforms using a 
connection-based web protocol. 

The main advantages are performance improvements from lock-free metadata calls, flexibility regarding the programming languages 
you want to integrate Exasol into, and a more native access compared to 
the standardized ways of communicating with a database, such as JDBC, 
ODBC or ADO.NET, which are mostly old and static standards and create
additional complexity due to the necessary driver managers.

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

## Example Driver Implementations
* [Python native driver implementation](python/)
* [JavaScript native driver implementation](javascript/)

