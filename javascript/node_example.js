// npm i jsbn
// npm i ws
exasol = require('./jsexasol');

console.log('Hello');

var start = process.hrtime();

var elapsed_time = function(note){
    var precision = 3; // 3 decimal places
    var elapsed = process.hrtime(start)[1] / 1000000; // divide by a million to get nano to milli
    console.log(process.hrtime(start)[0] + " s, " + elapsed.toFixed(precision) + " ms - " + note); // print message + time
    start = process.hrtime(); // reset the timer
}

account = 'localhost:8563'
user = 'sys'
password = 'exasol'

// Create a Connection object that we can use later to connect.
var connection = exasol.createConnection( {
    account: account,
    username: user,
    password: password
    }
    );

connection.connect( 
    function(err, conn) {
        if (err) {
            console.error('Unable to connect: ' + err.message);
            } 
        else {
            console.log('Successfully connected to Exasol.');
            // Optional: store the connection ID.
            connection_ID = conn.getId();

            console.log('Session ID: '+connection_ID);

            connection.execute({
            //sqlText: "SELECT 5 AS num, 'hi' as txt union all SELECT 7 AS num, 'hello' as txt",
            //sqlText: "SELECT article_id, description, base_sales_price FROM retail.article",
            sqlText: "SELECT * FROM retail.sales_positions LIMIT 1000000",
            complete: function(err, stmt, rows) {
                if (err) {
                console.error('Failed to execute statement due to the following error: ' + err.message);
                } else {
                console.log('Number of rows produced: ' + rows.length);
                console.log('ARTICLE_ID: '+rows[123456].ARTICLE_ID)
                elapsed_time('Finish')
                }
            }
            });

            }
        }
    );