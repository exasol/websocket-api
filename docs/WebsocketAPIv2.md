## WebSocket protocol v2 details

WebSocket Protocol v2 requires an Exasol version of at least 7.0.0. It follows the RFC 6455 document of the IETF.

The Exasol connection server identifies the initial GET request by the client.
This request contains information about the used protocol version.
Depending on this information the matching login and protocol class is
chosen.

After the handshake the process is identical to a connection using the
standard drivers like JDBC or ODBC: The connection server listens to
incoming messages and forwards the requests to the database. 

## Changes

| Exasol Version | Change | Issue |
| --- | --- | --- |
| 7.0.0 | Metadata commands were added. See [Metadata-related commands](#metadata-related-commands) for details. | [EXASOL-2640](https://www.exasol.com/support/browse/EXASOL-2640) |
| 7.0.0 | Columns of type `HASHTYPE` can be specified using the `HASHTYPE` type. See [Data Types](#data-types-type-names-and-properties) for details. | [EXASOL-2643](https://www.exasol.com/support/browse/EXASOL-2643) |

## Command summary

### Connection-related commands

The following commands are used to connect to Exasol, disconnect from Exasol, 
and query the hosts of an Exasol cluster.

| Command | Description |
| --- | --- |
| [disconnect](#disconnect-closes-a-connection-to-exasol) | Closes a connection to Exasol |
| [enterParallel](#enterparallel-opens-subconnections-for-parallel-execution) | Opens subconnections for parallel execution |
| [getHosts](#gethosts-gets-the-hosts-in-a-cluster) | Gets the hosts in a cluster |
| [login](#login-establishes-a-connection-to-exasol) | Establishes a connection to Exasol |
| [subLogin](#sublogin-establishes-a-subconnection-to-exasol) | Establishes a subconnection to Exasol |

### Session-related commands

The following commands are used for actions that a user would typically perform after an Exasol 
session has been established. These commands are responsible for executing queries and statements, 
reading result sets, and getting and setting session attributes.

| Command | Description |
| --- | --- |
| [abortQuery](#abortquery-aborts-a-running-query) | Aborts a running query |
| [closePreparedStatement](#closepreparedstatement-closes-a-prepared-statement) | Closes a prepared statement |
| [closeResultSet](#closeresultset-closes-a-result-set) | Closes a result set |
| [createPreparedStatement](#createpreparedstatement-creates-a-prepared-statement) | Creates a prepared statement |
| [execute](#execute-executes-an-sql-statement) | Executes an SQL statement |
| [executeBatch](#executebatch-executes-multiple-sql-statements-as-a-batch) | Executes multiple SQL statements as a batch |
| [executePreparedStatement](#executepreparedstatement-executes-a-prepared-statement) | Executes a prepared statement |
| [fetch](#fetch-retrieves-data-from-a-result-set) | Retrieves data from a result set |
| [getAttributes](#getattributes-gets-the-session-attribute-values) | Gets the session attribute values |
| [getOffset](#getoffset-gets-the-row-offset-of-a-result-set) | Gets the row offset of a result set |
| [getResultSetHeader](#getresultsetheader-gets-a-result-set-header) | Gets a result set header |
| [setAttributes](#setattributes-sets-the-given-session-attribute-values) | Sets the given session attribute values |

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

## Heartbeat/Feedback Messages

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

## Command details

### AbortQuery: Aborts a running query

This command aborts a running query. It does not have a response.

Request fields:
  * command (string) => command name: "abortQuery"

Request JSON format
```javascript
 {
     "command": "abortQuery"
 }
```

### ClosePreparedStatement: Closes a prepared statement

This command closes a prepared statement which has already been
created.

Request fields:
  * command (string) => command name: "closePreparedStatement"
  * attributes (object, optional) => attributes to set for the connection (see below)
  * statementHandle (number) => prepared statement handle

Request JSON format
```javascript
 {
     "command": "closePreparedStatement",
     "attributes": {
             // as defined separately
     },
     "statementHandle": <number>
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * attributes (object) => attributes set for the connection (see below)
  * exception (object, optional) =>  only present if status is "error"
    * text (string) => exception message which provides error details
    * sqlCode (string) => five-character exception code if known, otherwise "00000"

Response JSON format
```javascript
 {
     "status": <"ok" | "error">,
     "attributes": {
             // as defined separately
     },
     // in case of "error"
     "exception": {
             "text": <string>,
             "sqlCode": <string>
     }
 }
```

### CloseResultSet: Closes a result set

This command closes result sets.

Request fields:
  * command (string) => command name: "closeResultSet"
  * attributes (object, optional) => attributes to set for the connection (see below)
  * resultSetHandles (number[]) => array of result set handles

Request JSON format
```javascript
 {
     "command": "closeResultSet",
     "attributes": {
             // as defined separately
     },
     "resultSetHandles": [ <number> ]
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * exception (object, optional) =>  only present if status is "error"
    * text (string) => exception message which provides error details
    * sqlCode (string) => five-character exception code if known, otherwise "00000"

Response JSON format
```javascript
 {
     "status": <"ok" | "error">,
     // in case of "error"
     "exception": { // Optional: error
             "text": <string>, // Exception text
             "sqlCode": <string> // Five-character exception code if known, otherwise "00000"
     }
 }
```

### CreatePreparedStatement: Creates a prepared statement

This command creates a prepared statement.

Request fields:
  * command (string) => command name: "createPreparedStatement"
  * attributes (object, optional) => attributes to set for the connection (see below)
  * sqlText (string) => SQL statement

Request JSON format
```javascript
 {
     "command": "createPreparedStatement",
     "attributes": {
             // as defined separately
     },
     "sqlText": <string>
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * attributes (object, optional) => attributes set for the connection (see below)
  * responseData (object, optional) => only present if status is "ok"
    * statementHandle (number) => prepared statement handle
    * parameterData (object, optional) => prepared statement parameter information
      * numColumns (number) => number of columns
      * columns (object[]) => array of column metadata objects
        * name (string) => column name: always "" as named parameters are not supported
        * dataType (object) => column metadata
        * type (string) => column data type
        * precision (number, optional) => column precision
        * scale (number, optional) => column scale
        * size (number, optional) => maximum size in bytes of a column value
        * characterSet (string, optional) => character encoding of a text column
        * withLocalTimeZone (true | false, optional) => specifies if a timestamp has a local time zone
        * fraction (number, optional) => fractional part of number
        * srid (number, optional) => spatial reference system identifier
      * numResults (number) => number of result objects
      * results (object[]) => array of result objects
        * resultType (string) => type of result: "resultSet" or "rowCount"
        * rowCount (number, optional) => present if resultType is "rowCount", number of rows
        * resultSet (object, optional) => present if resultType is "resultSet", result set
          * resultSetHandle (number, optional) => result set handle
          * numColumns (number) => number of columns in the result set
          * numRows (number) => number of rows in the result set
          * numRowsInMessage (number) => number of rows in the current message
          * columns (object[]) => array of column metadata objects
            * name (string) => column name
            * dataType (object) => column metadata
              * type (string) => column data type
              * precision (number, optional) => column precision
              * scale (number, optional) => column scale
              * size (number, optional) => maximum size in bytes of a column value
              * characterSet (string, optional) => character encoding of a text column
              * withLocalTimeZone (true | false, optional) => specifies if a timestamp has a local time zone
              * fraction (number, optional) => fractional part of number
              * srid (number, optional) => spatial reference system identifier
  * exception (object, optional) =>  only present if status is "error"
    * text (string) => exception message which provides error details
    * sqlCode (string) => five-character exception code if known, otherwise "00000"

Response JSON format
```javascript
 {
     "status": <"ok" | "error">,
     "attributes": {
         // as defined separately
     },
     // if status is "ok"
     "responseData": {
         "statementHandle": <number>,
         "parameterData": {
             "numColumns": <number>,
             "columns": [ {
                 "name": <string>,
                 "dataType": {
                     "type": <string>,
                     "precision": <number>,
                     "scale": <number>,
                     "size": <number>,
                     "characterSet": <number>,
                     "withLocalTimeZone": <true | false>,
                     "fraction": <number>,
                     "srid": <number>
                 }
             } ]
         },
         "numResults": <number>,
         "results": [ {
             "resultType": <"resultSet" | "rowCount">,
             // if type is "rowCount"
             "rowCount": <number>,
             // if type is "resultSet"
             "resultSet": {
                 "resultSetHandle": <number>,
                 "numColumns": <number>,
                 "numRows": <number>,
                 "numRowsInMessage": <number>,
                 "columns": [ {
                     "name": <string>,
                     "dataType": {
                         "type": <string>,
                         "precision": <number>,
                         "scale": <number>,
                         "size": <number>,
                         "characterSet": <number>,
                         "withLocalTimeZone": <true | false>,
                         "fraction": <number>,
                         "srid": <number>
                     }
                 } ]
             }
         } ]
     },
     // if status is "error"
     "exception": {
         "text": <string>,
         "sqlCode": <string>
     }
 }
```

### Disconnect: Closes a connection to Exasol

This command closes the connection between the client and Exasol.
After the connection is closed, it cannot be used for further
interaction with Exasol anymore.

Request fields:
  * command (string) => command name: "disconnect"
  * attributes (object, optional) => attributes to set for the connection (see below)

Request JSON format
```javascript
 {
     "command": "disconnect",
     "attributes": {
             // as defined separately
     }
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * attributes (object, optional) => attributes set for the connection (see below)
  * exception (object, optional) =>  only present if status is "error"
    * text (string) => exception message which provides error details
    * sqlCode (string) => five-character exception code if known, otherwise "00000"

Reponse JSON format
```javascript
 {
     "status": <"ok" | "error">,
     "attributes": {
             // as defined separately
     },
     // if status is "error"
     "exception": {
             "text": <string>,
             "sqlCode": <string>
     }
 }
```

### EnterParallel: Opens subconnections for parallel execution

This command opens subconnections, which are additional connections to
other nodes in the cluster, for the purpose of parallel execution. If
the requested number of subconnections is 0, all open subconnections
are closed.

Request fields:
  * command (string) => command name: "enterParallel"
  * attributes (object, optional) => attributes to set for the connection (see below)
  * hostIp (string) => IP address of the Exasol host to which the client is currently connected (i.e., the Exasol host used to create the connection; e.g., ws://\<hostIp\>:8563)
  * numRequestedConnections (number) => number of subconnections to open. If 0, all open subconnections are closed.

Request JSON format
```javascript
 {
     "command": "enterParallel",
     "attributes": {
             // as defined separately
     },
     "hostIp": <string>,
     "numRequestedConnections": <number>
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * responseData (object, optional) => only present if status is "ok"
    * numOpenConnections (number) => number of subconnections actually opened
    * token (number) => token required for the login of subconnections
    * nodes (string[]) => IP addresses and ports of the nodes, to which subconnections may be established
  * exception (object, optional) =>  only present if status is "error"
    * text (string) => exception message which provides error details
    * sqlCode (string) => five-character exception code if known, otherwise "00000"

Response JSON format
```javascript
 {
     "status": <"ok" | "error">,
     // in case of "ok"
     "responseData": {
             "numOpenConnections": <number>,
             "token": <number>,
             "nodes": [
                     <string>
             ]
     },
     // in case of "error"
     "exception": {
             "text": <string>,
             "sqlCode": <string>
     }
 }
```

### Execute: Executes an SQL statement

This command executes an SQL statement.

If the SQL statement returns a result set which has less than 1,000 rows of data, the data will be provided in the data field of resultSet. However if the SQL statement returns a result set which has 1,000 or more rows of data, a result set will be opened whose handle is returned in the resultSetHandle field of resultSet. Using this handle, the data from the result set can be retrieved using the Fetch command. Once the result set is no longer needed, it should be closed using the CloseResultSet command.

Request fields:
  * command (string) => command name: "executePreparedStatement"
  * attributes (object) => attributes to set for the connection (see below)
  * sqlText (string) => SQL statement to execute

Request JSON format
```javascript
 {
     "command": "execute",
     "attributes": {
             // as defined separately
     },
     "sqlText": <string>
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * attributes (object, optional) => attributes set for the connection (see below)
  * responseData (object, optional) => only present if status is "ok"
    * numResults (number) => number of result objects
    * results (object[]) => array of result objects
      * resultType (string) => type of result: "resultSet" or "rowCount"
      * rowCount (number, optional) => present if resultType is "rowCount", number of rows
      * resultSet (object, optional) => present if resultType is "resultSet", result set
        * resultSetHandle (number) => result set handle
        * numColumns (number) => number of columns in the result set
        * numRows (number) => number of rows in the result set
        * numRowsInMessage (number, optional) => number of rows in the current message
        * columns (object[]) => array of column metadata objects
          * name (string) => column name
          * dataType (object) => column metadata
            * type (string) => column data type
            * precision (number, optional) => column precision
            * scale (number, optional) => column scale
            * size (number, optional) => maximum size in bytes of a column value
            * characterSet (string, optional) => character encoding of a text column
            * withLocalTimeZone (true | false, optional) => specifies if a timestamp has a local time zone
            * fraction (number, optional) => fractional part of number
            * srid (number, optional) => spatial reference system identifier
        * data (array[], optional) => object containing the data for the prepared statement in column-major order
  * exception (object, optional) =>  only present if status is "error"
    * text (string) => exception message which provides error details
    * sqlCode (string) => five-character exception code if known, otherwise "00000"

Response JSON format
```javascript
 {
     "status": <"ok" | "error">,
     "attributes": {
         // as defined separately
     },
     // in case of "ok"
     "responseData": { // Optional: ok
         "numResults": <number>,
         "results": [ {
             "resultType": <"resultSet" | "rowCount">,
             // if type is "rowCount"
             "rowCount": <number>,
             // if type is "resultSet"
             "resultSet": {
                 "resultSetHandle": <number>,
                 "numColumns": <number>,
                 "numRows": <number>,
                 "numRowsInMessage": <number>,
                 "columns": [ {
                     "name": <string>,
                     "dataType": {
                         "type": <string>,
                         "precision": <number>,
                         "scale": <number>,
                         "size": <number>,
                         "characterSet": <number>,
                         "withLocalTimeZone": <true | false>,
                         "fraction": <number>,
                         "srid": <number>
                     }
                 } ],
                 "data": [
                     [
                         <string | number | true | false | null>
                     ]
                 ]
             }
         } ]
     },
     // in case of "error"
     "exception": {
         "text": <string>,
         "sqlCode": <string>
     }
 }
```

### ExecuteBatch: Executes multiple SQL statements as a batch

This command executes multiple SQL statements sequentially as a batch.

If the SQL statement returns a result set which has less than 1,000 rows of data, the data will be provided in the data field of resultSet. However if the SQL statement returns a result set which has 1,000 or more rows of data, a result set will be opened whose handle is returned in the resultSetHandle field of resultSet. Using this handle, the data from the result set can be retrieved using the Fetch command. Once the result set is no longer needed, it should be closed using the CloseResultSet command.

Request fields:
  * command (string) => command name: "executeBatch"
  * attributes (object, optional) => attributes to set for the connection (see below)
  * sqlTexts (string[]) => array of SQL statement to execute

Request JSON format
```javascript
 {
     "command": "executeBatch",
     "attributes": {
             // as defined separately
     },
     "sqlTexts": [
             <string>
     ]
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * attributes (object, optional) => attributes set for the connection (see below)
  * responseData (object, optional) => only present if status is "ok"
    * numResults (number) => number of result objects
    * results (object[]) => array of result objects
      * resultType (string) => type of result: "resultSet" or "rowCount"
      * rowCount (number, optional) => present if resultType is "rowCount", number of rows
      * resultSet (object, optional) => present if resultType is "resultSet", result set
        * resultSetHandle (number, optional) => result set handle
        * numColumns (number) => number of columns in the result set
        * numRows (number) => number of rows in the result set
        * numRowsInMessage (number) => number of rows in the current message
        * columns (object[]) => array of column metadata objects
          * name (string) => column name
          * dataType (object) => column metadata
            * type (string) => column data type
            * precision (number, optional) => column precision
            * scale (number, optional) => column scale
            * size (number, optional) => maximum size in bytes of a column value
            * characterSet (string, optional) => character encoding of a text column
            * withLocalTimeZone (true | false, optional) => specifies if a timestamp has a local time zone
            * fraction (number, optional) => fractional part of number
            * srid (number, optional) => spatial reference system identifier
        * data (array[], optional) => object containing the data for the prepared statement in column-major order
  * exception (object, optional) =>  only present if status is "error"
    * text (string) => exception message which provides error details
    * sqlCode (string) => five-character exception code if known, otherwise "00000"

Response JSON format
```javascript
 {
     "status": <"ok" | "error">,
     "attributes": {
         // as defined separately
     },
     // in case of "ok"
     "responseData": {
         "numResults": <number>,
         "results": [ {
             "resultType": <"resultSet" | "rowCount">,
             // if type is "rowCount"
             "rowCount": <number>,
             // if type is "resultSet"
             "resultSet": {
                 "resultSetHandle": <number>,
                 "numColumns": <number>,
                 "numRows": <number>,
                 "numRowsInMessage": <number>,
                 "columns": [ {
                     "name": <string>,
                     "dataType": {
                         "type": <string>,
                         "precision": <number>,
                         "scale": <number>,
                         "size": <number>,
                         "characterSet": <number>,
                         "withLocalTimeZone": <true | false>,
                         "fraction": <number>,
                         "srid": <number>
                     }
                 } ],
                 "data": [
                     [
                         <string | number | true | false | null>
                     ]
                 ]
             }
         } ]
     },
     // in case of "error"
     "exception": {
         "text": <string>,
         "sqlCode": <string>
     }
 }
```

### ExecutePreparedStatement: Executes a prepared statement

This command executes a prepared statement which has already been
created.

If the SQL statement returns a result set which has less than 1,000 rows of data, the data will be provided in the data field of resultSet. However if the SQL statement returns a result set which has 1,000 or more rows of data, a result set will be opened whose handle is returned in the resultSetHandle field of resultSet. Using this handle, the data from the result set can be retrieved using the Fetch command. Once the result set is no longer needed, it should be closed using the CloseResultSet command.

Request fields:
  * command (string) => command name: "executePreparedStatement"
  * attributes (object, optional) =>   attributes to set for the connection (see below)
  * statementHandle (number) => prepared statement handle
  * numColumns (number) => number of columns in data
  * numRows (number) => number of rows in data
  * columns (object[], optional) => array of column metadata objects
    * name (string) => column name
    * dataType (object) => column metadata
      * type (string) => column data type
      * precision (number, optional) => column precision
      * scale (number, optional) => column scale
      * size (number, optional) => maximum size in bytes of a column value
      * characterSet (string, optional) => character encoding of a text column
      * withLocalTimeZone (true | false, optional) => specifies if a timestamp has a local time zone
      * fraction (number, optional) => fractional part of number
      * srid (number, optional) => spatial reference system identifier
  * data (array[], optional) => array containing the data for the prepared statement in column-major order

Request JSON format
```javascript
 {
    "command": "executePreparedStatement",
    "attributes": {
        // as defined separately
    },
    "statementHandle": <number>,
    "numColumns": <number>,
    "numRows": <number>,
    "columns": [ {
        "name": <string>,
        "dataType": {
            "type": <string>,
            "precision": <number>,
            "scale": <number>,
            "size": <number>,
            "characterSet": <number>,
            "withLocalTimeZone": <boolean>,
            "fraction": <number>,
            "srid": <number>
        }
    } ],
    "data": [
        [
            <string | number | true | false | null>
        ]
    ]
 }
```

Response fields:

  * status (string) => command status: "ok" or "error"
  * attributes (object, optional) => attributes set for the connection (see below)
  * responseData (object, optional) => only present if status is "ok"
    * numResults (number) => number of result objects
    * results (object[]) => array of result objects
      * resultType (string) => type of result: "resultSet" or "rowCount"
      * rowCount (number, optional) => present if resultType is "rowCount", number of rows
      * resultSet (object, optional) => present if resultType is "resultSet", result set
        * resultSetHandle (number, optional) => result set handle
        * numColumns (number) => number of columns in the result set
        * numRows (number) => number of rows in the result set
        * numRowsInMessage (number) => number of rows in the current message
        * columns (object[]) => array of column metadata objects
          * name (string) => column name
          * dataType (object) => column metadata
            * type (string) => column data type
            * precision (number, optional) => column precision
            * scale (number, optional) => column scale
            * size (number, optional) => maximum size in bytes of a column value
            * characterSet (string, optional) => character encoding of a text column
            * withLocalTimeZone (true | false, optional) => specifies if a timestamp has a local time zone
            * fraction (number, optional) => fractional part of number
            * srid (number, optional) => spatial reference system identifier
        * data (array[], optional) => object containing the data for the prepared statement in column-major order
  * exception (object, optional) =>  only present if status is "error"
    * text (string) => exception message which provides error details
    * sqlCode (string) => five-character exception code if known, otherwise "00000"

Response JSON format
```javascript
 {
     "status": <"ok" | "error">,
     "attributes": {
         // as defined separately
     },
     // in case of "ok"
     "responseData": {
         "numResults": <number>,
         "results": [ {
             "resultType": <"resultSet" | "rowCount">,
             // if type is "rowCount"
             "rowCount": <number>,
             // if type is "resultSet"
             "resultSet": {
                 "resultSetHandle": <number>,
                 "numColumns": <number>,
                 "numRows": <number>,
                 "numRowsInMessage": <number>,
                 "columns": [ {
                     "name": <string>,
                     "dataType": {
                         "type": <string>,
                         "precision": <number>,
                         "scale": <number>,
                         "size": <number>,
                         "characterSet": <number>,
                         "withLocalTimeZone": <true | false>,
                         "fraction": <number>,
                         "srid": <number>
                     }
                 } ],
                 "data": [
                     [
                         <string | number | true | false | null>
                     ]
                 ]
             }
         } ]
     },
     // in case of "error"
     "exception": {
         "text": <string>,
         "sqlCode": <string>
     }
 }
```

### Fetch: Retrieves data from a result set

This command retrieves data from a result set.

Request fields:
  * command (string) => command name: "fetch"
  * attributes (object, optional) =>  attributes to set for the connection (see below)
  * resultSetHandle (number) => result set handle
  * startPosition (number) => row offset (0-based) from which to begin data retrieval
  * numBytes (number) => number of bytes to retrieve (max: 64MB)

Request JSON format
```javascript
 {
     "command": "fetch",
     "attributes": {
             // as defined separately
     },
     "resultSetHandle": <number>,
     "startPosition": <number>,
     "numBytes": <number>
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * responseData (object, optional) => only present if status is "ok"
    * numRows (number) => number of rows fetched from the result set
    * data (array[]) => object containing the data for the prepared statement in column-major order
  * exception (object, optional) =>  only present if status is "error"
    * text (string) => exception message which provides error details
    * sqlCode (string) => five-character exception code if known, otherwise "00000"

Response JSON format
```javascript
 {
     "status": <"ok" | "error">,
     // in case of "ok"
     "responseData": {
             "numRows": <number>,
             "data": [
                 [
                     <string | number | true | false | null>
                 ]
             ]
     },
     // in case of "error"
     "exception": {
             "text": <string>,
             "sqlCode": <string>
     }
 }
```

### GetAttributes: Gets the session attribute values

This command retrieves the session attribute values.

Request fields:
  * command (string) => command name: "getAttributes"
  * attributes (object, optional) => attributes to set for the connection (see below)

JSON format
```javascript
 {
     "command": "getAttributes",
     "attributes": {
             // as defined separately
     },
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * attributes (object, optional) => attributes set for the connection (see below)
  * exception(object, optional) =>  only present if status is "error"
    * text (string) => exception message which provides error details
    * sqlCode (string) => five-character exception code if known, otherwise "00000"

Reponse JSON format
```javascript
 {
     "status": <"ok" | "error">,
     "attributes": {
             // as defined separately
     },
     // if status is "error"
     "exception": {
             "text": <string>,
             "sqlCode": <string>
     }
 }
```

### GetCatalogs: Gets the catalog names

### GetColumnPrivileges: Gets column privilege descriptions

### GetColumns: Gets column descriptions

### GetHosts: Gets the hosts in a cluster

This command gets the number hosts and the IP address of each host in
an Exasol cluster.

Request fields:
  * command (string) => command name: "getHosts"
  * attributes (object, optional) => attributes to set for the connection (see below)
  * hostIp (string) => IP address of the Exasol host to which the client is currently connected (i.e., the Exasol host used to create the connection; e.g., ws://\<hostIp\>:8563)

Request JSON format
```javascript
 {
     "command": "getHosts",
     "attributes": {
             // as defined separately
     },
     "hostIp": <string>
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * responseData (object, optional) => only present if status is "ok"
    * numNodes (number) => number of nodes in the cluster
    * nodes (string[]) => array of cluster node IP addresses
  * exception (object, optional) =>  only present if status is "error"
    * text (string) => exception message which provides error
         details
    * sqlCode (string) => five-character exception code if known,
         otherwise "00000"

Response JSON format
```javascript
 {
     "status": <"ok" | "error">,
     // in case of "ok"
     "responseData": {
             "numNodes": <number>,
             "nodes": [
                     <string>
             ]
     },
     // in case of "error"
     "exception": {
             "text": <string>,
             "sqlCode": <string>
     }
 }
```

### GetOffset: Gets the row offset of a result set

This command retrieves the row offset of the result set of this
(sub)connection. This is the row number of the first row of the current
(sub)connection's result set in the global result set.

Request fields:
  * command (string) => command name: "getOffset"
  * attributes (object, optional) => attributes to set for the connection (see below)
  * resultSetHandle (number) => open result set handle

Request JSON format
```javascript
 {
     "command": "getOffset",
     "attributes": {
             // as defined separately
     },
     "resultSetHandle": <number>
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * responseData (object, optional) => only present if status is "ok"
    * rowOffset (number) => row offset of connection's result set
  * exception (object, optional) =>  only present if status is "error"
    * text (string) => exception message which provides error details
    * sqlCode (string) => five-character exception code if known, otherwise "00000"

Response JSON format
```javascript
 {
     "status": <"ok" | "error">,
     // in case of "ok"
     "responseData": {
             "rowOffset": <number>
     },
     // in case of "error"
     "exception": {
             "text": <string>,
             "sqlCode": <string>
     }
 }
```

### GetPrimaryKeys: Gets primary key descriptions

### GetProcedureColumns: Gets procedure column descriptions

### GetProcedures: Gets procedure descriptions

### GetResultSetHeader: Gets a result set header

This command retrieves a header (i.e., empty result set) which contains
the metadata for an open result set.

Request fields:
  * command (string) => command name: "getResultSetHeader"
  * attributes (object, optional) => attributes to set for the connection (see below)
  * resultSetHandles (number[]) => array of open result set handles

Request JSON format
```javascript
 {
     "command": "getResultSetHeader",
     "attributes": {
             // as defined separately
     },
     "resultSetHandles": [
         <number>
     ]
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * attributes (object, optional) => attributes set for the connection (see below)
  * responseData (object, optional) => only present if status is "ok"
    * numResults (number) => number of result objects
    * results (object[]) => array of result objects
      * resultType (string) => type of result: "resultSet"
      * resultSet (object) => result set
        * resultSetHandle (number, optional) => result set handle
        * numColumns (number) => number of columns in the result set
        * numRows (number) => number of rows in the result set
        * numRowsInMessage (number) => number of rows in the current message
        * columns (object[]) => array of column metadata objects
          * name (string) => column name
          * dataType (object) => column metadata
            * type (string) => column data type
            * precision (number, optional) => column precision
            * scale (number, optional) => column scale
            * size (number, optional) => maximum size in bytes of a column value
            * characterSet (string, optional) => character encoding of a text column
            * withLocalTimeZone (true | false, optional) => specifies if a timestamp has a local time zone
            * fraction (number, optional) => fractional part of number
            * srid (number, optional) => spatial reference system identifier
  * exception (object, optional) =>  only present if status is "error"
    * text (string) => exception message which provides error details
    * sqlCode (string) => five-character exception code if known, otherwise "00000"

Response JSON format
```javascript
 {
     "status": <"ok" | "error">,
     "attributes": {
         // as defined separately
     },
     // in case of "ok"
     "responseData": {
         "numResults": <number>,
         "results": [ {
             "resultType": "resultSet",
             "resultSet": {
                 "resultSetHandle": <number>,
                 "numColumns": <number>,
                 "numRows": <number>,
                 "numRowsInMessage": <number>,
                 "columns": [ {
                     "name": <string>,
                     "dataType": {
                         "type": <string>,
                         "precision": <number>,
                         "scale": <number>,
                         "size": <number>,
                         "characterSet": <number>,
                         "withLocalTimeZone": <true | false>,
                         "fraction": <number>,
                         "srid": <number>
                     }
                 } ]
             }
         } ]
     },
     // in case of "error"
     "exception": {
         "text": <string>,
         "sqlCode": <string>
     }
 }
```

### GetSchemas: Gets the schema names

### GetTablePrivileges: Gets table privilege descriptions

### GetTables: Gets table descriptions

### GetTableTypes: Gets the supported table types

### GetTypeInfo: Gets the supported data types

### Login: Establishes a connection to Exasol

This command invokes the login process which establishes a connection
between the client and Exasol. As long as the connection is open,
the user can interact with Exasol using the commands specified
below.

The login process is composed of four steps:

1. The client sends the login command including the requested protocol 
   version.
   
   Request fields:
     * command (string) => command name: "login"
     * protocolVersion (number) => requested WebSocket protocol version, (e.g., 1)
   
   Request JSON format
   ```javascript
    {
        "command": "login",
        "protocolVersion": <number>
    }
   ```

2. The server returns a public key which is used to encode the
   user's password. The public key can be obtained in one of two ways:
    a. importing the key using the publicKeyPem field
    b. constructing the key using the publicKeyModulus and publicKeyExponent fields

   Response fields:
     * status (string) => command status: "ok" or "error"
     * responseData (object, optional) => only present if status is "ok"
       * publicKeyPem (string) => PEM-formatted, 1024-bit RSA public key used to encode the user's password (see 3.)
       * publicKeyModulus (string) => hexadecimal modulus of the 1024-bit RSA public key used to encode the user's password (see 3.)
       * publicKeyExponent (string) => hexadecimal exponent of the 1024-bit RSA public key used to encode the user's password (see 3.)
     * exception (object, optional) => only present if status is "error"
       * text (string) => exception message which provides error details
       * sqlCode (string) => five-character exception code if known, otherwise "00000"
   
   Response JSON format
   ```javascript
    {
        "status": <"ok" | "error">,
        // if status is "ok"
        "responseData": {
                "publicKeyPem": <string>,
                "publicKeyModulus": <string>,
                "publicKeyExponent": <string>
    },
        // if status is "error"
        "exception": {
                "text": <string>,
                "sqlCode": <string>
        }
    }
   ```
   
   
3. The client sends the username, encrypted password, and optionally
   other client information.
   
   Request fields:
     * username (string) => Exasol user name to use for the login process
     * password (string) => user's password, which is encrypted using publicKey (see 2.) and PKCS #1 v1.5 padding, encoded in Base64 format
     * useCompression (boolean) => use compression for messages during the session (beginning after the login process is completed)
     * sessionId (number, optional) => requested session ID
     * clientName (string, optional) => client program name, (e.g., "EXAplus")
     * driverName (string, optional) => driver name, (e.g., "EXA Python")
     * clientOs (string, optional) => name and version of the client operating system
     * clientOsUsername (string, optional) => client's operating system user name
     * clientLanguage (string, optional) => language setting of the client system
     * clientVersion (string, optional) => client version number
     * clientRuntime (string, optional) => name and version of the client runtime
     * attributes (object, optional) => array of attributes to set for the connection (see below)
   
   Request JSON format
   ```javascript
    {
        "username": <string>,
        "password": <string>,
        "useCompression": <boolean>,
        "sessionId": <number>,
        "clientName": <string>,
        "driverName": <string>,
        "clientOs": <string>,
        "clientOsUsername": <string>,
        "clientLanguage": <string>,
        "clientVersion": <string>,
        "clientRuntime": <string>,
        "attributes": {
                // as defined separately
        }
    }
   ```
   
   
4. The server uses username and password (see 3.) to authenticate the
   user. If successful, the server replies with an "ok" response and a
   connection is established. If authentication of the user fails, the
   server sends an "error" response to the client indicating that the login
   process failed and a connection couldn't be established.
   
   Response fields:
     * status (string) => command status: "ok" or "error"
     * responseData (object, optional) => only present if status is "ok"
       * sessionId (number) => current session ID
       * protocolVersion (number) => WebSocket protocol version of the connection (e.g., 1)
       * releaseVersion (string) => Exasol version (e.g. "6.0.0")
       * databaseName (string) => database name (e.g., "productionDB1")
       * productName (string) => Exasol product name: "EXASolution"
       * maxDataMessageSize (number) => maximum size of a data message in bytes
       * maxIdentifierLength (number) => maximum length of identifiers
       * maxVarcharLength (number) =>  maximum length of VARCHAR values
       * identifierQuoteString (string) => value of the identifier quote string (e.g., "'")
       * timeZone (string) => name of the session time zone
       * timeZoneBehavior (string) => value of the session option "TIME_ZONE_BEHAVIOR"
     * exception (object, optional) =>  only present if status is "error"
       * text (string) => exception message which provides error details
       * sqlCode (string) => five-character exception code if known, otherwise "00000"
   
   Response JSON format
   ```javascript
    {
        "status": <"ok" | "error">,
        // if status is "ok"
        "responseData": {
                "sessionId": <number>,
                "protocolVersion": <number>,
                "releaseVersion": <string>,
                "databaseName": <string>,
                "productName": <string>,
                "maxDataMessageSize": <number>,
                "maxIdentifierLength": <number>,
                "maxVarcharLength": <number>,
                "identifierQuoteString": <string>,
                "timeZone": <string>,
                "timeZoneBehavior": <string>
        },
        // if status is "error"
        "exception": {
                "text": <string>,
                "sqlCode": <string>
        }
    }
   ```

### SetAttributes: Sets the given session attribute values

This command sets the specified session attribute values.

Request fields:
  * command (string) => command name: "getAttributes"
  * attributes (object, optional) =>  attributes to set for the connection (see below)

Request JSON format
```javascript
 {
     "command": "setAttributes",
     "attributes": {
             // as defined separately
     }
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * attributes (object, optional) =>  attributes set for the connection (see below)
  * exception (object, optional) =>  only present if status is "error"
    * text (string) => exception message which provides error details
    * sqlCode (string) => five-character exception code if known, otherwise "00000"

Response JSON format
```javascript
 {
     "status": <"ok" | "error">,
     "attributes": {
             // as defined separately
     },
     // if status is "error"
     "exception": {
             "text": <string>,
             "sqlCode": <string>
     }
 }
```

### SubLogin: Establishes a subconnection to Exasol

This command invokes the login process, which establishes a
subconnection between the client and Exasol. Using subconnections,
the user can interact with Exasol in parallel using the commands
specified below.

The login process is composed of four steps:

1. The client sends the login command including the requested protocol
   version.
   
   Request fields:
     * command (string) => command name: "login"
     * protocolVersion (number) => requested WebSocket protocol version, (e.g., 1)
   
   Request JSON format
   ```javascript
    {
        "command": "subLogin",
        "protocolVersion": <number>
    }
   ```


2. The server returns a public key which is used to encode the
   user's password. The public key can be obtained in one of two ways:
    a. importing the key using the publicKeyPem field
    b. constructing the key using the publicKeyModulus and publicKeyExponent fields.
   
   Response fields:
     * status (string) => command status: "ok" or "error"
     * responseData (object, optional) => only present if status is "ok"
       * publicKeyPem (string) => PEM-formatted, 1024-bit RSA public key used to encode the user's password (see 3.)
       * publicKeyModulus (string) => hexadecimal modulus of the 1024-bit RSA public key used to encode the user's password (see 3.)
       * publicKeyExponent (string) => hexadecimal exponent of the 1024-bit RSA public key used to encode the user's password (see 3.)
     * exception (object, optional) => only present if status is "error"
       * text (string) => exception message which provides error details
       * sqlCode (string) => five-character exception code if known, otherwise "00000"
   
   Response JSON format
   ```javascript
    {
        "status": <"ok" | "error">,
        // if status is "ok"
        "responseData": {
                "publicKeyPem": <string>,
                "publicKeyModulus": <string>,
                "publicKeyExponent": <string>
        },
        // if status is "error"
        "exception": {
                "text": <string>,
                "sqlCode": <string>
        }
    }
   ```
   

3. The client sends the username, encrypted password, and token.

   Request fields:
     * username (string) => Exasol user name to use for the login process
     * password (string) => user's password, which is encrypted using publicKey (see 2.) and PKCS #1 v1.5 padding, encoded in Base64 format
     * token (number) => token required for subconnection logins (see, EnterParallel)
   
   Request JSON format
   ```javascript
    {
        "username": <string>,
        "password": <string>,
        "token": <number>
    }
   ```
   
4. The server uses username, password, and token (see 3.) to
   authenticate the user. If successful, the server replies with an
   "ok" response and a subconnection is established. If authentication of
   the user fails, the server sends an "error" response to the client
   indicating that the login process failed and a subconnection couldn't
   be established.
   
   Response fields:
     * status (string) => command status: "ok" or "error"
     * responseData (object, optional) => only present if status is "ok"
       * sessionId (number) => current session ID
       * protocolVersion (number) => WebSocket protocol version of the connection (e.g., 1)
       * releaseVersion (string) => Exasol version (e.g. "6.0.0")
       * databaseName (string) => database name (e.g., "productionDB1")
       * productName (string) => Exasol product name: "EXASolution"
       * maxDataMessageSize (number) => maximum size of a data message in bytes
       * maxIdentifierLength (number) => maximum length of identifiers
       * maxVarcharLength (number) =>  maximum length of VARCHAR values
       * identifierQuoteString (string) => value of the identifier quote string (e.g., "'")
       * timeZone (string) => name of the session time zone
       * timeZoneBehavior (string) => value of the session option "TIME_ZONE_BEHAVIOR"
     * exception (object, optional) =>  only present if status is "error"
       * text (string) => exception message which provides error details
       * sqlCode (string) => five-character exception code if known, otherwise "00000"
   
   Response JSON format
   ```javascript
    {
        "status": <"ok" | "error">,
        // if status is "ok"
        "responseData": {
                "sessionId": <number>,
                "protocolVersion": <number>,
                "releaseVersion": <string>,
                "databaseName": <string>,
                "productName": <string>,
                "maxDataMessageSize": <number>,
                "maxIdentifierLength": <number>,
                "maxVarcharLength": <number>,
                "identifierQuoteString": <string>,
                "timeZone": <string>,
                "timeZoneBehavior": <string>
        },
        // if status is "error"
        "exception": {
                "text": <string>,
                "sqlCode": <string>
        }
    }
   ```
