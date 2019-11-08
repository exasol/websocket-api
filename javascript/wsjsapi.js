// npm i jsbn
// npm i ws

jsbn = require('jsbn');
WebSocket = require('ws');

var debug = false

var json_parse = (function () {
    "use strict";

    // We are defining the function inside of another function to avoid creating
    // global variables.

    var at;     // The index of the current character
    var ch;     // The current character
    var escapee = {
        "\"": "\"",
        "\\": "\\",
        "/": "/",
        b: "\b",
        f: "\f",
        n: "\n",
        r: "\r",
        t: "\t"
    };
    var text;

    var error = function (m) {

        // Call error when something is wrong.
        throw {
            name: "SyntaxError",
            message: m,
            at: at,
            text: text
        };
    };

    var next = function (c) {

        // If a c parameter is provided, verify that it matches the current character.
        if (c && c !== ch) {
            error("Expected '" + c + "' instead of '" + ch + "'");
        }

        // Get the next character. When there are no more characters,
        // return the empty string.

        ch = text.charAt(at);
        at += 1;
        return ch;
    };

    var number = function () {

        // Parse a number value.

        //var value;
        var string = "";

        if (ch === "-") {
            string = "-";
            next("-");
        }
        while (ch >= "0" && ch <= "9") {
            string += ch;
            next();
        }
        if (ch === ".") {
            string += ".";
            while (next() && ch >= "0" && ch <= "9") {
                string += ch;
            }
        }
        if (ch === "e" || ch === "E") {
            string += ch;
            next();
            if (ch === "-" || ch === "+") {
                string += ch;
                next();
            }
            while (ch >= "0" && ch <= "9") {
                string += ch;
                next();
            }
        }
//        value = +string;
//        if (!isFinite(value)) {
//            error("Bad number");
//        } else {
//            return value;
//        }
        return string;
    };

    var string = function () {

        // Parse a string value.

        var hex;
        var i;
        var value = "";
        var uffff;

        // When parsing for string values, we must look for " and \ characters.

        if (ch === "\"") {
            while (next()) {
                if (ch === "\"") {
                    next();
                    return value;
                }
                if (ch === "\\") {
                    next();
                    if (ch === "u") {
                        uffff = 0;
                        for (i = 0; i < 4; i += 1) {
                            hex = parseInt(next(), 16);
                            if (!isFinite(hex)) {
                                break;
                            }
                            uffff = uffff * 16 + hex;
                        }
                        value += String.fromCharCode(uffff);
                    } else if (typeof escapee[ch] === "string") {
                        value += escapee[ch];
                    } else {
                        break;
                    }
                } else {
                    value += ch;
                }
            }
        }
        error("Bad string");
    };

    var white = function () {

        // Skip whitespace.

        while (ch && ch <= " ") {
            next();
        }
    };

    var word = function () {

        // true, false, or null.

        switch (ch) {
        case "t":
            next("t");
            next("r");
            next("u");
            next("e");
            return true;
        case "f":
            next("f");
            next("a");
            next("l");
            next("s");
            next("e");
            return false;
        case "n":
            next("n");
            next("u");
            next("l");
            next("l");
            return null;
        }
        error("Unexpected '" + ch + "'");
    };

    var value;  // Place holder for the value function.

    var array = function () {

        // Parse an array value.

        var arr = [];

        if (ch === "[") {
            next("[");
            white();
            if (ch === "]") {
                next("]");
                return arr;   // empty array
            }
            while (ch) {
                arr.push(value());
                white();
                if (ch === "]") {
                    next("]");
                    return arr;
                }
                next(",");
                white();
            }
        }
        error("Bad array");
    };

    var object = function () {

        // Parse an object value.

        var key;
        var obj = {};

        if (ch === "{") {
            next("{");
            white();
            if (ch === "}") {
                next("}");
                return obj;   // empty object
            }
            while (ch) {
                key = string();
                white();
                next(":");
                if (Object.hasOwnProperty.call(obj, key)) {
                    error("Duplicate key '" + key + "'");
                }
                obj[key] = value();
                white();
                if (ch === "}") {
                    next("}");
                    return obj;
                }
                next(",");
                white();
            }
        }
        error("Bad object");
    };

    value = function () {

        // Parse a JSON value. It could be an object, an array, a string, a number,
        // or a word.

        white();
        switch (ch) {
        case "{":
            return object();
        case "[":
            return array();
        case "\"":
            return string();
        case "-":
            return number();
        default:
            return (ch >= "0" && ch <= "9")
                ? number()
                : word();
        }
    };

        // Return the json_parse function. It will have access to all of the above
        // functions and variables.

    return function (source, reviver) {
        var result;

        text = source;
        at = 0;
        ch = " ";
        result = value();
        white();
        if (ch) {
            error("Syntax error");
        }

        // If there is a reviver function, we recursively walk the new structure,
        // passing each name/value pair to the reviver function for possible
        // transformation, starting with a temporary root object that holds the result
        // in an empty key. If there is not a reviver function, we simply return the
        // result.

        return (typeof reviver === "function")
            ? (function walk(holder, key) {
                var k;
                var v;
                var val = holder[key];
                if (val && typeof val === "object") {
                    for (k in val) {
                        if (Object.prototype.hasOwnProperty.call(val, k)) {
                            v = walk(val, k);
                            if (v !== undefined) {
                                val[k] = v;
                            } else {
                                delete val[k];
                            }
                        }
                    }
                }
                return reviver.call(holder, key, val);
            }({"": result}, ""))
            : result;
    };
}());

