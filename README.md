<h1 align="center">OnlySnarf</h1>
<p align="center"><img src="public/images/snarf-missionary.jpg" alt="Shnarf" width="400"/></p>
<p align="center">Please refer to the <a href="public/docs/menu.md">Menu</a> for help with the available arguments and config settings.</p> 

## Description
OnlySnarf is a python based automation tool to assist with uploading content to OnlyFans by interacting with the site via web scraping. It does not interact with the API whatsoever. OnlySnarf carries no weapons, but it has been known to use its tail, teeth and claws when improperly configured.

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

## Config
Example config files are provided. There are two main config files that should be provided to affect runtime behavior as well as one optional method to help distinguish between user logins for multiple accounts.
1) the config for the general app's behavior: `$HOME/.onlysnarf/config.conf`
2) one config for each user containing their credentials: `$HOME/.onlysnarf/users/$username.conf`
3) (optional) one config containing the default user credentials to use: `$HOME/.onlysnarf/users/default.conf`

User config example: `$HOME/.onlysnarf/users/alexdicksdown.conf`

**Note for Windows**: the user's $HOME path works out to `C:\Users\YOUR_USERNAME` so the base directory for config files and such can instead be found at `C:\Users\YOUR_USERNAME\.onlysnarf`

**No**, the user credentials **are not** handled in the safest manner because they are very clearly **stored in plain text** with **no encryption**. Yes, a better way can be figured out. Do I think a better way is necessary for this project? No. So please be careful with your own credentials.

## Dependencies
Selenium's webdriver manager should install everything it needs automatically. If left unspecified the default browser argument is "auto" which will cylce throuch each web driver available and attempt to spawn a working browser. If you are using a Raspberry Pi 4, be sure to run `sudo apt-get install chromium-chromedriver` on your device to be able to launch chrome. 

## Platforms
Runs successfully on:
- Linux Ubuntu
- Windows 11

Runs sucessfully on browsers:
- Chrome
- Firefox

Runs successfully on devices:
- Raspberry Pi 4

## Tests

The test environment uses the config file found at:  [OnlySnarf/conf/test-config.conf](/OnlySnarf/conf/test-config.conf) 

Basic unittesting:
- `python -m unittest tests/snarf/test_discount.py`
- `python -m unittest tests/snarf/test_post.py`
- `python -m unittest tests/snarf/test_message.py`
- `python -m unittest tests/snarf/test_users.py`

Pytests available under /tests:
- `pytest tests/selenium`
- `pytest tests/snarf`

## Updates
7/5/2023 : clarifications to readme and menu text...
4/18/2023 : To further reduce repo size, preview gifs have been relocated to [IPFS](//ipfs.io/ipfs/QmVpjSy9NXy3VUM474hSDoPSsmsb5WVYkN9WN6N7nFxZuj).

<hr>
Feel free to make use of my <a href="//onlyfans.com/?ref=409408" target="_blank">referral code</a> ;)