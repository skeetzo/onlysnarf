#!/bin/bash

HOST=localhost

# curl -X POST -H "Content-Type: application/json" -d '{
#   "text": "your mom",
#   "schedule": "07/18/2023 16:20:00",
#   "input": "https://github.com/skeetzo/onlysnarf/blob/master/public/images/shnarf.jpg?raw=true"
# }' http://$HOST:5000/post

curl -X POST -H "Content-Type: application/json" -d '{
  "text": "your mom",
  "price": 6,
  "user": "random",
  "input": "https://github.com/skeetzo/onlysnarf/blob/master/public/images/shnarf.jpg?raw=true, https://github.com/skeetzo/onlysnarf/blob/master/public/images/snarf.jpg?raw=true"
}' http://$HOST:5000/message