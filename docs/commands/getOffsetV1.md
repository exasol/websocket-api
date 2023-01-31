### getOffset: Gets the row offset of a result set

This command retrieves the row offset of the result set of this
(sub)connection. This is the row number of the first row of the current
(sub)connection's result set in the global result set.

Request fields:

  * command (string) => command name: "getOffset"
  * attributes (object, optional) => attributes to set for the connection (see [Attributes](../WebsocketAPIV1.md#attributes-session-and-database-properties))
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
