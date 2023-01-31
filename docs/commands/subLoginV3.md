### subLogin: Establishes a subconnection to Exasol

This command invokes the login process, which establishes a
subconnection between the client and Exasol. Using subconnections,
the user can interact with Exasol in parallel using various commands.

ℹ️ A compatibility mode has been added to enable logins using OpenID refresh tokens if using [subLoginToken](subLoginTokenV3.md) is not possible. For details, see step 3.

The login process is composed of four steps:

1. The client sends the `subLogin` command including the requested protocol
   version.
   
     Request fields:
     * command (string) => command name: "subLogin"
     * protocolVersion (number) => requested WebSocket protocol version, (e.g., 1)
     
     Request JSON format
     ```javascript
      {
          "command": "subLogin",
          "protocolVersion": <number>
      }
     ```


2. The server returns a public key which is used to encode the
   user's password. The public key can be obtained in one of two ways:

     - importing the key using the `publicKeyPem` field, or
     - constructing the key using the `publicKeyModulus` and `publicKeyExponent` fields.
     
     Response fields:

     * status (string) => command status: "ok" or "error"
     * responseData (object, optional) => only present if status is "ok"
       * publicKeyPem (string) => PEM-formatted, 1024-bit RSA public key used to encode the user's password (see 3.)
       * publicKeyModulus (string) => hexadecimal modulus of the 1024-bit RSA public key used to encode the user's password (see 3.)
       * publicKeyExponent (string) => hexadecimal exponent of the 1024-bit RSA public key used to encode the user's password (see 3.)
     * exception (object, optional) => only present if status is "error"
       * text (string) => exception message which provides error details
       * sqlCode (string) => five-character exception code if known, otherwise "00000"
     
     Response JSON format
     ```javascript
      {
          "status": <"ok" | "error">,
          // if status is "ok"
          "responseData": {
                  "publicKeyPem": <string>,
                  "publicKeyModulus": <string>,
                  "publicKeyExponent": <string>
          },
          // if status is "error"
          "exception": {
                  "text": <string>,
                  "sqlCode": <string>
          }
      }
     ```
   

3. The client sends the username, encrypted password or OpenID refresh token, and token.

     To use OpenID compatibility mode, substitute the OpenID refresh token for the password.

     Request fields:

     * username (string) => Exasol user name to use for the login process
     * password (string) => user's password or OpenID refresh token, which is encrypted using publicKey (see 2.) and PKCS #1 v1.5 padding, encoded in Base64 format
     * token (number) => token required for subconnection logins (see, [EnterParallel](enterParallelV1.md))
     
     Request JSON format
     ```javascript
      {
          "username": <string>,
          "password": <string>,
          "token": <number>
      }
     ```
   
4. The server uses `username`, `password`, and `token` (see 3.) to
   authenticate the user. If successful, the server replies with an
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
