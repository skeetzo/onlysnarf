#!/usr/bin/env node 
let args = ['-d'];
process.argv.forEach((val, index) => {
  // console.log(`${index}: ${val}`)
  if (index>1) args.push(val);
})
// console.log(args);
// return;
console.log('Spawning Python Demo process...');
let {PythonShell} = require('python-shell');
var path = require('path');
let options = {
  'mode': 'text',
  'pythonPath': '/usr/bin/python3',
  'pythonOptions': ['-u'], // get print results in real-time
  'scriptPath': path.join(__dirname,'../OnlySnarf'),
  'args': args
};
let pyshell = new PythonShell('onlysnarf.py', options);

pyshell.on('message', function (message) {
  console.log(message);
});

// end the input stream and allow the process to exit
pyshell.end(function (err, code, signal) {
  if (err) console.warn(err);
  console.log('The exit code was: ' + code);
  console.log('The exit signal was: ' + signal);
  console.log('OnlyFans Demo Completed');
});  


