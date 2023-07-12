#!/bin/bash

curl -X POST -H "Content-Type: application/json" -d '{
  "text": "your mom",
  "action": "post",
  "schedule": "07/12/2023:16:20",
  "input": "https://github.com/skeetzo/onlysnarf/blob/master/public/images/shnarf.jpg?raw=true"
}' http://localhost:5000/post

# curl -X POST -H "Content-Type: application/json" -d '{
#   "text": "your mom",
#   "action": "post",
#   "price": 6,
#   "user": "random",
#   "input": "https://github.com/skeetzo/onlysnarf/blob/master/public/images/shnarf.jpg?raw=true, https://github.com/skeetzo/onlysnarf/blob/master/public/images/snarf.jpg?raw=true"
# }' http://localhost:5000/message