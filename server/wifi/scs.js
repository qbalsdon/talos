const SERVER_PORT=5000;
const http = require('http');
var ip = require('ip');

var server = http.createServer(function (req, res) {
    if (req.url == '/') { //check the URL of the current request
        // set response header
        res.writeHead(200, { 'Content-Type': 'text/html' }); 
        
        // set response content    
        //res.write('<html><body><p>This is home Page.</p></body></html>');
        res.write('Hello, client');
        res.end();
    }
});

server.listen(SERVER_PORT); 

console.log('Script Command Server ' + ip.address()  + ':' + SERVER_PORT + ' is running..')

