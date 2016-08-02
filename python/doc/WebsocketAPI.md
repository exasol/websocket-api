# Short Introduction

The JSON over WebSockets client-server protocol allows customers to
implement their own drivers for all kinds of platforms. The WebSocket
connection can be either encrypted or unencrypted. Encryption will be
added in EXASolution 6.1.

In addition to that, the support of Web Services provides different
useful services like returning static files (e.g., documentation of the
commands including the JSON structure used for communication). By
returning JavaScript that is executed in the browser, the user can
easily execute queries directly within the browser.

In a future version Web Services could also be used to download the
latest drivers.

# Proposition for EXASolution

The WebSocket protocol that will be implemented was standardized by the
IETF as RFC 6455.

## Connection server

The connection server identifies the initial GET request by the client.
This request contains information about the used protocol version.
Depending on this information the matching login and protocol class is
chosen. The established connection can be either encrypted or
unencrypted.

After the handshake the process is identical to a connection using the
standard drivers like JDBC or ODBC: The connection server checks for
incoming messages. In case of metadata requests the connection server
will handle this request without the usage of a sql process (see
[38]Login Improvements). All other requests will be forwarded to a sql
process.

The connection server will also check for requests of static files like
the description of the JSON API or the JavaScript file for query
execution within a browser.

## Sql processes

The reading and writing of the messages is performed by new login and
protocol classes that are used instead of the classes for standard
drivers. All changes for the sql processes are located in these
classes.

## Client side

A native Python driver using this WebSocket client-server protocol will
be implemented.

Furthermore, a JavaScript file can be requested from the connection
server. By executing this in the browser, the user will be able to
execute queries directly within the browser.

# Server JSON API

## WebSocket Protocol v1

WebSocket Protocol v1 requires an EXASolution client/server protocol of
at least v14.

## Login process

### Login: Establish a connection to EXASolution

This command begins the login process, which establishes a connection
between the client and EXASolution. As long as the connection is open,
the user can interact with EXASolution using the commands specified
below.

The login process is composed of four steps:

1. The client sends the server the Login command including the
requested protocol version.

Request fields:
  * command (string) => command name: "login"
  * protocolVersion (number) => requested WebSocket protocol version,
    (e.g., 1)

Request JSON format
```
 {
     "command": "login",
     "protocolVersion": <number>
 }
```


2. The server sends the client a public key which is used to encode the
user's password. The public key can be obtained in one of two ways:
 1. importing the key using the publicKeyPem field
 2. constructing the key using the publicKeyModulus and
    publicKeyExponent fields.

Response fields:
  * status (string) => command status: "ok" or "error"
  * responseData (object, optional) => only present if status is "ok"
       + publicKeyPem (string) => PEM-formatted, 1024-bit RSA public
         key used to encode the user's password (see 3.)
       + publicKeyModulus (string) => Hexadecimal modulus of the
         1024-bit RSA public key used to encode the user's password
         (see 3.)
       + publicKeyExponent (string) => Hexadecimal exponent of the
         1024-bit RSA public key used to encode the user's password
         (see 3.)
  * exception (object, optional) => only present if status is "error"
       + text (string) => exception message which provides error
         details
       + sqlCode (string) => five-character exception code if known,
         otherwise "00000"

Response JSON format
```
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
  * username (string) => EXASolution user name to use for the login
    process
  * password (string) => user's password, which is encrypted using
    publicKey (see 2.) and PKCS #1 v1.5 padding, encoded in Base64
    format
  * useCompression (boolean) => use compression for messages during the
    session (beginning after the login process is completed)
  * sessionId (number, optional) => requested session ID
  * clientName (string, optional) => client program name, (e.g.,
    "EXAplus")
  * driverName (string, optional) => driver name, (e.g., "EXA Python")
  * clientOs (string, optional) => name and version of the client
    operating system
  * clientOsUsername (string, optional) => client's operating system
    user name
  * clientLanguage (string, optional) => language setting of the client
    system
  * clientVersion (string, optional) => client version number
  * clientRuntime (string, optional) => name and version of the client
    runtime
  * attributes (object, optional) => array of attributes to set for the
    connection (see below)

Request JSON format
```
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


4. The server uses username and password (see 3.) to authenticate the
user. If successful, the server sends the client an "ok" response and a
connection is established. If authentication of the user fails, the
server sends the client an "error" response indicating that the login
process failed and a connection is not established.

