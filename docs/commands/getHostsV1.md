### getHosts: Gets the hosts in a cluster

This command gets the number hosts and the IP address of each host in
an Exasol cluster.

:warning: This command was designed to be used for creating subconnections using [enterParallel](enterParallelV1.md) which has been deprecated. The IP addresses returned by this command may not be correct if the prerequisites for subconnections using [enterParallel](enterParallelV1.md) are not fulfilled. Namely, the private and public IP addresses of the database must have a uniform distance between all active nodes. For example, a database with the IP addresses 192.168.56.101, 192.168.56.102, 192.168.56.103 fulfills this requirement because the distance between nodes is 1. A database with the IP addresses 192.168.56.101, 192.168.56.105, 192.168.56.106 does not fulfill this requirement, because the distance between nodes is not uniform (in this case, it is 4 and 1, respectively).

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
