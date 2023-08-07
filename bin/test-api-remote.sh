#!/bin/bash

# curl -X POST -H "Content-Type: application/json" -d '{
#   "text": "your mom",
#   "input": "https://github.com/skeetzo/onlysnarf/blob/master/public/images/shnarf.jpg?raw=true"
# }' http://13.48.136.241:5000

# curl -X POST -H "Content-Type: application/json" -d '{
#   "text": "your mom",
#   "user": "random",
#   "input": "https://github.com/skeetzo/onlysnarf/blob/master/public/images/shnarf.jpg?raw=true"
# }' http://13.57.87.181:5000/message


curl -X POST -H "Content-Type: application/json" -d '{
  "text": "your mom",
  "input": "https://github.com/skeetzo/onlysnarf/blob/master/public/images/shnarf.jpg?raw=true"
}' http://3.101.69.182:5000/post

