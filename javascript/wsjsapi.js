var Exasol = function(url, user, pass, onconnect, onerror) {
    var context = this;
    context.onerror = onerror;
    function isFunction(functionToCheck) {
        var getType = {};
        return functionToCheck && getType.toString.call(functionToCheck) === '[object Function]';
    }
    
    var Queue = function(){
        var queue  = [];
        var offset = 0;
        this.getLength = function() { return (queue.length - offset); }
        this.isEmpty = function() { return (queue.length == 0); }
        this.enqueue = function(item) { queue.push(item); }
        this.peek = function() { return (queue.length > 0 ? queue[offset] : undefined); }
        this.dequeue = function() {
            if (queue.length == 0) return undefined;
            var item = queue[offset];
            if (++ offset * 2 >= queue.length){
                queue  = queue.slice(offset);
                offset = 0;
            }
            return item;
        }
    }
    
    var Base64 = {
        base64: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",
        encode: function($input) {
            if (!$input) {
                return false;
            }
            var $output = "";
            var $chr1, $chr2, $chr3;
            var $enc1, $enc2, $enc3, $enc4;
            var $i = 0;
            do {
                $chr1 = $input.charCodeAt($i++);
                $chr2 = $input.charCodeAt($i++);
                $chr3 = $input.charCodeAt($i++);
                $enc1 = $chr1 >> 2;
                $enc2 = (($chr1 & 3) << 4) | ($chr2 >> 4);
                $enc3 = (($chr2 & 15) << 2) | ($chr3 >> 6);
                $enc4 = $chr3 & 63;
                if (isNaN($chr2)) $enc3 = $enc4 = 64;
                else if (isNaN($chr3)) $enc4 = 64;
                $output += this.base64.charAt($enc1) + this.base64.charAt($enc2) + this.base64.charAt($enc3) + this.base64.charAt($enc4);
            } while ($i < $input.length);
            return $output;
        },
        decode: function($input) {
            if(!$input) return false;
            $input = $input.replace(/[^A-Za-z0-9\+\/\=]/g, "");
            var $output = "";
            var $enc1, $enc2, $enc3, $enc4;
            var $i = 0;
            do {
                $enc1 = this.base64.indexOf($input.charAt($i++));
                $enc2 = this.base64.indexOf($input.charAt($i++));
                $enc3 = this.base64.indexOf($input.charAt($i++));
                $enc4 = this.base64.indexOf($input.charAt($i++));
                $output += String.fromCharCode(($enc1 << 2) | ($enc2 >> 4));
                if ($enc3 != 64) $output += String.fromCharCode((($enc2 & 15) << 4) | ($enc3 >> 2));
                if ($enc4 != 64) $output += String.fromCharCode((($enc3 & 3) << 6) | $enc4);
            } while ($i < $input.length);
            return $output;
        }
    };

    var Hex = {
        hex: "0123456789abcdef",
        encode: function($input) {
            if(!$input) return false;
            var $output = "";
            var $k;
            var $i = 0;
            do {
                $k = $input.charCodeAt($i++);
                $output += this.hex.charAt(($k >> 4) &0xf) + this.hex.charAt($k & 0xf);
            } while ($i < $input.length);
            return $output;
        },
        decode: function($input) {
            if(!$input) return false;
            $input = $input.replace(/[^0-9abcdef]/g, "");
            var $output = "";
            var $i = 0;
            do {
                $output += String.fromCharCode(((this.hex.indexOf($input.charAt($i++)) << 4) & 0xf0) | (this.hex.indexOf($input.charAt($i++)) & 0xf));
            } while ($i < $input.length);
            return $output;
        }
    };
    
    var pw_encode = function(pass, exp, mod) {
        var keysize = 128;
        var data = pass;
        var keyexp = bigInt(exp, 16);
        var keymod = bigInt(mod, 16);

        if(keysize < data.length + 11)
            return null;

        var buffer = "";
        var j = keysize;
        var i = data.length - 1;
        while(i >= 0 && j > 2) { buffer = data.charAt(i--) + buffer; --j; }
        buffer = String.fromCharCode(0) + buffer; --j;
        while(j > 2) { buffer = String.fromCharCode(Math.floor(Math.random()*254) + 1) + buffer; --j; }
        buffer = String.fromCharCode(0) + String.fromCharCode(2) + buffer;
        data = bigInt(Hex.encode(buffer), 16);

        encdata = data.modPow(keyexp, keymod).toString(16);
        while (encdata.length < keysize*2)
            encdata = '0' + encdata;

        return Base64.encode(Hex.decode(encdata));
    };

    context.communicate = function(request, onresponse, onerror) {
        if (!isFunction(onresponse))
            throw "onresponse argument is not a function";
        reqdata = JSON.stringify(request);
        context.connection.onmessage = function(repdata) {
            context.inwork = false;
            try {
                context.connection.onmessage = function(rd) { console.log("Unexpected message: " + rd); };
                console.log('Got response: ' + repdata.data);
                rep = JSON.parse(repdata.data);
                if (rep['status'] == 'ok') {
                    if (rep['exception'] != undefined)
                        throw "Database error [" + rep['exception']['sqlCode'] + "] " + rep['exception']['text'];
                    onresponse(rep['responseData']);
                } else if (rep['status'] == 'error') {
                    throw "Operational error [" + rep['exception']['sqlCode'] + "] " + rep['exception']['text'];
                } else throw "Operational error [" + repdata.data + "]";
            } catch(err) {
                if (isFunction(onerror))
                    onerror(err)
                throw err;
            }
        }
        if (context.inwork == true) {
            if (isFunction(onerror))
                onerror("Connection already in work");
            throw "Connection already in work";
        }
        
        console.log('Send request: ' + reqdata);
        context.inwork = true;
        context.connection.send(reqdata);
    };

    var logedin = function(response) {
        console.log("Successfully connected to the database!");
        onconnect(context);
    };

    var login = function(response) {
        context.publicKey = response['publicKey'];
        context.communicate({"username": user,
                             "password": pw_encode(pass, response['publicKeyExponent'], response['publicKeyModulus']),
                             "clientName": "EXAJS",
                             "driverName": "WS",
                             "clientOs": "Browser",
                             "clientOsUsername": "N/A",
                             "clientVersion": "0.1",
                             "clientRuntime": "Browser"},
                            logedin, context.onerror);
    };

    context.reset = function() {
        context.inwork = false;
        context.connection = new WebSocket(url);
        context.connection.onopen = function () {
            context.communicate({"command": "login", "protocolVersion": 14}, login, context.onerror);
        };
    };

    context.executePrepared = function(statementHandle, onResponse) {
        context.communicate({'command': 'executePreparedStatement',
                             'statementHandle': statementHandle},
                            onResponse, context.onerror);
    };

    context.prepareStatement = function(sqlText, onResponse) {
        context.communicate({'command': 'createPreparedStatement',
                             'sqlText': sqlText},
                            onResponse, context.onerror);
    };

    context.execute = function(sqlText, onResponse) {
        context.communicate({'command': 'execute', 'sqlText': sqlText}, onResponse, context.onerror);
    };
    
    context.fetch = function(res, startPosition, numBytes, onResponse) {
        context.communicate({'command': 'fetch',
                             'resultSetHandle': res.resultSetHandle,
                             'startPosition': startPosition,
                             'numBytes': numBytes},
                            function(rep) {
                                res.data = rep.data;
                                res.dataRows = rep.numRows;
                                onResponse(res);
                            }, context.onerror);
    };
    context.reset();
}

