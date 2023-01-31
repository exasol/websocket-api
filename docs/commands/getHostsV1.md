### getHosts: Gets the hosts in a cluster

This command gets the number hosts and the IP address of each host in
an Exasol cluster.

Request fields:

  * command (string) => command name: "getHosts"
  * attributes (object, optional) => attributes to set for the connection (see [Attributes](../WebsocketAPIV1.md#attributes-session-and-database-properties))
  * hostIp (string) => IP address of the Exasol host to which the client is currently connected (i.e., the Exasol host used to create the connection; e.g., ws://\<hostIp\>:8563)

Request JSON format
```javascript
 {
     "command": "getHosts",
     "attributes": {
             // as defined separately
     },
     "hostIp": <string>
 }
```

Response fields:

  * status (string) => command status: "ok" or "error"
  * responseData (object, optional) => only present if status is "ok"
    * numNodes (number) => number of nodes in the cluster
    * nodes (string[]) => array of cluster node IP addresses
  * exception (object, optional) =>  only present if status is "error"
    * text (string) => exception message which provides error
         details
    * sqlCode (string) => five-character exception code if known,
         otherwise "00000"

Response JSON format
```javascript
 {
     "status": <"ok" | "error">,
     // in case of "ok"
     "responseData": {
             "numNodes": <number>,
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
