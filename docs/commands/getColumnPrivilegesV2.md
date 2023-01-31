### getColumnPrivileges: Gets the column privilege descriptions

This command gets the specified column privilege descriptions in the database.

Result set columns: Ordered by `COLUMN`, `NAME`, `GRANTOR`, `GRANTEE`.

| Name | Data Type | Description |
| --- | --- | --- |
| SCHEMA | string | schema name |
| TABLE | string | table name |
| COLUMN | string | column name |
| NAME | string | privilege name |
| GRANTOR | string | privilege grantor |
| GRANTEE | string | privilege grantee |
| OWNER | string | column owner |

If the command returns a result set which has less than 1,000 rows of data, the data will be provided in the `data` field of `resultSet`. However if the command returns a result set which has 1,000 or more rows of data, a result set will be opened whose handle is returned in the `resultSetHandle` field of `resultSet`. Using this handle, the data from the result set can be retrieved using the `fetch` command. Once the result set is no longer needed, it should be closed using the `closeResultSet` command.

Request fields:

  * command (string) => command name: "getColumnPrivileges"
  * attributes (object, optional) => attributes to set for the connection (see [Attributes](../WebsocketAPIV2.md#attributes-session-and-database-properties))
  * schema (string, optional) => schema name. `""` means no schema, `null` means all schemas.
  * table (string, optional) => table name. `""` means no table, `null` means all tables.
  * column (string, optional) => column name search criteria in SQL `LIKE` format. `""` means no column, `null` means all columns.

Request JSON format
```javascript
 {
     "command": "getColumnPrivileges",
     "attributes": {
             // as defined separately
     },
     "schema": <string>,
     "table": <string>,
     "column": <string>
 }
```

Response fields:

  * status (string) => command status: "ok" or "error"
  * attributes (object, optional) => attributes set for the connection (see [Attributes](../WebsocketAPIV2.md#attributes-session-and-database-properties))
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
        * data (array[], optional) => object containing the data in column-major order
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
                         "characterSet": <string>
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