Response fields:
  * status (string) => command status: "ok" or "error"
  * responseData (object, optional) => only present if status is "ok"
       + sessionId (number) => current session ID
       + protocolVersion (number) => protocol version of the connection
         (e.g., 14)
       + releaseVersion (string) => EXASolution version (e.g. "6.0.0")
       + databaseName (string) => database name (e.g., "productionDB1")
       + productName (string) => EXASolution product name:
         "EXASolution"
       + maxDataMessageSize (number) => maximum size of a data message
         in bytes
       + maxIdentifierLength (number) => maximum length of identifiers
       + maxVarcharLength (number) =>  maximum length of VARCHAR values
       + identifierQuoteString (string) => value of the identifier
         quote string (e.g., "'")
       + timeZone (string) => name of the session time zone
       + timeZoneBehavior (string) => value of the session option
         "TIME_ZONE_BEHAVIOR"
  * exception (object, optional) =>  only present if status is "error"
       + text (string) => exception message which provides error
         details
       + sqlCode (string) => five-character exception code if known,
         otherwise "00000"

Response JSON format
```
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

### SubLogin: Establish a subconnection to EXASolution

This command begins the login process, which establishes a
subconnection between the client and EXASolution. Using subconnections,
the user can interact with EXASolution in parallel using the commands
specified below.

The login process is composed of four steps:

1. The client sends the server the Login command including the
requested protocol version.

Request fields:
  * command (string) => command name: "login"
  * protocolVersion (number) => requested WebSocket protocol version,
    (e.g., 1)

Request JSON format
```
 {
     "command": "subLogin",
     "protocolVersion": <number>
 }
```


2. The server sends the client a public key which is used to encode the
user's password. The public key can be obtained in one of two ways:
 1. importing the key using the publicKeyPem field
 2. constructing the key using the publicKeyModulus and
    publicKeyExponent fields.

Response fields:
  * status (string) => command status: "ok" or "error"
  * responseData (object, optional) => only present if status is "ok"
       + publicKeyPem (string) => PEM-formatted, 1024-bit RSA public
         key used to encode the user's password (see 3.)
       + publicKeyModulus (string) => Hexadecimal modulus of the
         1024-bit RSA public key used to encode the user's password
         (see 3.)
       + publicKeyExponent (string) => Hexadecimal exponent of the
         1024-bit RSA public key used to encode the user's password
         (see 3.)
  * exception (object, optional) => only present if status is "error"
       + text (string) => exception message which provides error
         details
       + sqlCode (string) => five-character exception code if known,
         otherwise "00000"

Response JSON format
```
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


3. The client sends the username, encrypted password, and token.

Request fields:
  * username (string) => EXASolution user name to use for the login
    process
  * password (string) => user's password, which is encrypted using
    publicKey (see 2.) and PKCS #1 v1.5 padding, encoded in Base64
    format
  * token (number) => token required for subconnection logins (see,
    EnterParallel)

Request JSON format
```
 {
     "username": <string>,
     "password": <string>,
     "token": <number>
 }
```

4. The server uses username, password, and token (see 3.) to
authenticate the user. If successful, the server sends the client an
"ok" response and a subconnection is established. If authentication of
the user fails, the server sends the client an "error" response
indicating that the login process failed and a subconnection is not
established.

Response fields:
  * status (string) => command status: "ok" or "error"
  * responseData (object, optional) => only present if status is "ok"
       + sessionId (number) => current session ID
       + protocolVersion (number) => protocol version of the connection
         (e.g., 14)
       + releaseVersion (string) => EXASolution version (e.g. "6.0.0")
       + databaseName (string) => database name (e.g., "productionDB1")
       + productName (string) => EXASolution product name:
         "EXASolution"
       + maxDataMessageSize (number) => maximum size of a data message
         in bytes
       + maxIdentifierLength (number) => maximum length of identifiers
       + maxVarcharLength (number) =>  maximum length of VARCHAR values
       + identifierQuoteString (string) => value of the identifier
         quote string (e.g., "'")
       + timeZone (string) => name of the session time zone
       + timeZoneBehavior (string) => value of the session option
         "TIME_ZONE_BEHAVIOR"
  * exception (object, optional) =>  only present if status is "error"
       + text (string) => exception message which provides error
         details
       + sqlCode (string) => five-character exception code if known,
         otherwise "00000"

