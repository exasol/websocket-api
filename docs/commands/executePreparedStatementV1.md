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