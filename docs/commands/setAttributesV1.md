### setAttributes: Sets the given session attribute values

This command sets the specified session attribute values.

Request fields:

  * command (string) => command name: "setAttributes"
  * attributes (object, optional) =>  attributes to set for the connection (see [Attributes](../WebsocketAPIV1.md#attributes-session-and-database-properties))

Request JSON format
```javascript
 {
     "command": "setAttributes",
     "attributes": {
             // as defined separately
     }
 }
```

Response fields:

  * status (string) => command status: "ok" or "error"
  * attributes (object, optional) =>  attributes set for the connection (see [Attributes](../WebsocketAPIV1.md#attributes-session-and-database-properties))
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
     // if status is "error"
     "exception": {
             "text": <string>,
             "sqlCode": <string>
     }
 }
```