var exa = new Exasol("ws://127.0.0.1:8563", "sys", "exasol", function (context) {
    console.log('Connected: ' + context);
}, function(err) { document.getElementById("result").innerHTML = "ERROR: " + err; });

function printResult(res) {
    var result = "<table>";
    for (i = 0; i < res.dataRows; i++) {
        result += "<tr><th>" + (i+1) + "</th>";
        for (j = 0; j < res.numColumns; j++) {
            result += "<td>" + res.data[j][i] + "</td>";
        }
        result += "</tr>";
    }
    result += "</table>";
    document.getElementById("result").innerHTML = result;
}

function formExecute() {
    sqlText = document.getElementById("query").value;
    document.getElementById("result").innerHTML = "";
    exa.execute(sqlText, function(rep) {
        console.log("OK: " + JSON.stringify(rep));
        if (rep.resultType == 'rowCount') {
            document.getElementById("result").innerHTML = rep.numRows + " rows";
        } else if (rep.resultType == 'resultSet') {
            var res = rep.resultSets[0];
            if (res.data != undefined) {
                res.dataRows = res.numRows;
                printResult(res);
            } else if (res.numRows > 0)
                exa.fetch(res, 0, 500000, printResult);
            else document.getElementById("result").innerHTML = "0 rows";
        } else {
            document.getElementById("result").innerHTML = "Unknown result: " + JSON.stringify(rep);
        }
    });
    return false;
}
