wsjsapi = require('./wsjsapi');

class ExasolConnection {
    account = null;
    username = null;
    password = null;
    sessionId = null;
    exa_con = null;

    constructor(account, username, password) {
        this.account = account
        this.username = username
        this.password = password
    }

    connect(callback) {
        var conn = this
        var err = null

        this.exa_con = new wsjsapi.Exasol("ws://"+this.account, this.username, this.password,
        function (context) {
            console.log('Connected: ' + context)
            conn.sessionId = context.sessionId
            err = null
            callback(err, conn)
        },
        function(err_msg) {
            err = { message: err_msg }
            conn = null
            callback(err, conn)
        });
    }

    getId() {
        return this.sessionId
    }

    static get_rows(resultSet, columns) {
        var rows = []
        var data = resultSet.data      /* [ [r1c1, r1c2], [r2c1, r2c2], ...] */
        for(var r in data) {
            var row = {}
            for(var c in columns) {
                row[columns[c].name] = data[c][r]
            }
            rows.push(row)
        }
        return rows
    }

    rows = []
    numRows_total = 0
    numRows_current_pos = 0

    fetch_next_batch(resultSet, columns, stmt, callback) {
        var err = null
        var conn = this
        conn.exa_con.fetch(resultSet, conn.numRows_current_pos, 1024*10,
            function (res) {
                var new_rows = ExasolConnection.get_rows(res, columns)
                conn.numRows_current_pos += parseInt(res.numRowsInMessage);
                conn.rows = conn.rows.concat(new_rows)

                if(conn.numRows_current_pos == conn.numRows_total) { /* finished */
                    callback(err, stmt, conn.rows)
                } else {  /* continue with next batch */
                    conn.fetch_next_batch(resultSet, columns, stmt, callback)
                }
        });
    }

    execute(exe_details) {
        var conn = this
        var err = null
        var stmt = exe_details
        var rows = []
        var exa_con = this.exa_con

        if(!('sqlText' in exe_details) || !('complete' in exe_details)) {
            console.error('Statement error: sqlText and complete (function) must be provided')
        }
        exa_con.com({'command': 'execute', 'sqlText': exe_details.sqlText},
            function(rep) {
               var columns = rep.results[0].resultSet.columns      /* [ {name:..., dataType:...}] */
               conn.numRows_total = parseInt(rep.results[0].resultSet.numRows);
               if('resultSetHandle' in rep.results[0].resultSet) {
                    rows = conn.fetch_next_batch(rep.results[0].resultSet, columns, stmt, exe_details.complete)
               } else if('data' in rep.results[0].resultSet) {
                    rows = ExasolConnection.get_rows(rep.results[0].resultSet, columns)
                    exe_details.complete(err, stmt, rows)           
               }
    
            }, function(err_msg) {
                err = { message: err_msg }
                exe_details.complete(err, stmt, rows)
            });
    }
}

module.exports = {
    createConnection: function(con_details) {
        if(!('account' in con_details) || !('username' in con_details) || !('password' in con_details)) {
            console.error('Connection error: account, username, password must be provided')
        }
        return new ExasolConnection(con_details.account, con_details.username, con_details.password)
    }
}