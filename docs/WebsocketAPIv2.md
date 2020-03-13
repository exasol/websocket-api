## WebSocket protocol v2 details

WebSocket Protocol v2 requires an Exasol version of at least 7.0.0. It follows the RFC 6455 document of the IETF.

The Exasol connection server identifies the initial GET request by the client.
This request contains information about the used protocol version.
Depending on this information the matching login and protocol class is
chosen.

After the handshake the process is identical to a connection using the
standard drivers like JDBC or ODBC: The connection server listens to
incoming messages and forwards the requests to the database. 

## Table of contents
* [Changes](#changes)
* [Command summary](#command-summary)
* [Attributes: Session and database properties](#attributes-session-and-database-properties)
* [Data Types: Type names and properties](#data-types-type-names-and-properties)
* [Compression](#compression)
* [Heartbeat/Feedback messages](#heartbeatfeedback-messages)
* [Subconnections](#subconnections)

## Changes

| Date | Exasol Version | Change | Issue |
| --- | --- | --- | --- |
| - | 7.0.0 | Metadata commands were added. See [Metadata-related commands](#metadata-related-commands) for details. | [EXASOL-2640](https://www.exasol.com/support/browse/EXASOL-2640) |
| 2020.10.03 | 7.0.0 | Columns of type `HASHTYPE` can be specified using the `HASHTYPE` type. See [Data Types](#data-types-type-names-and-properties) for details. | [EXASOL-2643](https://www.exasol.com/support/browse/EXASOL-2643) |

## Command summary

### Connection-related commands

The following commands are used to connect to Exasol, disconnect from Exasol, 
and query the hosts of an Exasol cluster.

| Command | Description |
| --- | --- |
| [disconnect](commands/disconnectV1.md) | Closes a connection to Exasol |
| [enterParallel](commands/enterParallelV1.md) | Opens subconnections for parallel execution |
| [getHosts](commands/getHostsV1.md) | Gets the hosts in a cluster |
| [login](commands/loginV1.md) | Establishes a connection to Exasol |
| [subLogin](commands/subLoginV1.md) | Establishes a subconnection to Exasol |

### Session-related commands

The following commands are used for actions that a user would typically perform after an Exasol 
session has been established. These commands are responsible for executing queries and statements, 
reading result sets, and getting and setting session attributes.

| Command | Description |
| --- | --- |
| [abortQuery](commands/abortQueryV1.md) | Aborts a running query |
| [closePreparedStatement](commands/closePreparedStatementV1.md) | Closes a prepared statement |
| [closeResultSet](commands/closeResultSetV1.md) | Closes a result set |
| [createPreparedStatement](commands/createPreparedStatementV1.md) | Creates a prepared statement |
| [execute](commands/executeV1.md) | Executes an SQL statement |
| [executeBatch](commands/executeBatchV1.md) | Executes multiple SQL statements as a batch |
| [executePreparedStatement](commands/executePreparedStatementV1.md) | Executes a prepared statement |
| [fetch](commands/fetchV1.md) | Retrieves data from a result set |
| [getAttributes](commands/getAttributesV1.md) | Gets the session attribute values |
| [getOffset](commands/getOffsetV1.md) | Gets the row offset of a result set |
| [getResultSetHeader](commands/getResultSetHeaderV1.md) | Gets a result set header |
| [setAttributes](commands/setAttributesV1.md) | Sets the given session attribute values |

### Metadata-related commands

The following commands are used to query metadata in Exasol. The commands and their behavior are very similar to methods in the JDBC standard.

| Command | Description |
| --- | --- |
| [getCatalogs](#getcatalogs-gets-the-catalog-names) | Gets the catalog names |
| [getColumnPrivileges](#getcolumnprivileges-gets-column-privilege-descriptions) | Gets column privilege descriptions |
| [getColumns](#getcolumns-gets-column-descriptions) | Gets column descriptions |
| [getPrimaryKeys](#getprimarykeys-gets-primary-key-descriptions) | Gets primary key descriptions |
| [getProcedureColumns](#getprocedurecolumns-gets-procedure-column-descriptions) | Gets procedure column descriptions |
| [getProcedures](#getprocedures-gets-procedure-descriptions) | Gets procedure descriptions |
| [getSchemas](#getschemas-gets-the-schema-names) | Gets the schema names |
| [getTablePrivileges](#gettableprivileges-gets-table-privilege-descriptions) | Gets table privilege descriptions |
| [getTables](#gettables-gets-table-descriptions) | Gets table descriptions |
| [getTableTypes](#gettabletypes-gets-the-supported-table-types) | Gets the supported table types |
| [getTypeInfo](#gettypeinfo-gets-the-supported-data-types) | Gets the supported data types |

## Attributes: Session and database properties

Attributes can be queried with the GetAttributes command and some of
them can be modified with the SetAttributes command. Modified
attributes are included in command replies.

| Name | JSON value | Read-only | Committable | Description |
| --- | --- | --- | --- | --- |
| autocommit | true \| false | no | no | If true, commit() will be executed automatically after each statement. If false, commit() and rollback() must be executed manually. |
| compressionEnabled | true \| false | yes | no | If true, the WebSocket data frame payload data is compressed. If false, it is not compressed. |
| currentSchema | string | no |  yes | Current schema name |
| dateFormat | string | yes | yes | Date format |
| dateLanguage | string | yes | yes | Language used for the day and month of dates. |
| datetimeFormat | string | yes | yes | Timestamp format |
| defaultLikeEscapeCharacter | string | yes | yes | Escape character in LIKE expressions. |
| feedbackInterval | number | no | no | Time interval (in seconds) specifying how often heartbeat/feedback packets are sent to the client during query execution. |
| numericCharacters | string | no | yes | Characters specifying the group and decimal separators (NLS_NUMERIC_CHARACTERS). For example, ",." would result in "123,456,789.123". |
| openTransaction | true \| false | yes | no | If true, a transaction is open. If false, a transaction is not open. 
| queryTimeout | number | no | yes | Query timeout value (in seconds). If a query runs longer than the specified time, it will be aborted. |
| snapshotTransactionsEnabled | true \| false | no | no | If true, snapshot transactions will be used. If false, they will not be used. |
| timestampUtcEnabled | true \| false | no | no | If true, timestamps will be converted to UTC. If false, UTC will not be used. |
| timezone | string | yes | yes | Timezone of the session. |
| timeZoneBehavior | string | yes | yes | Specifies the conversion behavior of UTC timestamps to local timestamps when the time value occurs during a time shift because of daylight saving time (TIME_ZONE_BEHAVIOR). |

Attributes are specified as an object of name/value pairs. Multiple attributes are separated by a comma.

Attribute JSON format
```javascript
 {
     // name: value
     <string>: <string | number | true | false>
 }
```

## Data Types: Type names and properties

The following data types and properties can be used to specify column
types in the executePreparedStatement request.

| Type | Required Properties | Optional Properties |
| --- | --- | --- |
| BOOLEAN | | |
| CHAR | size | |
| DATE | | |
| DECIMAL | precision, scale | |
| DOUBLE | | |
| GEOMETRY | | |
| HASHTYPE | | |
| INTERVAL DAY TO SECOND | precision, fraction | |
| INTERVAL YEAR TO MONTH | precision | |
| TIMESTAMP | | withLocalTimeZone |
| TIMESTAMP WITH LOCAL TIME ZONE | | withLocalTimeZone |
| VARCHAR | size | |


The following data types and properties are used to specify column
types in responses from Exasol.

| Type | Properties |
| --- | --- |
| BOOLEAN | |
| CHAR | size, characterSet |
| DATE | size |
| DECIMAL | precision, scale |
| DOUBLE | |
| GEOMETRY | size, srid |
| HASHTYPE | size |
| INTERVAL DAY TO SECOND | size, precision, fraction |
| INTERVAL YEAR TO MONTH | size, precision |
| TIMESTAMP | size, withLocalTimeZone |
| TIMESTAMP WITH LOCAL TIME ZONE | size, withLocalTimeZone |
| VARCHAR | size, characterSet |

## Compression

The data in the WebSocket data frames may be compressed using zlib. In
order to enable compression, the client must set the useCompression
field in the login command to true. If compression is enabled during
login, all messages sent and received after login completion must be
binary data frames, in which the payload data (i.e., command
request/response) is zlib-compressed.

## Heartbeat/Feedback messages

The feedbackInterval session attribute specifies how often (in seconds)
unidirectional heartbeat/feedback messages are sent to the client
during query execution. These messages are sent using Pong WebSocket
control frames (see RFC 6455), and thus a response is not expected.

The client may send Ping WebSocket control frames (see RFC 6455) to
Exasol, for example, as client-initiated keepalives. Exasol
will respond to a Ping frame with a Pong response.

Exasol will not send Ping frames to the client.

## Subconnections

### Introduction

Subconnections are additional connections to Exasol cluster nodes which can be created by the client. The main reason to create and use subconnections, as opposed to simply using the existing main connection, is to parallelize fetching/inserting data from/into Exasol.

For example, fetching a result set from Exasol can be done easily using the main connection. In this scenario, the Exasol cluster nodes will automatically send their data to the node which is connected to the client. This node then sends the combined data as a single result set. Thus, the client does not need to be aware of any data sharing/communication among the Exasol cluster nodes.

However, for performance-critical scenarios, a significant performance gain can be acheived by using subconnections to fetch/insert data directly from/into multiple Exasol cluster nodes in parallel. Thus, instead of all the data going through the single main connection, the data can flow through multiple subconnections to different Exasol nodes in parallel.

Please note that subconnections are only useful for multi-node Exasol clusters. With a single-node Exasol instance, the subconnection would basically be a duplicate of the main connection.

### How to create and use subconnections

Subconnections are created using the enterParallel command. The number of requested subconnections can be specified by the user, and the number of subconnections actually opened is given in the enterParallel response. Please note that the maximum number of subconnections is equal to the number of nodes in the Exasol cluster. For example, if the user has an eight-node cluster and requests 1,000 subconnections, only eight subconnections will be opened. As a general rule, the number of subconnections should usually be equal to the number of nodes in the Exasol cluster, which ensures one subconnection per node. After the subconnections have been created, the subLogin command should be used to login to each subconnection. Note: Failing to login to all subconnections will cause the login to hang. After this, they are ready for use.

:warning: Any command can be executed on subconnections; however, there is a significant difference in *how* they can be executed. The only two commands which can be executed ansynchronously on subconnections (i.e., not executed on all subconnections at the same time) are fetch and executePrepared. All other commands are synchronous, meaning the same command must be executed on all subconnections at the same time. For example, if the execute command is not called on all subconnections, the call will hang and eventually fail because of a time out.

After a subconnection is no longer needed, the disconnect command should be called and the WebSocket for it closed as normal. Please note that subconnections can be reused for multiple statements.

### Example

The following is an example of how to create, use, and close subconnections to fetch a result set from an executed prepared statement. If subconnections have already been created or are needed afterwards, the enterParallel, subLogin, and disconnect commands may be ignored.

1. On main connection:
   * Create subconnections (enterParallel)

2. On subconnections:
   * Login to subconnection (subLogin)

3. On main connection:
   * Execute prepared statement (executePreparedStatement)

4. On subconnections:
   * Get result set offset (getOffset)
   * Fetch result set data using the offset (fetch)
   * Close result set (closeResultSet)
   * Disconnect (disconnect)

5. On main connection:
   * Close result set (closeResultSet)