module.exports = {
 Exasol : function(url, user, pass, onconnect, onerror) {
    var context = this;
    context.onerror = onerror;
    context.sessionId = "-1";

    var BigInteger = jsbn.BigInteger;

    function isFunction(functionToCheck) {
        var getType = {};
        return functionToCheck && getType.toString.call(functionToCheck) === '[object Function]';
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
                $output = $output
                    + this.base64.charAt($enc1)
                    + this.base64.charAt($enc2)
                    + this.base64.charAt($enc3)
                    + this.base64.charAt($enc4);
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
                $output += String.fromCharCode(((this.hex.indexOf($input.charAt($i++)) << 4) & 0xf0)
                                               | (this.hex.indexOf($input.charAt($i++)) & 0xf));
            } while ($i < $input.length);
            return $output;
        }
    };
    
    function pkcs1pad2(s,n) {
        if(n < s.length + 11) { // TODO: fix for utf-8
            alert("Message too long for RSA");
            return null;
        }

        var ba = new Array();
        var i = s.length - 1;
        while(i >= 0 && n > 0) {
            var c = s.charCodeAt(i--);
            if(c < 128) { // encode using utf-8
                ba[--n] = c;
            } else
            if((c > 127) && (c < 2048)) {
                ba[--n] = (c & 63) | 128;
                ba[--n] = (c >> 6) | 192;
            } else {
                ba[--n] = (c & 63) | 128;
                ba[--n] = ((c >> 6) & 63) | 128;
                ba[--n] = (c >> 12) | 224;
            }
        }

        ba[--n] = 0;
        while(n > 2) { // random non-zero pad
            ba[--n] = Math.floor(Math.random()*254) + 1;
        }

        ba[--n] = 2;
        ba[--n] = 0;
        return new BigInteger(ba);
    }

    var pw_encode = function(pass, exp, mod) {
        var keysize = 128;
        var keyexp = new BigInteger(exp, 16);
        var keymod = new BigInteger(mod, 16);

        var paddata = pkcs1pad2(pass, keysize);
        var encdata = paddata.modPow(keyexp, keymod).toString(16);

        if ((encdata.length & 1) != 0)
            encdata = "0" + encdata;

        return Base64.encode(Hex.decode(encdata));
    };

    context.com = function(request, onresponse, onerror) {
        if (!isFunction(onresponse))
            throw "onresponse argument is not a function";
        reqdata = JSON.stringify(request);
        context.connection.onmessage = function(repdata) {
            context.inwork = false;
            try {
                context.connection.onmessage = function(rd) {
                    if (debug) console.log("Unexpected message: " + rd);
                };
                //if (debug) console.log('Got response: ' + repdata.data);
                rep = json_parse(repdata.data);
                numRows = 'numRows' in rep.responseData ? rep.responseData.numRows : 
                          'results' in rep.responseData ? rep.responseData.results[0].resultSet.numRows : null;

                if (debug) console.log('Got response: ' + numRows + ' rows');
                if (rep['status'] == 'ok') {
                    if (rep['exception'] != undefined)
                        throw ("Database error [" + rep['exception']['sqlCode'] + "] "
                               + rep['exception']['text']);
                    onresponse(rep['responseData']);
                } else if (rep['status'] == 'error') {
                    throw ("Operational error [" + rep['exception']['sqlCode'] + "] "
                           + rep['exception']['text']);
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
        
        if (debug) console.log('Send request: ' + reqdata);
        context.inwork = true;
        context.connection.send(reqdata);
    };

    context.fetch = function(res, startPosition, numBytes, onResponse) {
        context.com({'command': 'fetch',
                     'resultSetHandle': +parseInt(res.resultSetHandle),
                     'startPosition': +startPosition,
                     'numBytes': +numBytes},
                    function(rep) {
                        res.data = rep.data;
                        res.numRowsInMessage = rep.numRows;
                        onResponse(res);
                    }, context.onerror);
    };

    context.inwork = false;
    context.connection = new WebSocket(url, { "cert_reqs":0,
        //cert: "-----BEGIN CERTIFICATE-----\nMIIDPTCCAiWgAwIBAgIJAMZU5w2Lf1cPMA0GCSqGSIb3DQEBCwUAMDUxCzAJBgNV\nBAYTAkRFMRIwEAYDVQQHDAlOdXJlbWJlcmcxEjAQBgNVBAoMCUVYQVNPTCBBRzAe\nFw0xOTExMDgxNTExMDdaFw0zMzA3MTcxNTExMDdaMDUxCzAJBgNVBAYTAkRFMRIw\nEAYDVQQHDAlOdXJlbWJlcmcxEjAQBgNVBAoMCUVYQVNPTCBBRzCCASIwDQYJKoZI\nhvcNAQEBBQADggEPADCCAQoCggEBALfypvhPv1vlhAzeMO5Vn6FMNiYgHWN4dDXK\n9Hx80yXLuyuoB1H47SS/SHLDIvGliwFT5T71cjcI17vrNmXxcIpvgEsYPCAVN0Pi\nfEpnia8AFJRjJ8BsR0uRpuZJDJPxyL16luwpL6XNGJL317goRas6gH8gLqA5PDHN\nMZB5hM/X78iKWMsgYzk4Ja48DBRJbY0qqHTZQvsVJobo/57+vPzdFBFQglNNP3np\nWtV875el4sMG9qD1pyLzc5LOYH5hqkxwbO/GFIOzq/Bprv7VdiIbXK4zOHa/ut/B\ntuuEfjUfdVif6jwYtAMBcnsRD2tLUI7RY6IJARa4DcNqP+nnrncCAwEAAaNQME4w\nHQYDVR0OBBYEFMyqj1V9IlgICg5x/Mg/vKQyopvkMB8GA1UdIwQYMBaAFMyqj1V9\nIlgICg5x/Mg/vKQyopvkMAwGA1UdEwQFMAMBAf8wDQYJKoZIhvcNAQELBQADggEB\nAG0ulZfrJ2XP3bEUX2nSNaKOxnTJhaR1a3xyDDDWH9MTw94121CB5YdGM2Fu6+ss\ngGrNpxyGPtfbJlzjLQJntPerdsKJWPjP8Fa7BLqE1FuIv47koauDUf9jiuLk1aPs\ndWPIO1v/jbmao7tyGLIjuBsB/+exDkijjvCL0a/f4PKeSR9j6CB7TBehx0qWQa6f\npGU3xgow54bFhvYORpbKrAYSAQIaCGIpw4wnASFRJ8QPXqrNJjXSxT4DM3eMiOJQ\nZwfkMuFZzTdkjWPAWIyJBT8eAcew/E0+MDt8LztkVhiYy7F2RB0FO+2uEeIo5Pd/\nc8o+KrbsHm4AIw8rcl2OvtI=\n-----END CERTIFICATE-----\n"
        rejectUnauthorized: false //sslCertificatePath: ""
    });
    context.connection.onopen = function () {
        context.com({"command": "login", "protocolVersion": 1},
                    function(response) {
                        var pw = pw_encode(pass,
                                           response['publicKeyExponent'],
                                           response['publicKeyModulus']);
                        context.publicKey = response['publicKey'];
                        context.com({"username": user,
                                     "password": pw,
                                     "useCompression": false,
                                     "clientName": "EXAJS",
                                     "driverName": "WS",
                                     "clientOs": "Browser",
                                     "clientOsUsername": "N/A",
                                     "clientVersion": "0.1",
                                     "clientRuntime": "Browser"},
                                    function(response) {
                                        context.sessionId = response['sessionId'];
                                        onconnect(context);
                                    }, context.onerror);
                    }, context.onerror);
    };
}};