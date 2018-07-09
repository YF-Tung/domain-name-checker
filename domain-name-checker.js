#!/usr/bin/env node
// This is a simple wrapper for domain-name-checker.py, in case one must use node

const { spawn } = require('child_process');
const dnc = spawn('./domain-name-checker.py', process.argv.slice(2))

dnc.stdout.on('data', (data) => {
  console.log(`stdout: ${data}`);
});

dnc.stderr.on('data', (data) => {
  console.log(`stderr: ${data}`);
});

dnc.on('close', (code) => {
  console.log(`child process exited with code ${code}`);
});

