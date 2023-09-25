**Note**: General options go in front of the chosen subcommand. Options specific to the subcommand go after the subcommand.  
**Double Note**: These are all modified help outputs for reading on github from running the help commmand or `-h` for each subcommand.

# -h

`snarf [-h] [-browser {auto,brave,chrome,chromium,firefox}] [-login {auto,onlyfans,twitter}] [-tweet] [--username USERNAME]
             [-config PATH_CONFIG] [-debug] [-keep] [-show] [-v] [-version]
             {api,config,discount,menu,message,post,users} ...`

No mention of old Shnarf, I notice. Go ahead, just take all the glory, and leave it to Snarf to clean up after you. I don't mind!  

positional arguments: {**api**,**config**,**discount**,**menu**,**message**,**post**,**users**}  

Include a sub-command to run a corresponding action:  
**api**                 > flask server  
**config**              > configuration options  
**discount**            > discount one or more users  
**menu**                > access the cli menu  
**message**             > send a message to one or more users  
**post**                > upload a post  
**users**               > scan & save users  

options:
> -h, --help            show this help message and exit  
> -browser {auto,brave,chrome,chromium,firefox}, -B {auto,brave,chrome,chromium,firefox}	web browser to use  
> -login {auto,onlyfans,twitter}, -L {auto,onlyfans,twitter}	method of user login to prefer  
> -tweet                enable tweeting when posting  
> --username USERNAME, --u USERNAME		OnlyFans username to use  
> -config PATH_CONFIG, -C PATH_CONFIG	path to config.conf  
> -debug, -D            enable debugging  
> -keep, -K             keep browser window open after scripting ends  
> -show, -SW            enable displaying browser window  
> -v, -verbose          verbosity level (max 3)  
> -version, --version   show program's version number and exit  

Shnarrf!  

# API

`snarf api`

Flask server API for receiving POST requests to /post and /message. 

# Config

`snarf config`

Menu interface for interacting with user config files.

# Discount

`snarf discount [-h] [-amount AMOUNT] [-months MONTHS] [-user USER | -users USERS]`  

options:  
> -h, --help      show this help message and exit  
> -amount AMOUNT  amount (%) to discount by  
> -months MONTHS  number of months to discount  
> -user USER      user to discount  
> -users USERS    users to discount  

# Message

`snarf message [-h] [-date DATE] [-performers PERFORMERS] [-price PRICE] [-schedule SCHEDULE] [-time TIME] [-text TEXT] [-user USER | -users USERS] ... `  

positional arguments:  
> input                 one or more paths to files (or folder) to include in the message  

options:  
> -h, --help            show this help message and exit  
> -date DATE            schedule date (MM-DD-YYYY)  
> -performers PERFORMERS  performers to reference. adds "@[...performers]"  
> -price PRICE          price to charge ($)  
> -schedule SCHEDULE    schedule (MM-DD-YYYY:HH:MM:SS)  
> -time TIME            time (HH:MM)  
> -text TEXT            text to send  
> -user USER            user to message  
> -users USERS          users to message  

# Post

`snarf post [-h] [-date DATE] [-duration {1,3,7,30,99} | -expiration EXPIRATION] [-performers PERFORMERS] [-price PRICE] [-schedule SCHEDULE] [-time TIME] [-text TEXT] [-question QUESTIONS] ... `  

positional arguments:  
> input                 one or more paths to files (or folders) to include in the post  

options:  
> -h, --help            show this help message and exit  
> -date DATE            schedule date (MM-DD-YYYY)  
> -duration {1,3,7,30,99} duration in days (99 for 'No Limit') for a poll  
> -expiration EXPIRATION  expiration in days (999 for 'No Limit')  
> -performers PERFORMERS  performers to reference. adds "@[...performers]"  
> -price PRICE          price to charge ($)  
> -schedule SCHEDULE    schedule (MM-DD-YYYY:HH:MM:SS)  
> -time TIME            time (HH:MM)  
> -text TEXT            text to send  
> -question QUESTIONS, -Q QUESTIONS   questions to ask  

# Users

`snarf users [-h]`  

options:  
> -h, --help  show this help message and exit  
