### closeResultSet: Closes a result set

This command closes result sets.

Request fields:

  * command (string) => command name: "closeResultSet"`
  * attributes (object, optional) => attributes to set for the connection (see [Attributes](../WebsocketAPIV1.md#attributes-session-and-database-properties))
  * resultSetHandles (number[]) => array of result set handles

Request JSON format
```javascript
 {
     "command": "closeResultSet",
     "attributes": {
             // as defined separately
     },
     "resultSetHandles": [ <number> ]
 }
```

Response fields:

  * status (string) => command status: "ok" or "error"
  * exception (object, optional) =>  only present if status is "error"
    * text (string) => exception message which provides error details
    * sqlCode (string) => five-character exception code if known, otherwise "00000"

Response JSON format
```javascript
 {
     "status": <"ok" | "error">,
     // in case of "error"
     "exception": {
             "text": <string>, // Exception text
             "sqlCode": <string> // Five-character exception code if known, otherwise "00000"
     }
 }
```
