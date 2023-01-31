### closePreparedStatement: Closes a prepared statement

This command closes a prepared statement which has already been
created.

Request fields:

  * command (string) => command name: "closePreparedStatement"
  * attributes (object, optional) => attributes to set for the connection (see [Attributes](../WebsocketAPIV1.md#attributes-session-and-database-properties))
  * statementHandle (number) => prepared statement handle

Request JSON format
```javascript
 {
     "command": "closePreparedStatement",
     "attributes": {
             // as defined separately
     },
     "statementHandle": <number>
 }
```

Response fields:

  * status (string) => command status: "ok" or "error"
  * attributes (object) => attributes set for the connection (see [Attributes](../WebsocketAPIV1.md#attributes-session-and-database-properties))
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
     // in case of "error"
     "exception": {
             "text": <string>,
             "sqlCode": <string>
     }
 }
```
