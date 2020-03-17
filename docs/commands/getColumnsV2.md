### getColumns: Gets the column descriptions

This commands gets the specified columns descriptions in the database.

Result set columns: Ordered by `TABLE_CAT`, `TABLE_SCHEM`, `TABLE_NAME`, `ORDINAL_POSITION`.
| Name | Data Type | Description |
| --- | --- | --- |
| TABLE_CAT | string | catalog name |
| TABLE_SCHEM | string | schema name |
| TABLE_NAME | string | table name |
| COLUMN_NAME | string | column name |
| DATA_TYPE | number | data type from java.sql.Types |
| TYPE_NAME | string | type name |
| COLUMN_SIZE | number | column size |
| BUFFER_LENGTH | number | unused |
| DECIMAL_DIGITS | number | number of fractional digits |
| NUM_PREC_RADIX | number | number base |
| NULLABLE | number | is nullable (0 = not nullable, 1 = nullable, 2 = unknown) |
| REMARKS | string | column comment |
| COLUMN_DEF | string | default value |
| SQL_DATA_TYPE | number | unused |
| SQL_DATETIME_SUB | number | unused |
| CHAR_OCTET_LENGTH | number | maximum size |
| ORDINAL_POSITION | number | column number in the table (starting at 1) |
| IS_NULLABLE | string | is nullable ("NO" = not nullable, "YES" = nullable, "" = unknown) |
| SCOPE_CATALOG | string | unused |
| SCOPE_SCHEMA | string | unused |
| SCOPE_TABLE | string | unused |
| SOURCE_DATA_TYPE | number | unused |
| IS_AUTOINCREMENT | string | is auto incremented (i.e. identity column) ("NO" = not auto incremented, "YES" = auto incremented, "" = unknown) |
| IS_GENERATEDCOLUMN | string | is generated (i.e. identity column) ("NO" = not generated, "YES" = generated, "" = unknown) |

If the command returns a result set which has less than 1,000 rows of data, the data will be provided in the `data` field of `resultSet`. However if the command returns a result set which has 1,000 or more rows of data, a result set will be opened whose handle is returned in the `resultSetHandle` field of `resultSet`. Using this handle, the data from the result set can be retrieved using the `fetch` command. Once the result set is no longer needed, it should be closed using the `closeResultSet` command.

Request fields:
  * command (string) => command name: "getColumns"
  * attributes (object, optional) => attributes to set for the connection (see [Attributes](../WebsocketAPIV2.md#attributes-session-and-database-properties))
  * catalog (string, optional) => catalog name (i.e. "EXA_DB"). `""` means no catalog, `null` means all catalogs.
  * schema (string, optional) => schema name search criteria in SQL `LIKE` format. `""` means no schema, `null` means all schemas.
  * table (string, optional) => table name search criteria in SQL `LIKE` format. `""` means no table, `null` means all tables.
  * column (string, optional) => column name search criteria in SQL `LIKE` format. `""` means no column, `null` means all columns.

Request JSON format
```javascript
 {
     "command": "getColumns",
     "attributes": {
             // as defined separately
     },
     "catalog": <string>,
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
                         "characterSet": <number>
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
