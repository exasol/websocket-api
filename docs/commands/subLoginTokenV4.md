### subLoginToken: Establishes a subconnection to Exasol using an OpenID token

This command invokes the login process, which establishes a
subconnection between the client and Exasol. Using subconnections,
the user can interact with Exasol in parallel using various commands.

:warning: This command requires a TLS connection (i.e., `wss://...`).

The login process is composed of four steps:

1. The client sends the `subLoginToken` command including the requested protocol
   version.
   
   Request fields:
     * command (string) => command name: "subLoginToken"
     * protocolVersion (number) => requested WebSocket protocol version, (e.g., 4)
   
   Request JSON format
   ```javascript
    {
        "command": "subLoginToken",
        "protocolVersion": <number>
    }
   ```


2. The server responds with either
     * "ok", in which case the login process continues in step 3, or
     * "error", in which case the login process is aborted.

   Response fields:
     * status (string) => command status: "ok" or "error"
     * exception (object, optional) => only present if status is "error"
       * text (string) => exception message which provides error details
       * sqlCode (string) => five-character exception code if known, otherwise "00000"
   
   Response JSON format
   ```javascript
    {
        "status": <"ok" | "error">,
        // if status is "error"
        "exception": {
                "text": <string>,
                "sqlCode": <string>
        }
    }
   ```
   

3. The client sends either an OpenID `accessToken` or a `refreshToken` and optionally other client information.

   Request fields:
     * accessToken (string, optional) => OpenID access token to use for the login process
     * refreshToken (string, optional) => OpenID refresh token to use for the login process
     * token (number) => token required for subconnection logins (see [requestParallelConnections](requestParallelConnectionsV4.md))
     * sessionId (number) => main connection's session ID (see [login](loginV3.md), [loginToken](loginTokenV3.md))
   
   Request JSON format
   ```javascript
    {
        "accessToken": <string>,
        "refreshToken": <string>,
        "token": <number>,
        "sessionId": <number>
    }
   ```
   
4. The server uses either `accessToken` or `refreshToken` (see 3.) to authenticate the
   user. If successful, the server replies with an
   "ok" response and a subconnection is established. If authentication of
   the user fails, the server sends an "error" response to the client
   indicating that the login process failed and a subconnection could not
   be established.
   
   Response fields:
     * status (string) => command status: "ok" or "error"
     * responseData (object, optional) => only present if status is "ok"
       * sessionId (number) => current session ID
       * protocolVersion (number) => WebSocket protocol version of the connection (e.g., 1)
       * releaseVersion (string) => Exasol version (e.g. "6.0.0")
       * databaseName (string) => database name (e.g., "productionDB1")
       * productName (string) => Exasol product name: "EXASolution"
       * maxDataMessageSize (number) => maximum size of a data message in bytes
       * maxIdentifierLength (number) => maximum length of identifiers
       * maxVarcharLength (number) =>  maximum length of VARCHAR values
       * identifierQuoteString (string) => value of the identifier quote string (e.g., "'")
       * timeZone (string) => name of the session time zone
       * timeZoneBehavior (string) => value of the session option "TIME_ZONE_BEHAVIOR"
     * exception (object, optional) =>  only present if status is "error"
       * text (string) => exception message which provides error details
       * sqlCode (string) => five-character exception code if known, otherwise "00000"
   
   Response JSON format
   ```javascript
    {
        "status": <"ok" | "error">,
        // if status is "ok"
        "responseData": {
                "sessionId": <number>,
                "protocolVersion": <number>,
                "releaseVersion": <string>,
                "databaseName": <string>,
                "productName": <string>,
                "maxDataMessageSize": <number>,
                "maxIdentifierLength": <number>,
                "maxVarcharLength": <number>,
                "identifierQuoteString": <string>,
                "timeZone": <string>,
                "timeZoneBehavior": <string>
        },
        // if status is "error"
        "exception": {
                "text": <string>,
                "sqlCode": <string>
        }
    }
   ```
