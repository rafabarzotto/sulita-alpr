var express = require('express');
var app = express();
var path = require('path');
var fs = require('fs');
var cors = require('cors');
var PythonShell = require('python-shell');

var sys = require('sys'),
  exec = require('child_process').exec;


var pictures = function(req, res) {
  console.log(res.locals['plate']);
  if (res.locals['plate'] == "NOK" || res.locals['plate'] == "Arquivo nao encontrado" || res.locals['plate'] == undefined) {
    console.log("Nao capturar fotos");
  } else {
    console.log("Salvando Fotos - Aguarde");
    var options = {
      args: [res.locals['op'], res.locals['plate']]
    };

    PythonShell.run('cont.py', options, function(err, data) {
      if (err) console.log(err);
      console.log(data.toString());
    });
  }
};

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

app.get('/log', function(req, res) {
  fs.readFile('/usr/local/bin/plateservice/plate_log.log', function(err, data) {
    if (err) {
      res.send("Could not open file: %s", err);
      process.exit(1);
    }
    res.json(data.toString('utf8'));
  });
});

//route to handle a client calling node to check a plage
app.get('/check_plate/:id', function(req, res, next) {

  var options = {
    args: [req.params.id]
  };

  PythonShell.run('take_recognize.py', options, function(err, data) {
    if (err) res.send(err);
    res.send(data.toString());
    res.locals.op = req.params.id;
    res.locals.plate = data.toString();
    next();
  });
});

app.use(pictures);

var server = app.listen(3000, function() {
  console.log('Server listening on port 3000');
});