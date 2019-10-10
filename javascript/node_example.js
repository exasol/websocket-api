// npm i jsbn
// npm i ws
exasol = require('./jsexasol');

console.log('Hello');

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
            sqlText: "SELECT article_id, description, base_sales_price FROM retail.article",
            complete: function(err, stmt, rows) {
                if (err) {
                console.error('Failed to execute statement due to the following error: ' + err.message);
                } else {
                console.log('Number of rows produced: ' + rows.length);
                }
            }
            });

            }
        }
    );