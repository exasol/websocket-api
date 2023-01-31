### createPreparedStatement: Creates a prepared statement

This command creates a prepared statement.

Request fields:

  * command (string) => command name: "createPreparedStatement"
  * attributes (object, optional) => attributes to set for the connection (see [Attributes](../WebsocketAPIV1.md#attributes-session-and-database-properties))
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
  * attributes (object, optional) => attributes set for the connection (see [Attributes](../WebsocketAPIV1.md#attributes-session-and-database-properties))
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
                     "characterSet": <string>,
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
                         "characterSet": <string>,
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
