var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var path = require('path');
var formidable = require('formidable');
var fs = require('fs');
var cors = require('cors');
var PythonShell = require('python-shell');
var sys = require('sys'),
  exec = require('child_process').exec;
app.set('view engine', 'jade');

app.use(bodyParser.json());
app.use(cors());

var pictures = function(req, res) {
  if (res.locals['plate'] == "NOK" || res.locals['plate'] == "Arquivo nao encontrado" || res.locals['plate'] == undefined || res.locals['plate'] == "Problema na Camera") {
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

app.get('/', function(req, res) {;
  //res.send("API");
  res.render('index', {
    title: 'API',
    message: 'API-ALPR'
  });
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
      res.send("Nao foi possivel localizar ou abrir o Arquivo");
    } else {
      res.json(data.toString('utf8'));
    }
  });
});

app.get('/rmlog', function(req, res) {
  fs.unlink('/usr/local/bin/plateservice/plate_log.log', function(err) {
    if (err) {
      res.send("Nao foi possivel localizar ou apagar o Arquivo");
    } else {
      res.send("Arquivo de Log Deletado");
    }
  });
});

app.get('/confidence', function(req, res) {
  PythonShell.run('take_recognize_confidence.py', function(err, data) {
    if (err) {
      res.send(err);
    } else {
      res.send(data.toString());
    }
  });
});

//route to handle a client calling node to check a plage
app.get('/check_plate/:id', function(req, res, next) {

  var options = {
    args: [req.params.id]
  };

  PythonShell.run('take_recognize.py', options, function(err, data) {
    if (err) {
      res.send(err);
    } else {
      res.send(data.toString());
      res.locals.op = req.params.id;
      res.locals.plate = data.toString();
      next();
    }
  });
});

app.use(function(req, res, next) {
  res.status(404).send('Erro 404 essa URL não existe!');
});

app.use(pictures);

var server = app.listen(3000, function() {
  console.log('Server listening on port 3000');
});