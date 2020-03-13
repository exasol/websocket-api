### getAttributes: Gets the session attribute values

This command retrieves the session attribute values.

Request fields:
  * command (string) => command name: "getAttributes"
  * attributes (object, optional) => attributes to set for the connection (see below)

JSON format
```javascript
 {
     "command": "getAttributes",
     "attributes": {
             // as defined separately
     },
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * attributes (object, optional) => attributes set for the connection (see below)
  * exception(object, optional) =>  only present if status is "error"
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
