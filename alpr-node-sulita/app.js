var express = require('express');
var app = express();
var path = require('path');
var formidable = require('formidable');
var fs = require('fs');
var cors = require('cors');
var PythonShell = require('python-shell');
var io = require('socket.io').listen(server, {
  log: false,
  origins: '*:*'
})
var sys = require('sys'),
  exec = require('child_process').exec;

app.use(cors());

app.get('/', function(req, res) {;
  res.send("API");
});

PythonShell.defaultOptions = {
  scriptPath: '/usr/local/bin/plateservice/'
};

app.get('/check_plate', function(req, res) {
  res.send('É nessario informar a operação')
});

//route to handle a client calling node to check a plage
app.get('/check_plate/:id', function(req, res) {
  var op = req.params.id;

  var options = {
    args: [op]
  };

  PythonShell.run('take_recognize.py', options, function(err, results) {
    if (err) res.send(err);
    // results is an array consisting of messages collected during execution
    console.log('results: %j', results);
    res.json('results: %j', results);
  });

});


var server = app.listen(3000, function() {
  console.log('Server listening on port 3000');
});