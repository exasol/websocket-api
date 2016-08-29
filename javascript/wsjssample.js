var exa = new Exasol("ws://127.0.0.1:8563", "sys", "exasol",
                     function (context) {
                         console.log('Connected: ' + context);
                     },
                     function(err) {
                         document.getElementById("result").innerHTML = "ERROR: " + err;
                     });

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
    exa.com({'command': 'execute', 'sqlText': sqlText}, function(res) {
        console.log("OK: " + JSON.stringify(rep));
        if (res.resultType == 'rowCount') {
            document.getElementById("result").innerHTML = res.numRows + " rows";
        } else if (res.resultType == 'resultSet') {
            var rset = res.resultSets[0];
            if (rset.data != undefined) {
                rset.dataRows = rset.numRows;
                printResult(rset);
            } else if (rset.numRows > 0)
                exa.fetch(rset, 0, 500000, printResult);
            else document.getElementById("result").innerHTML = "0 rows";
        } else {
            document.getElementById("result").innerHTML = "Unknown result: " + JSON.stringify(rep);
        }
    }, exa.onerror);
    return false;
}
