# Introduction

This is a protoype implementation of a web client for EXASOL which uses the EXASOL WebSocket protocol API with JSON as the serialization format.

# Web Interface Usage

A recent or similar version of this code is already included with EXASOL 6.0. It may be updated from time to time in future versions.

To access the web interface, simply enter the following URL into the web browser: `http://<exa-host>:8563/console.html`.

Note: HTTPS is currently unsupported.

# Code Usage

To connect, use the `Exasol` object with the connection string, user name and password as the first three arguments. The fourth argument is a function, which is called after the connection has been successfully established. The fifth argument is a function which is called on connection error and on errors related to the usage of this object.

```
var exa = new Exasol("ws://127.0.0.1:8563", "sys", "exasol",
                     function (context) {
                         console.log('Connected: ' + context);
                     },
                     function(err) {
                         document.getElementById("result").innerHTML = "ERROR: " + err;
                     });
```

To communicate with the database, use the `com` method. For example, to execute a query:
```
exa.com({'command': 'execute', 'sqlText': 'SELECT * FROM cat'},
        function(rep) {
            console.log("OK: " + JSON.stringify(rep));
        }, exa.onerror);
```

The last two arguments are again functions, which are executed on success or on error with the result as the argument. The error handler, given with the connection, is accessible through the `onerror` member variable.

To fetch the data, you can use integrated fetch method `com` method or the shorter `fetch` method:
```
exa.com({'command': 'execute', 'sqlText': 'SELECT * FROM cat'},
        function(rep) {
            exa.fetch(rep['results'][0].resultSet, 0, 500000,
                      function (res) {
                          console.log("OK: " + JSON.stringify(res));
                      });
        }, exa.onerror);
```

For more information about the protocol, please refer to the WebSocket API reference.
