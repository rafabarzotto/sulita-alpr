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

var pictures = function(req, res){
    console.log(req.url);

    PythonShell.run('cont.py', function(err, data){
     if(err) console.log(err);
     console.log(data.toString());
    });
};

//route to handle a client calling node to check a plage
app.get('/check_plate/:id', function(req, res, next){

  var options = {
    args: [req.params.id]
  };

  PythonShell.run('take_recognize.py', options, function(err, data){
    if(err) res.send(err);
    res.send(data.toString());
    next();
  });

});

app.use(pictures);

var server = app.listen(3000, function() {
  console.log('Server listening on port 3000');
});
