### getTypeInfo: Gets the data types

This command gets the data types supported by the database.

Result set columns: Ordered by `TYPE_ID`.

| Name | Data Type | Description |
| --- | --- | --- |
| NAME | string | type name |
| TYPE_ID | number | data type ID |
| PRECISION | number | precision |
| LITERAL_PREFIX | string | literal quote prefix |
| LITERAL_SUFFIX | string | literal quote suffix |
| CREATE_PARAMS | string | type creation parameters |
| IS_NULLABLE | boolean | NULL values are allowed |
| CASE_SENSITIVE | boolean | is case sensitive |
| SEARCHABLE | number | how the type can be used in a WHERE clause:<br>0: cannot be searched<br>1: can only be searched with WHERE .. LIKE<br>2: cannot be searched with WHERE .. LIKE<br>3: can be searched with any WHERE clause |
| UNSIGNED_ATTRIBUTE | boolean | is unsigned |
| FIXED_PREC_SCALE | boolean | has fixed representation |
| AUTO_INCREMENT | boolean | is an automatically incremented type |
| LOCAL_TYPE_NAME | string | localized type name |
| MINIMUM_SCALE | number | minimum scale |
| MAXIMUM_SCALE | number | maximum scale |
| SQL_DATA_TYPE | number | SQL data type |
| SQL_DATETIME_SUB | number | datetime and interval subtype |
| NUM_PREC_RADIX | number | number base |
| INTERVAL_PRECISION | number | interval precision |

If the command returns a result set which has less than 1,000 rows of data, the data will be provided in the `data` field of `resultSet`. However if the command returns a result set which has 1,000 or more rows of data, a result set will be opened whose handle is returned in the `resultSetHandle` field of `resultSet`. Using this handle, the data from the result set can be retrieved using the `fetch` command. Once the result set is no longer needed, it should be closed using the `closeResultSet` command.

Request fields:

  * command (string) => command name: "getTypeInfo"
  * attributes (object, optional) => attributes to set for the connection (see [Attributes](../WebsocketAPIV2.md#attributes-session-and-database-properties))

Request JSON format
```javascript
 {
     "command": "getTypeInfo",
     "attributes": {
             // as defined separately
     }
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