Response JSON format
```
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

## Commands

### Disconnect: Close a connection to EXASolution

This command closes the connection between the client and EXASolution.
After the connection is closed, it may no longer be used for further
interaction with EXASolution.

Request fields:
  * command (string) => command name: "disconnect"
  * attributes (object) =>  array of attributes to set for the
    connection (see below)

Request JSON format
```
 {
     "command": "disconnect",
     "attributes": {
             // as defined separately
     }
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * attributes (object) =>  array of set attributes for the connection
    (see below)
  * exception (object, optional) =>  only present if status is "error"
       + text (string) => exception message which provides error
         details
       + sqlCode (string) => five-character exception code if known,
         otherwise "00000"

Reponse JSON format
```
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

### GetAttributes: Gets the requested session attribute values

This command retrieves the values for the specified attributes.

Request fields:
  * command (string) => command name: "getAttributes"
  * attributes (object) =>  array of attributes to set for the
    connection (see below)

JSON format
```
 {
     "command": "getAttributes",
     "attributes": {
             // as defined separately
     },
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * attributes (attribute[]) => array of retrieved attributes (see
    below)
  * exception(object, optional) =>  only present if status is "error"
  *
       + text (string) => exception message which provides error
         details
       + sqlCode (string) => five-character exception code if known,
         otherwise "00000"

Reponse JSON format
```
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

### SetAttributes: Sets the given session attribute values

This command sets the values for the specified attributes.

Request fields:
  * command (string) => command name: "getAttributes"
  * attributes (object) =>  array of attributes to set for the
    connection (see below)

Request JSON format
```
 {
     "command": "setAttributes",
     "attributes": {
             // as defined separately
     }
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * attributes (object) =>  array of set attributes for the connection
    (see below)
  * exception (object, optional) =>  only present if status is "error"
       + text (string) => exception message which provides error
         details
  *
       + sqlCode (string) => five-character exception code if known,
         otherwise "00000"

Response JSON format
```
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

### CreatePreparedStatement: Creates a prepared statement

This command creates a prepared statement.

Request fields:
  * command (string) => command name: "createPreparedStatement"
  * attributes (object) =>  array of attributes to set for the
    connection (see below)
  * sqlText (string) => SQL statement

Request JSON format
```
 {
     "command": "createPreparedStatement",
     "attributes": {
             // as defined separately
     },
     "sqlText": <string>
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * attributes (object) =>  array of set attributes for the connection
    (see below)
  * responseData (object, optional) => only present if status is "ok"
       + statementHandle (number) => prepared statement handle
       + parameterData (object) => prepared statement parameter
         information
            o numColumns (number) => number of columns in columns
            o columns (object[]) => array of column metadata objects
                 # name (string) => column name
                 # dataType (object) => column metadata
                 # type (string) => column data type
                 # precision (number, optional) => column precision
                 # scale (number, optional) => column scale
                 # size (number, optional) => maximum size in bytes of
                   a column value
                 # characterSet (string, optional) => character
                   encoding of a text column
                 # withLocalTimeZone (true | false, optional) =>
                   specifies if a timestamp has a local time zone
                 # fraction (number, optional) => fractional part of
                   number
                 # srid (number, optional) => spatial reference system
                   identifier
       + type (string) => type of result: "resultSet" or "rowCount"
       + rowCount (number, optional) => present if type is "rowCount",
         number of rows
       + resultSets (object[]) => present if type is "resultSet", array
         of result sets
            o resultSetHandle (number) => result set handle
            o numColumns (number) => number of columns in the result
              set
            o numRows (number) => number of rows in the result set
            o numRowsInMessage (number) => number of rows in the
              current message
            o columns (object[]) => array of column metadata objects
                 # name (string) => column name
                 # dataType (object) => column metadata
                      @ type (string) => column data type
                      @ precision (number, optional) => column
                        precision
                      @ scale (number, optional) => column scale
                      @ size (number, optional) => maximum size in
                        bytes of a column value
                      @ characterSet (string, optional) => character
                        encoding of a text column
                      @ withLocalTimeZone (true | false, optional) =>
                        specifies if a timestamp has a local time zone
                      @ fraction (number, optional) => fractional part
                        of number
                      @ srid (number, optional) => spatial reference
                        system identifier
  * exception (object, optional) =>  only present if status is "error"
       + text (string) => exception message which provides error
         details
       + sqlCode (string) => five-character exception code if known,
         otherwise "00000"

Response JSON format
```
 {
     "status": <"ok" | "error">,
     "attributes": {
             // as defined separately
     },
     // if status is "ok"
     "responseData": {
             "statementHandle": <number>,
             "parameterData": {
                     "numColumns": <number>,
                     "columns": [ {
                             "name": <string>,
                             "dataType": {
                                     "type": <string>,
                                     "precision": <number>,
                                     "scale": <number>,
                                     "size": <number>,
                                     "characterSet": <number>,
                                     "withLocalTimeZone": <true | false>,
                                     "fraction": <number>,
                                     "srid": <number>
                             }
                     } ]
             },
             "resultType": <"resultSet" | "rowCount">,
             // if type is "rowCount"
             "rowCount": <number>,
             // if type is "resultSet"
             "resultSets": [ {
                     "resultSetHandle": <number>,
                     "numColumns": <number>,
                     "numRows": <number>,
                     "numRowsInMessage": <number>,
                     "columns": [ {
                             "name": <string>,
                             "dataType": {
                                     "type": <string>,
                                     "precision": <number>,
                                     "scale": <number>,
                                     "size": <number>,
                                     "characterSet": <number>,
                                     "withLocalTimeZone": <true | false>,
                                     "fraction": <number>,
                                     "srid": <number>
                             }
                     } ]
             } ],
     },
     // if status is "error"
     "exception": {
             "text": <string>,
             "sqlCode": <string>
     }
 }
```

### ExecutePreparedStatement: Executes a prepared statement

This command executes a prepared statement, which has already been
created.

Request fields:
  * command (string) => command name: "executePreparedStatement"
  * attributes (object) =>  array of attributes to set for the
    connection (see below)
  * statementHandle (number) => prepared statement handle
  * numColumns (number) => number of columns in data
  * numRows (number) => number of rows in data
  * columns (object[]) => array of column metadata objects
       + name (string) => column name
       + dataType (object) => column metadata
            o type (string) => column data type
            o precision (number, optional) => column precision
            o scale (number, optional) => column scale
            o size (number, optional) => maximum size in bytes of a
              column value
            o characterSet (string, optional) => character encoding of
              a text column
            o withLocalTimeZone (true | false, optional) => specifies
              if a timestamp has a local time zone
            o fraction (number, optional) => fractional part of number
            o srid (number, optional) => spatial reference system
              identifier
  * data (array[]) => object containing the data for the prepared
    statement in column-major order

Request JSON format
```
 {
    "command": "executePreparedStatement",
    "attributes": {
        // as defined separately
    },
    "statementHandle": <number>,
    "numColumns": <number>,
    "numRows": <number>,
    "columns": [ {
        "name": <string>,
        "dataType": {
            "type": <string>,
            "precision": <number>,
            "scale": <number>,
            "size": <number>,
            "characterSet": <number>,
            "withLocalTimeZone": <boolean>,
            "fraction": <number>,
            "srid": <number>
        }
    } ],
    "data": [ [ <string | number | true | false | null> ] ]
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * attributes (object) =>  array of set attributes for the connection
    (see below)
  * responseData (object, optional) => only present if status is "ok"
       + type (string) => type of result: "resultSet" or "rowCount"
       + rowCount (number, optional) => present if type is "rowCount",
         number of rows
       + resultSets (object[]) => present if type is "resultSet", array
         of result sets
            o resultSetHandle (number) => result set handle
            o numColumns (number) => number of columns in the result
              set
            o numRows (number) => number of rows in the result set
            o numRowsInMessage (number) => number of rows in the
              current message
            o columns (object[]) => array of column metadata objects
                 # name (string) => column name
                 # dataType (object) => column metadata
                      @ type (string) => column data type
                      @ precision (number, optional) => column
                        precision
                      @ scale (number, optional) => column scale
                      @ size (number, optional) => maximum size in
                        bytes of a column value
                      @ characterSet (string, optional) => character
                        encoding of a text column
                      @ withLocalTimeZone (true | false, optional) =>
                        specifies if a timestamp has a local time zone
                      @ fraction (number, optional) => fractional part
                        of number
                      @ srid (number, optional) => spatial reference
                        system identifier
            o data (array[]) => object containing the data for the
              prepared statement in column-major order
  * exception (object, optional) =>  only present if status is "error"
       + text (string) => exception message which provides error
         details
       + sqlCode (string) => five-character exception code if known,
         otherwise "00000"

Response JSON format
```
 {
     "status": <"ok" | "error">,
     "attributes": {
         // as defined separately
     },
     // in case of "ok"
     "responseData": {
         "resultType": <"resultSet" | "rowCount">,
                 // if type is "rowCount"
         "rowCount": <number>,
                 // if type is "resultSet"
         "resultSets": [ {
             "resultSetHandle": <number>,
             "numColumns": <number>,
             "numRows": <number>,
             "numRowsInMessage": <number>,
             "columns": [ {
                 "name": <string>,
                 "dataType": {
                     "type": <string>,
                     "precision": <number>,
                     "scale": <number>,
                     "size": <number>,
                     "characterSet": <number>,
                     "withLocalTimeZone": <boolean>,
                     "fraction": <number>,
                     "srid": <number>
                 }
             } ],
             "data": [
                 [ <string | number | true | false | null> ]
             ]
         } ]
     },
     // in case of "error"
     "exception": {
         "text": <string>,
         "sqlCode": <string>
     }
 }
```

### ClosePreparedStatement: Closes a prepared statement

This command closes a prepared statement, which has already been
created.

Request fields:
  * command (string) => command name: "closePreparedStatement"
  * attributes (object) =>  array of attributes to set for the
    connection (see below)
  * statementHandle (number) => prepared statement handle

Request JSON format
```
 {
     "command": "closePreparedStatement",
     "attributes": {
             // as defined separately
     },
     "statementHandle": <number>
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * attributes (object) =>  array of set attributes for the connection
    (see below)
  * exception (object, optional) =>  only present if status is "error"
       + text (string) => exception message which provides error
         details
       + sqlCode (string) => five-character exception code if known,
         otherwise "00000"

Response JSON format
```
 {
     "status": <"ok" | "error">,
     "attributes": {
             // as defined separately
     },
     // in case of "error"
     "exception": {
             "text": <string>,
             "sqlCode": <string>
     }
 }
```

### Execute: Executes an SQL statement

This command executes an SQL statement.

Request fields:
  * command (string) => command name: "executePreparedStatement"
  * attributes (object) =>  array of attributes to set for the
    connection (see below)
  * sqlText (string) => SQL statement to execute

Request JSON format
```
 {
     "command": "execute",
     "attributes": {
             // as defined separately
     },
     "sqlText": <string>
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * attributes (object) =>  array of set attributes for the connection
    (see below)
  * responseData (object, optional) => only present if status is "ok"
       + type (string) => type of result: "resultSet" or "rowCount"
       + rowCount (number, optional) => present if type is "rowCount",
         number of rows
       + resultSets (object[]) => present if type is "resultSet", array
         of result sets
            o resultSetHandle (number) => result set handle
            o numColumns (number) => number of columns in the result
              set
            o numRows (number) => number of rows in the result set
            o numRowsInMessage (number) => number of rows in the
              current message
            o columns (object[]) => array of column metadata objects
                 # name (string) => column name
                 # dataType (object) => column metadata
                      @ type (string) => column data type
                      @ precision (number, optional) => column
                        precision
                      @ scale (number, optional) => column scale
                      @ size (number, optional) => maximum size in
                        bytes of a column value
                      @ characterSet (string, optional) => character
                        encoding of a text column
                      @ withLocalTimeZone (true | false, optional) =>
                        specifies if a timestamp has a local time zone
                      @ fraction (number, optional) => fractional part
                        of number
                      @ srid (number, optional) => spatial reference
                        system identifier
            o data (array[]) =>object containing the data for the
              prepared statement in column-major order
  * exception (object, optional) =>  only present if status is "error"
       + text (string) => exception message which provides error
         details
       + sqlCode (string) => five-character exception code if known,
         otherwise "00000"

Response JSON format
```
 {
     "status": <"ok" | "error">,
     "attributes": {
             // as defined separately
     },
     // in case of "ok"
     "responseData": { // Optional: ok
             "resultType": <"resultSet" | "rowCount">,
             // if type is "rowCount"
             "rowCount": <number>,
             // if type is "resultSet"
             "resultSets": [ {
                     "resultSetHandle": <number>,
                     "numColumns": <number>,
                     "numRows": <number>,
                     "numRowsInMessage": <number>,
                     "columns": [ {
                             "name": <string>,
                             "dataType": {
                                     "type": <string>,
                                     "precision": <number>,
                                     "scale": <number>,
                                     "size": <number>,
                                     "characterSet": <number>,
                                     "withLocalTimeZone": <boolean>,
                                     "fraction": <number>,
                                     "srid": <number>
                             }
                     } ],
                     "data": [ [ <string | number | true | false | null> ] ]
             } ]
     },
     // in case of "error"
     "exception": {
             "text": <string>,
             "sqlCode": <string>
     }
 }
```

### Fetch: Retrieves data

This command retrieves data.

Request fields:
  * command (string) => command name: "fetch"
  * attributes (object) =>  array of attributes to set for the
    connection (see below)
  * resultSetHandle (number) => result set handle
  * startPosition (number) => offset (in bytes) from which to begin
    data retrieval
  * numBytes (number) => number of bytes to retrieve

Request JSON format
```
 {
     "command": "fetch",
     "attributes": {
             // as defined separately
     },
     "resultSetHandle": <number>,
     "startPosition": <number>,
     "numBytes": <number>
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * responseData (object, optional) => only present if status is "ok"
       + numRows (number) => number of rows in the result set
       + data (array[]) => object containing the data for the prepared
         statement in column-major order
  * exception (object, optional) =>  only present if status is "error"
       + text (string) => exception message which provides error
         details
       + sqlCode (string) => five-character exception code if known,
         otherwise "00000"

Response JSON format
```
 {
     "status": <"ok" | "error">,
     // in case of "ok"
     "responseData": {
             "numRows": <number>,
             "data": [ [ <string | number | true | false | null> ] ]
     },
     // in case of "error"
     "exception": {
             "text": <string>,
             "sqlCode": <string>
     }
 }
```

### CloseResultSet: Closes a result set

This command closes result sets.

Request fields:
  * command (string) => command name: "closeResultSet"
  * attributes (object) =>  array of attributes to set for the
    connection (see below)
  * resultSetHandles (number[]) => array of result set handles

Request JSON format
```
 {
     "command": "closeResultSet",
     "attributes": {
             // as defined separately
     },
     "resultSetHandles": [ <number> ]
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * exception (object, optional) =>  only present if status is "error"
       + text (string) => exception message which provides error
         details
       + sqlCode (string) => five-character exception code if known,
         otherwise "00000"

Response JSON format
```
 {
     "status": <"ok" | "error">,
     // in case of "error"
     "exception": { // Optional: error
             "text": <string>, // Exception text
             "sqlCode": <string> // Five-character exception code if known, otherwise "00000"
     }
 }
```

### GetHosts: Gets the hosts in a cluster

This command gets the number hosts and the IP address of each host in
an EXASolution cluster.

Request fields:
  * command (string) => command name: "getHosts"
  * attributes (object) =>  array of attributes to set for the
    connection (see below)

Request JSON format
```
 {
     "command": "getHosts",
     "attributes": {
             // as defined separately
     }
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * responseData (object, optional) => only present if status is "ok"
       + numNodes (number) => number of nodes in the cluster
       + nodes (string[]) => array of cluster node IP addresses
  * exception (object, optional) =>  only present if status is "error"
       + text (string) => exception message which provides error
         details
       + sqlCode (string) => five-character exception code if known,
         otherwise "00000"

Response JSON format
```
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

### ExecuteBatch: Executes multiple SQL statements as a batch

This command executes multiple SQL statements sequentially as a batch.

Request fields:
  * command (string) => command name: "executeBatch"
  * attributes (object) =>  array of attributes to set for the
    connection (see below)
  * sqlTexts (string[]) => array of SQL statement to execute

Request JSON format
```
 {
     "command": "executeBatch",
     "attributes": {
             // as defined separately
     },
     "sqlTexts": [
             <string>
     ]
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * attributes (object) =>  array of set attributes for the connection
    (see below)
  * responseData (object, optional) => only present if status is "ok"
       + type (string) => type of result: "resultSet" or "rowCount"
       + rowCount (number, optional) => present if type is "rowCount",
         number of rows
       + resultSets (object[]) => present if type is "resultSet", array
         of result sets
            o resultSetHandle (number) => result set handle
            o numColumns (number) => number of columns in the result
              set
            o numRows (number) => number of rows in the result set
            o numRowsInMessage (number) => number of rows in the
              current message
            o columns (object[]) => array of column metadata objects
                 # name (string) => column name
                 # dataType (object) => column metadata
                      @ type (string) => column data type
                      @ precision (number, optional) => column
                        precision
                      @ scale (number, optional) => column scale
                      @ size (number, optional) => maximum size in
                        bytes of a column value
                      @ characterSet (string, optional) => character
                        encoding of a text column
                      @ withLocalTimeZone (true | false, optional) =>
                        specifies if a timestamp has a local time zone
                      @ fraction (number, optional) => fractional part
                        of number
                      @ srid (number, optional) => spatial reference
                        system identifier
            o data (array[]) => object containing the data for the
              prepared statement in column-major order
  * exception (object, optional) =>  only present if status is "error"
       + text (string) => exception message which provides error
         details
       + sqlCode (string) => five-character exception code if known,
         otherwise "00000"

Response JSON format
```
 {
     "status": <"ok" | "error">,
     "attributes": {
         // as defined separately
     },
     // in case of "ok"
     "responseData": {
         "resultType": <"resultSet" | "rowCount">,
                 // if type is "rowCount"
         "rowCount": <number>,
                 // if type is "resultSet"
         "resultSets": [ {
             "resultSetHandle": <number>,
             "numColumns": <number>,
             "numRows": <number>,
             "numRowsInMessage": <number>,
             "columns": [ {
                 "name": <string>,
                 "dataType": {
                     "type": <string>,
                     "precision": <number>,
                     "scale": <number>,
                     "size": <number>,
                     "characterSet": <number>,
                     "withLocalTimeZone": <boolean>,
                     "fraction": <number>,
                     "srid": <number>
                 }
             } ],
             "data": [ [ <string | number | true | false | null> ] ]
         } ]
     },
     // in case of "error"
     "exception": {
         "text": <string>,
         "sqlCode": <string>
     }
 }
```

### EnterParallel: Opens subconnections for parallel execution

This command opens subconnections, which are additional connections to
other nodes in the cluster, for the purpose of parallel execution. If
the requested number of subconnections is 0, all open subconnections
are closed.

Request fields:
  * command (string) => command name: "enterParallel"
  * attributes (object) =>  array of attributes to set for the
    connection (see below)
  * numRequestedConnections (number) => number of subconnections to
    open. If 0, all open subconnections are closed.

Request JSON format
```
 {
     "command": "enterParallel",
     "attributes": {
             // as defined separately
     },
     "numRequestedConnections": <number>
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * responseData (object, optional) => only present if status is "ok"
       + numOpenConnections (number) => number of subconnections
         actually opened
       + token (number) => token required for the login of
         subconnections
       + nodes (string[]) => IP addresses and ports of the nodes, to
         which subconnections may be established
  * exception (object, optional) =>  only present if status is "error"
       + text (string) => exception message which provides error
         details
       + sqlCode (string) => five-character exception code if known,
         otherwise "00000"

Response JSON format
```
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

### GetResultSetHeader: Gets a result set header

This command retrieves a header (i.e., empty result set) which contains
the metadata for an open result set.

Request fields:
  * command (string) => command name: "getResultSetHeader"
  * attributes (object) =>  array of attributes to set for the
    connection (see below)
  * resultSetHandles (number[]) => array of open result set handles

Request JSON format
```
 {
     "command": "getResultSetHeader",
     "attributes": {
             // as defined separately
     },
     "resultSetHandles": [
         <number>
     ]
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * attributes (object) =>  array of set attributes for the connection
    (see below)
  * responseData (object, optional) => only present if status is "ok"
       + type (string) => type of result: "resultSet"
       + resultSets (object[]) => present if type is "resultSet", array
         of result sets
            o resultSetHandle (number) => result set handle
            o numColumns (number) => number of columns in the result
              set
            o numRows (number) => number of rows in the result set
            o numRowsInMessage (number) => number of rows in the
              current message
            o columns (object[]) => array of column metadata objects
                 # name (string) => column name
                 # dataType (object) => column metadata
                      @ type (string) => column data type
                      @ precision (number, optional) => column
                        precision
                      @ scale (number, optional) => column scale
                      @ size (number, optional) => maximum size in
                        bytes of a column value
                      @ characterSet (string, optional) => character
                        encoding of a text column
                      @ withLocalTimeZone (true | false, optional) =>
                        specifies if a timestamp has a local time zone
                      @ fraction (number, optional) => fractional part
                        of number
                      @ srid (number, optional) => spatial reference
                        system identifier
  * exception (object, optional) =>  only present if status is "error"
       + text (string) => exception message which provides error
         details
       + sqlCode (string) => five-character exception code if known,
         otherwise "00000"

Response JSON format
```
 {
     "status": <"ok" | "error">,
     "attributes": {
         // as defined separately
     },
     // in case of "ok"
     "responseData": {
         "resultType": "resultSet",
         "resultSets": [ {
             "resultSetHandle": <number>,
             "numColumns": <number>,
             "numRows": <number>,
             "numRowsInMessage": <number>,
             "columns": [ {
                 "name": <string>,
                 "dataType": {
                     "type": <string>,
                     "precision": <number>,
                     "scale": <number>,
                     "size": <number>,
                     "characterSet": <number>,
                     "withLocalTimeZone": <boolean>,
                     "fraction": <number>,
                     "srid": <number>
                 }
             } ]
         } ]
     },
     // in case of "error"
     "exception": {
         "text": <string>,
         "sqlCode": <string>
     }
 }
```

### GetOffset: Gets the row offset of a result set

This command retrieves the row offset of the result set of this
(sub)connection. This is the row number of the first row of the current
(sub)connection's result set in the global result set.

Request fields:
  * command (string) => command name: "getOffset"
  * attributes (object) =>  array of attributes to set for the
    connection (see below)
  * resultSetHandle (number) => open result set handle

Request JSON format
```
 {
     "command": "getOffset",
     "attributes": {
             // as defined separately
     },
     "resultSetHandle": <number>
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * responseData (object, optional) => only present if status is "ok"
       + rowOffset (number) => row offset of connection's result set
  * exception (object, optional) =>  only present if status is "error"
       + text (string) => exception message which provides error
         details
       + sqlCode (string) => five-character exception code if known,
         otherwise "00000"

Response JSON format
```
 {
     "status": <"ok" | "error">,
     // in case of "ok"
     "responseData": {
             "rowOffset": <number>
     },
     // in case of "error"
     "exception": {
             "text": <string>,
             "sqlCode": <string>
     }
 }
```

### AbortQuery: Aborts a running query

This command aborts a running query. It does not have a response.

Request fields:
  * command (string) => command name: "abortQuery"

Request JSON format
```
 {
     "command": "abortQuery"
 }
```

### GetStatus: Gets the status of a query

This command get the status of a running query. If the attribute
"feedbackInterval" is set, this response will also be sent to the
client during command execution.

Request fields:
  * command (string) => command name: "getStatus"

Request JSON format
```
 {
     "command": "getStatus"
 }
```

Response fields:
  * status (string) => command status: "ok" or "error"
  * responseData (object, optional) => only present if status is "ok"
       + status (string) => status of the query
  * exception (object, optional) =>  only present if status is "error"
       + text (string) => exception message which provides error
         details
       + sqlCode (string) => five-character exception code if known,
         otherwise "00000"

Response JSON format
```
 {
     "status": <"ok" | "error">,
     // in case of "ok"
     "responseData": {
             "status": <string>
     },
     // in case of "error"
     "exception": {
             "text": <string>,
             "sqlCode": <string>
     }
 }
```

## Attributes

### Attributes: Session and database properties

Attributes can be queried with the GetAttributes command and some of
them can be modified with the SetAttributes command. Modified
attributes are included in command replies.

Name JSON value Read-only Committable Description
autocommit true | false no no If true, commit() will be executed
automatically after each statement. If false, commit() and rollback()
must be executed manually.
compressionEnabled true | false yes no If true, the WebSocket data
frame payload data is compressed. If false, it is not compressed.
currentSchema string no yes Current schema name
dateFormat string yes yes Date format
dateLanguage string yes yes Language used for the day and month of
dates.
datetimeFormat string yes yes Timestamp format
defaultLikeEscapeCharacter string yes yes Escape character in LIKE
expressions.
feedbackInterval number no no Time interval (in seconds) specifying how
often heartbeat/feedback packets are sent to the client during query
execution.
numericCharacters string no yes Characters specifying the group and
decimal separators (NLS_NUMERIC_CHARACTERS). For example, ",." would
result in "123,456,789.123".
openTransaction true | false yes no If true, a transaction is open. If
false, a transaction is not open.
queryTimeout number no yes Query timeout value (in seconds). If a query
runs longer than the specified time, it will be aborted.
snapshotTransactionsEnabled true | false no no If true, snapshot
transactions will be used. If false, they will not be used.
timestampUtcEnabled true | false no no If true, timestamps will be
converted to UTC. If false, UTC will not be used.
timezone string yes yes Timezone of the session.
timeZoneBehavior string yes yes Specifies the conversion behavior of
UTC timestamps to local timestamps when the time value occurs during a
time shift because of daylight saving time (TIME_ZONE_BEHAVIOR).

Attribute JSON format
```
 {
     "name": <string>,
     "value": <string | number | true | false>
 }
```

## Data Types

### Data Types: Type names and properties

The following data types and properties can be used to specify column
types in the executePreparedStatement request.

```
                Type              Required Properties Optional Properties
   BOOLEAN
   CHAR                           size
   DATE
   DECIMAL                        precision, scale
   DOUBLE
   GEOMETRY
   INTERVAL DAY TO SECOND         precision, fraction
   INTERVAL YEAR TO MONTH         precision
   TIMESTAMP                                          withLocalTimeZone
   TIMESTAMP WITH LOCAL TIME ZONE                     withLocalTimeZone
   VARCHAR                        size
```


The following data types and properties are used to specify column
types in responses from EXASolution.

```
                Type                     Properties
   BOOLEAN
   CHAR                           size, characterSet
   DATE                           size
   DECIMAL                        precision, scale
   DOUBLE
   GEOMETRY                       size, srid
   INTERVAL DAY TO SECOND         size, precision, fraction
   INTERVAL YEAR TO MONTH         size, precision
   TIMESTAMP                      size, withLocalTimeZone
   TIMESTAMP WITH LOCAL TIME ZONE size, withLocalTimeZone
   VARCHAR                        size, characterSet
```

## Compression

The data in the WebSocket data frames may be compressed using zlib. In
order to enable compression, the client must set the useCompression
field in the login command to true. If compression is enabled during
login, all messages sent and received after login completion must be
binary data frames, in which the payload data (i.e., command
request/response) is zlib compressed.

## Heartbeat/Feedback Messages

The feedbackInterval session attribute specifies how often (in seconds)
unidirectional heartbeat/feedback messages are sent to the client
during query execution. These messages are sent using Pong WebSocket
control frames (see RFC 6455), and thus a response is not expected.

The client may send Ping WebSocket control frames (see RFC 6455) to
EXASolution, for example, as client-initiated keepalives. EXASolution
will respond to a Ping frame with a Pong response.

EXASolution will not send Ping frames to the client.

## Server Web Interface

A simple Web interface will also be provided, which will allow
customers to easily access EXASolution. Using their browsers they
could, for example, execute queries, access product information and
documentation, and download the latest drivers directly from
EXASolution.

The Web interface can be accessed by simply pointing a browser to
EXASolution's URL: http://<exa-ip>:8563

The customer is then presented with a simple Web page, on which they
can perform certain actions (TBD).
size, withLocalTimeZone
