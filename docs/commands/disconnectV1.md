### disconnect: Closes a connection to Exasol

This command closes the connection between the client and Exasol.
After the connection is closed, it cannot be used for further
interaction with Exasol.

Request fields:

  * command (string) => command name: "disconnect"
  * attributes (object, optional) => attributes to set for the connection (see [Attributes](../WebsocketAPIV1.md#attributes-session-and-database-properties))

Request JSON format
```javascript
 {
     "command": "disconnect",
     "attributes": {
             // as defined separately
     }
 }
```

Response fields:

  * status (string) => command status: "ok" or "error"
  * attributes (object, optional) => attributes set for the connection (see [Attributes](../WebsocketAPIV1.md#attributes-session-and-database-properties))
  * exception (object, optional) =>  only present if status is "error"
    * text (string) => exception message which provides error details
    * sqlCode (string) => five-character exception code if known, otherwise "00000"

Reponse JSON format
```javascript
 {
     "status": <"ok" | "error">,
     "attributes": {
             // as defined separately
     },
     // if status is "error"
     "exception": {
             "text": <string>,
             "sqlCode": <string>
     }
 }
```
