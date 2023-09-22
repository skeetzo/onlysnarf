<h1 align="center">OnlySnarf</h1>
<p align="center"><img src="public/images/snarf-missionary.jpg" alt="Shnarf" width="400"/></p>
<p align="center">Please refer to the <a href="public/docs/menu.md">Menu</a> for help with the available arguments and config settings.</p> 

## Description
OnlySnarf is a python based automation tool to assist with uploading content to OnlyFans by interacting with the site purely via web scraping. OnlySnarf carries no weapons, but it has been known to use its tail, teeth and claws when improperly configured.

Here are some fuzzy debugging previews of how it looks when everything works:
- [Discount](//ipfs.io/ipfs/QmboqfpCeAAbbhqGhPQ8cCscqm7CNH4mxTPR42g8Cg7iLW?filename=discount.gif)
- [Message](//ipfs.io/ipfs/QmXitqxkRuMXb6XnUJw7MHUxLii7UNEXjENc5k4PyfTWfY?filename=message.gif)
- [Poll](//ipfs.io/ipfs/QmNkE4GpBoiQ3tGLLfxtTGS96jJJJixS4qbkx9fxN9GeYC?filename=poll.gif)
- [Post](//ipfs.io/ipfs/QmUBjuLK3yh5v4U9SSPmSG3NAGgYaY6rYoYACGi1smZpJ7?filename=post.gif)
- [Schedule](//ipfs.io/ipfs/QmUd843FXXyMP2eyfkB1d1erZyrKN1hmKchuviruzN8ctD?filename=schedule.gif)
- [Users](//ipfs.io/ipfs/Qmc9zPytgSKx4EK6V1A8DABNeCpMxBybcRs4hNtAMSKDyi?filename=users.gif)

## Installation
There are two **different** installation options (that I know of):
1) via pip for the latest official package: `python3 -m pip install onlysnarf`  
2) or clone the repo & setup a virtual environment to install locally like in the bash script at [bin/virtualenv.sh](/bin/virtualenv.sh) 

Here is an output of the command: [`snarf -h`](/public/docs/help.md/#-h)  
  
Command example: `snarf -text "suck my giant balls" /path/to/imageOfBalls.jpeg`  
Version: `snarf -version` or `snarf --version`  

## Config
The command `snarf config` is now available for help adding, listing, updating, and removing user config files. This command **does not** (yet) help with configuring the general config file which is described as follows.

Example config files are provided. There are two main types of config files that should be provided to affect runtime behavior as well as one optional method to help distinguish between user logins for multiple accounts.
1) the config for the general app's behavior: `$HOME/.onlysnarf/config.conf`
2) one config for each user containing their credentials: `$HOME/.onlysnarf/users/$username.conf`
3) (optional) one config containing the default user credentials to use: `$HOME/.onlysnarf/users/default.conf`

The user config to use at runtime can be specificed with the "--username" argument. 
User config example: "--username alexdicksdown" --> `$HOME/.onlysnarf/users/alexdicksdown.conf`
When no "--username" argument is passed at runtime or in the config file then the default config file containing the default user credentials is used.

**Note for Windows**: the user's $HOME path works out to `C:\Users\YOUR_USERNAME` so the base directory for config files and such can instead be found at `C:\Users\YOUR_USERNAME\.onlysnarf`

**No**, the user credentials **are not** handled in the safest manner because they are very clearly **stored in plain text** with **no encryption**. Yes, a better way can be figured out. Do I think a better way is necessary for this project? No. So please be careful with your own credentials.

## API
The api server is super basic and as such runs with the Flask development server behind the standard port 5000. Be sure to remember to open this port when attempting to make requests and don't spam your own server. The api fulfills a niche role built by request and allows OnlySnarf to passively wait to receive requests from the internet with the necessary data to post or message appropriately.

Make POST requests with the same basic discount, message, or post data to: /discount   or   /message   or   /post

## Menu
The `snarf menu` command has been semi-restored and still requires further updates to return to the same pointless iteration of glory.

## Dependencies
Selenium's webdriver manager should install everything it needs automatically. If left unspecified the default browser argument is "auto" which will cylce throuch each web driver available and attempt to spawn a working browser. If you are using a Raspberry Pi 4, be sure to run `sudo apt-get install chromium-chromedriver` on your device to be able to launch chrome. The only working browsers for me have been chrome and firefox and so the others are unlikely to work without extra tinkering by yourself.

## Platforms
Code versions:
- Python: 3.10.12
- selenium: 4.8.3
- webdriver_manager: 4.0.0

Runs successfully on:
- Linux Ubuntu : 86_64 
- Windows 11

Runs sucessfully with browsers:
- Chrome
- Firefox

Runs successfully on devices:
- Raspberry Pi 4 : aarch64

## Dev
If you are doing your own development or webscraping all of the related files are available at: [OnlySnarf/lib/webdriver](/OnlySnarf/lib/webdriver)  
And the shortcut file for [webdriver](/OnlySnarf/lib/driver.py) behaviors that I'm not quire sure if I want to be a class or not but is used to funnel proper interactions through.  
More in code commenting / documentation will come later.  

## Tests

The test environment uses the config file found at: [OnlySnarf/conf/test-config.conf](/OnlySnarf/conf/test-config.conf) 

Basic unittesting behavior organized by classes:
- `python -m unittest tests/classes/test_discount.py`
- `python -m unittest tests/classes/test_post.py`
- `python -m unittest tests/classes/test_message.py`
- `python -m unittest tests/classes/test_users.py`
and by webdriver interactions:
- `python -m unittest tests/webdriver/test_discount.py`
- `python -m unittest tests/webdriver/test_post.py`
- `python -m unittest tests/webdriver/test_message.py`
- `python -m unittest tests/webdriver/test_users.py`

Pytests available under /tests:
- `pytest tests`
- `pytest tests/classes`
- `pytest tests/selenium`
- `pytest tests/webdriver`

## Updates
7/5/2023 : clarifications to readme and menu text...  
4/18/2023 : to further reduce repo size, preview gifs have been relocated to [IPFS](//ipfs.io/ipfs/QmVpjSy9NXy3VUM474hSDoPSsmsb5WVYkN9WN6N7nFxZuj).  
9/20/2023 : major cleanup of webdriver structure & overlap with classes; test scripts overhaul to match  

<hr>
Feel free to make use of my <a href="//onlyfans.com/?ref=409408" target="_blank">referral code</a> ;)