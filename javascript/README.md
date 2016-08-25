# Installation

Copy the files `wsapi.js` and `bigint.js` to your webserver or directory, where you can access it.

# Usage

To connect use the `Exasol` object with the connection string, user name and password as the first three arguments. The fourth argument is a function, which is called after successfull connection. The fifth argument is a function whith is called on connection error and ond errors which happens on usage of this object.

```
var exa = new Exasol("ws://127.0.0.1:8563", "sys", "exasol",
                     function (context) {
                         console.log('Connected: ' + context);
                     },
                     function(err) {
                         document.getElementById("result").innerHTML = "ERROR: " + err;
                     });
```

To communicate with the database, use the `com` method, for example to execute a query:
```
exa.com({'command': 'execute', 'sqlText': 'SELECT * FROM cat'},
        function(rep) {
            console.log("OK: " + JSON.stringify(rep));
        }, exa.onerror);
```

The last two arguments are again functions, which are executed on success respective on error whith the result as argument. The error handler, given with in connection is accessible throug `onerror` member variable.

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

For more information about the protocol please reffer the websocket api reference.