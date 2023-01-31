### getColumns: Gets the column descriptions

This command gets the specified columns descriptions in the database.

Result set columns: Ordered by `SCHEMA`, `TABLE`, `ORDINAL_POSITION`.

| Name | Data Type | Description |
| --- | --- | --- |
| SCHEMA | string | schema name |
| TABLE | string | table name |
| NAME | string | column name |
| TABLE_TYPE | string | table type (supported values are "SYSTEM TABLE", "TABLE", "VIEW") |
| TYPE | string | data type |
| TYPE_ID | number | data type ID |
| MAXSIZE | number | maximum number of characters for strings |
| NUM_PREC | number | precision for numeric values |
| NUM_SCALE | number | scale for numeric values |
| ORDINAL_POSITION | number | column position in the table (beginning with 1) |
| IS_VIRTUAL | boolean | is part of a virtual table |
| IS_NULLABLE | boolean | are NULL values allowed (value is NULL for views) |
| IS_DISTRIBUTION_KEY | boolean | column is part of the distribution key |
| PARTITION_KEY_ORDINAL_POSITION | number | column position (beginning with 1) in the table's composite partition key, NULL for columns which are not part of it |
| DEFAULT | string | default value |
| IS_IDENTITY | boolean | has the identity attribute |
| OWNER | string | owner name |
| COMMENT | string | column comment |

If the command returns a result set which has less than 1,000 rows of data, the data will be provided in the `data` field of `resultSet`. However if the command returns a result set which has 1,000 or more rows of data, a result set will be opened whose handle is returned in the `resultSetHandle` field of `resultSet`. Using this handle, the data from the result set can be retrieved using the `fetch` command. Once the result set is no longer needed, it should be closed using the `closeResultSet` command.

Request fields:

  * command (string) => command name: "getColumns"
  * attributes (object, optional) => attributes to set for the connection (see [Attributes](../WebsocketAPIV2.md#attributes-session-and-database-properties))
  * schema (string, optional) => schema name search criteria in SQL `LIKE` format. `""` means no schema, `null` means all schemas.
  * table (string, optional) => table name search criteria in SQL `LIKE` format. `""` means no table, `null` means all tables.
  * column (string, optional) => column name search criteria in SQL `LIKE` format. `""` means no column, `null` means all columns.
  * tableTypes (string[], optional) => array of table types (supported values are "SYSTEM TABLE", "TABLE", "VIEW"). `null` means all table types.

Request JSON format
```javascript
 {
     "command": "getColumns",
     "attributes": {
             // as defined separately
     },
     "schema": <string>,
     "table": <string>,
     "column": <string>,
     "tableTypes": [
                  <string>
     ]
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
