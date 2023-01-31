### getResultSetHeader: Gets a result set header

This command retrieves a header (i.e., empty result set) which contains
the metadata for an open result set.

Request fields:

  * command (string) => command name: "getResultSetHeader"
  * attributes (object, optional) => attributes to set for the connection (see [Attributes](../WebsocketAPIV1.md#attributes-session-and-database-properties))
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
  * attributes (object, optional) => attributes set for the connection (see [Attributes](../WebsocketAPIV1.md#attributes-session-and-database-properties))
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
                         "characterSet": <string>,
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
