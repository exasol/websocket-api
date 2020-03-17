### getProcedureColumns: Gets the specified procedure column descriptions

This command gets the specified procedure column descriptions in the database.

Result set columns: Ordered by `PROCEDURE_CAT`, `PROCEDURE_SCHEM`, `PROCEDURE_NAME`, `SPECIFIC_NAME`.
| Name | Data Type | Description |
| --- | --- | --- |
| PROCEDURE_CAT | string | catalog name |
| PROCEDURE_SCHEM | string | schema name |
| PROCEDURE_NAME | string | procedure name |
| COLUMN_NAME | string | column/parameter name |
| COLUMN_TYPE | number | type of column/parameter |
| DATA_TYPE | number | data type from java.sql.Types |
| TYPE_NAME | string | type name |
| PRECISION | number | precision |
| LENGTH | number | length in bytes |
| SCALE | number | scale |
| RADIX | number | number base |
| NULLABLE | number | is nullable (0 = not nullable, 1 = nullable, 2 = unknown) |
| REMARKS | string | column/parameter comment |
| COLUMN_DEF | string | default value |
| SQL_DATA_TYPE | number | unused |
| SQL_DATETIME_SUB | number | unused |
| CHAR_OCTET_LENGTH | number | maximum size |
| ORDINAL_POSITION | number | column/parameter number (starting at 1) |
| IS_NULLABLE | string | is nullable ("NO" = not nullable, "YES" = nullable, "" = unknown) |
| SPECIFIC_NAME | string | procedure name |

:warning: This command always returns an empty result set.

Request fields:
  * command (string) => command name: "getProcedureColumns"
  * attributes (object, optional) => attributes to set for the connection (see [Attributes](../WebsocketAPIV2.md#attributes-session-and-database-properties))
  * catalog (string, optional) => catalog name (i.e. "EXA_DB"). `""` means no catalog, `null` means all catalogs.
  * schema (string, optional) => schema name search criteria in SQL `LIKE` format. `""` means no schema, `null` means all schemas.
  * procedure (string, optional) => procedure name search criteria in SQL `LIKE` format. `""` means no procedure, `null` means all procedures.
  * column (string, optional) => column/parameter name search criteria in SQL `LIKE` format. `""` means no column, `null` means all columns.

Request JSON format
```javascript
 {
     "command": "getProcedureColumns",
     "attributes": {
             // as defined separately
     },
     "catalog": <string>,
     "schema": <string>,
     "procedure": <string>,
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
