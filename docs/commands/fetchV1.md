### fetch: Retrieves data from a result set

This command retrieves data from a result set.

Request fields:

  * command (string) => command name: "fetch"
  * attributes (object, optional) =>  attributes to set for the connection (see [Attributes](../WebsocketAPIV1.md#attributes-session-and-database-properties))
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
    * data (array[]) => object containing the data in column-major order
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
