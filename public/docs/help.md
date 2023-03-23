# -h

usage: snarf [-h] [-browser {auto,chrome,firefox,remote}] [-login {auto,onlyfans,twitter}] [-reduce] [-save] [-tweet]
                 [--username USERNAME] [-config PATH_CONFIG] [-debug] [-keep] [-show] [-v] [-version]
                 {discount,message,post,users} ...

positional arguments:
  {discount,message,post,users}
                        Include a sub-command to run a corresponding action:
    discount            > discount one or more users
    message             > send a message to one or more users
    post                > upload a post
    users               > scan & save users

optional arguments:
  -h, --help            show this help message and exit
  -browser {auto,chrome,firefox,remote}, -B {auto,chrome,firefox,remote}
                        web browser to use
  -login {auto,onlyfans,twitter}, -L {auto,onlyfans,twitter}
                        method of user login to prefer
  -reduce               enable reducing files over 50 MB
  -save, -S             enable saving users locally on exit
  -tweet                enable tweeting when posting
  --username USERNAME, --u USERNAME
                        OnlyFans username to use
  -config PATH_CONFIG, -C PATH_CONFIG
                        path to config.conf
  -debug, -D            enable debugging
  -keep, -K             keep browser window open after scripting ends
  -show, -SW            enable displaying browser window
  -v, -verbose          verbosity level (max 3)
  -version              show program's version number and exit

Shnarrf!

# Discount

usage: snarf discount [-h] [-amount AMOUNT] [-months MONTHS] [-user USER | -users USERS]

optional arguments:
  -h, --help      show this help message and exit
  -amount AMOUNT  amount (%) to discount by
  -months MONTHS  number of months to discount
  -user USER      user to discount
  -users USERS    users to discount

# Message

usage: snarf message [-h] [-date DATE] [-performers PERFORMERS] [-price PRICE] [-schedule SCHEDULE] [-time TIME] [-tags TAGS]
                         [-text TEXT] [-user USER | -users USERS]
                         ...

positional arguments:
  input                 one or more paths to files (or folder) to include in the message

optional arguments:
  -h, --help            show this help message and exit
  -date DATE            schedule date (MM-DD-YYYY)
  -performers PERFORMERS
                        performers to reference. adds "@[...performers]"
  -price PRICE          price to charge ($)
  -schedule SCHEDULE    schedule (MM-DD-YYYY:HH:MM:SS)
  -time TIME            time (HH:MM)
  -tags TAGS            the tags (@[tag])
  -text TEXT            text to send
  -user USER            user to message
  -users USERS          users to message

# Post

usage: snarf post [-h] [-date DATE] [-duration {1,3,7,30,99} | -expiration EXPIRATION] [-performers PERFORMERS] [-price PRICE]
                      [-schedule SCHEDULE] [-time TIME] [-tags TAGS] [-text TEXT] [-question QUESTIONS]
                      ...

positional arguments:
  input                 one or more paths to files (or folders) to include in the post

optional arguments:
  -h, --help            show this help message and exit
  -date DATE            schedule date (MM-DD-YYYY)
  -duration {1,3,7,30,99}
                        duration in days (99 for 'No Limit') for a poll
  -expiration EXPIRATION
                        expiration in days (999 for 'No Limit')
  -performers PERFORMERS
                        performers to reference. adds "@[...performers]"
  -price PRICE          price to charge ($)
  -schedule SCHEDULE    schedule (MM-DD-YYYY:HH:MM:SS)
  -time TIME            time (HH:MM)
  -tags TAGS            tags (@[tag])
  -text TEXT            text to send
  -question QUESTIONS, -Q QUESTIONS
                        questions to ask

# Users

usage: snarf users [-h]

optional arguments:
  -h, --help  show this help message and exit
