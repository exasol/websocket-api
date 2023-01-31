### enterParallel: Opens subconnections for parallel execution

This command opens subconnections, which are additional connections to
other nodes in the cluster, for the purpose of parallel execution. If
the requested number of subconnections is 0, all open subconnections
are closed.

Request fields:

  * command (string) => command name: "enterParallel"
  * attributes (object, optional) => attributes to set for the connection (see see [Attributes](../WebsocketAPIV1.md#attributes-session-and-database-properties))
  * hostIp (string) => IP address of the Exasol host to which the client is currently connected (i.e., the Exasol host used to create the connection; e.g., ws://\<hostIp\>:8563)
  * numRequestedConnections (number) => number of subconnections to open. If 0, all open subconnections are closed.

Request JSON format
```javascript
 {
     "command": "enterParallel",
     "attributes": {
             // as defined separately
     },
     "hostIp": <string>,
     "numRequestedConnections": <number>
 }
```

Response fields:

  * status (string) => command status: "ok" or "error"
  * responseData (object, optional) => only present if status is "ok"
    * numOpenConnections (number) => number of subconnections actually opened
    * token (number) => token required for the login of subconnections
    * nodes (string[]) => IP addresses and ports of the nodes, to which subconnections may be established
  * exception (object, optional) =>  only present if status is "error"
    * text (string) => exception message which provides error details
    * sqlCode (string) => five-character exception code if known, otherwise "00000"

Response JSON format
```javascript
 {
     "status": <"ok" | "error">,
     // in case of "ok"
     "responseData": {
             "numOpenConnections": <number>,
             "token": <number>,
             "nodes": [
                     <string>
             ]
     },
     // in case of "error"
     "exception": {
             "text": <string>,
             "sqlCode": <string>
     }
 }
```
