#!/bin/bash

curl -X POST -H "Content-Type: application/json" -d '{
  "debug": "True",
  "text": "your mom",
  "action": "post",
  "input": "https://github.com/skeetzo/onlysnarf/blob/master/public/images/shnarf.jpg?raw=true"
}' http://localhost:5000/