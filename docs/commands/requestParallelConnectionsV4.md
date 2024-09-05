### requestParallelConnections: Request subconnections for parallel execution
This command requests the use of parallel connections and specifies the maximum number of connections needed. The response will provide the number of parallel connections which were opened and a token which must be used for `subLogin`.

Request fields:
* command (string) => command name: "requestParallelConnections"
* attributes (object, optional) => attributes to set for the connection (see see Attributes)
* numRequestedConnections (number) => number of subconnections to open. If 0, all open subconnections are closed.

Request JSON format
```javascript
{
    "command": "requestParallelConnections",
    "attributes": {
        // as defined separately
    },
    "numRequestedConnections": <number>
}
```

Response fields:
* status (string) => command status: "ok" or "error"
* responseData (object, optional) => only present if status is "ok"
    * numOpenConnections (number) => number of subconnections actually opened
    * token (number) => token required for the login of subconnections
* exception (object, optional) => only present if status is "error"
    * text (string) => exception message which provides error details
    * sqlCode (string) => five-character exception code if known, otherwise "00000"

Response JSON format
```javascript
{
    "status": <"ok" | "error">,
    // in case of "ok"
    "responseData": {
        "numOpenConnections": <number>,
        "token": <number>
    },
    // in case of "error"
    "exception": {
        "text": <string>,
        "sqlCode": <string>
    }
}
```
