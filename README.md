# Exasol JSON over WebSockets API

###### Please note that this is an open source project which is officially supported by Exasol. For any question, you can contact our support team.

## Why a WebSockets API?

The JSON over WebSockets client-server protocol allows customers to 
implement their own drivers for all kinds of platforms using a 
connection-based web protocol. 

The main advantages are flexibility regarding the programming languages 
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

## Supported versions
| | WebSocket API v1 | WebSocket API v2 |
| --- | --- | --- |
| **Exasol 7.0** | :heavy_check_mark: | :heavy_check_mark: |
| **Exasol 6.2** | :heavy_check_mark: | :x: |
| **Exasol 6.1** | :heavy_check_mark: | :x: |
| **Exasol 6.0** | :heavy_check_mark: | :x: |

## Content
* [API specification of the protocol](WebsocketAPI.md)
* Several native Exasol driver implementations using the JSON over WebSockets API protocol
