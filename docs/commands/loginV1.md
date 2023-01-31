### login: Establishes a connection to Exasol

This command invokes the login process which establishes a connection
between the client and Exasol. As long as the connection is open,
the user can interact with Exasol using various commands.

The login process is composed of four steps:

1. The client sends the `login` command including the requested protocol 
   version.
   
     Request fields:

     * command (string) => command name: "login"
     * protocolVersion (number) => requested WebSocket protocol version, (e.g., 1)
     
     Request JSON format
     ```javascript
      {
          "command": "login",
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
   
   
3. The client sends the username, encrypted password, and optionally
   other client information.
   
     Request fields:

     * username (string) => Exasol user name to use for the login process
     * password (string) => user's password, which is encrypted using publicKey (see 2.) and PKCS #1 v1.5 padding, encoded in Base64 format
     * useCompression (boolean) => use compression for messages during the session (beginning after the login process is completed)
     * sessionId (number, optional) => requested session ID
     * clientName (string, optional) => client program name, (e.g., "EXAplus")
     * driverName (string, optional) => driver name, (e.g., "EXA Python")
     * clientOs (string, optional) => name and version of the client operating system
     * clientOsUsername (string, optional) => client's operating system user name
     * clientLanguage (string, optional) => language setting of the client system
     * clientVersion (string, optional) => client version number
     * clientRuntime (string, optional) => name and version of the client runtime
     * attributes (object, optional) => array of attributes to set for the connection (see [Attributes](../WebsocketAPIV1.md#attributes-session-and-database-properties))
     
     Request JSON format
     ```javascript
      {
          "username": <string>,
          "password": <string>,
          "useCompression": <boolean>,
          "sessionId": <number>,
          "clientName": <string>,
          "driverName": <string>,
          "clientOs": <string>,
          "clientOsUsername": <string>,
          "clientLanguage": <string>,
          "clientVersion": <string>,
          "clientRuntime": <string>,
          "attributes": {
                  // as defined separately
          }
      }
     ```
   
4. The server uses `username` and `password` (see 3.) to authenticate the
   user. If successful, the server replies with an "ok" response and a
   connection is established. If authentication of the user fails, the
   server sends an "error" response to the client indicating that the login
   process failed and a connection could not be established.
   
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
