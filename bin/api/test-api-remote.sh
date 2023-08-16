#!/bin/bash

HOST=someaddress.com

# curl -X POST -H "Content-Type: application/json" -d '{
#   "text": "your mom",
#   "input": "https://github.com/skeetzo/onlysnarf/blob/master/public/images/shnarf.jpg?raw=true"
# }' http://$HOST:5000

# curl -X POST -H "Content-Type: application/json" -d '{
#   "text": "your mom",
#   "user": "random",
#   "input": "https://github.com/skeetzo/onlysnarf/blob/master/public/images/shnarf.jpg?raw=true"
# }' http://$HOST:5000/message

curl -X POST -H "Content-Type: application/json" -d '{
  "text": "your mom",
  "input": "https://github.com/skeetzo/onlysnarf/blob/master/public/images/shnarf.jpg?raw=true"
}' http://$HOST:5000/post
