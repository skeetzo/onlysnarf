<h1 align="center">OnlySnarf</h1>
<p align="center"><img src="public/images/snarf-missionary.jpg" alt="Shnarf" width="400"/></p>
<p align="center">Please refer to the <a href="public/docs/menu.md">Menu</a> for help with the available arguments and config settings.</p> 

## Description
OnlySnarf is a python based automation tool to assist with uploading content to OnlyFans by interacting with the site via web scraping. OnlySnarf carries no weapons, but it has been known to use its tail, teeth and claws when improperly configured.

Here are some debugging previews of how it looks when everything works:
- [Discount](//ipfs.io/ipfs/QmboqfpCeAAbbhqGhPQ8cCscqm7CNH4mxTPR42g8Cg7iLW?filename=discount.gif)
- [Message](//ipfs.io/ipfs/QmXitqxkRuMXb6XnUJw7MHUxLii7UNEXjENc5k4PyfTWfY?filename=message.gif)
- [Poll](//ipfs.io/ipfs/QmNkE4GpBoiQ3tGLLfxtTGS96jJJJixS4qbkx9fxN9GeYC?filename=poll.gif)
- [Post](//ipfs.io/ipfs/QmUBjuLK3yh5v4U9SSPmSG3NAGgYaY6rYoYACGi1smZpJ7?filename=post.gif)
- [Schedule](//ipfs.io/ipfs/QmUd843FXXyMP2eyfkB1d1erZyrKN1hmKchuviruzN8ctD?filename=schedule.gif)
- [Users](//ipfs.io/ipfs/Qmc9zPytgSKx4EK6V1A8DABNeCpMxBybcRs4hNtAMSKDyi?filename=users.gif)

## Installation

pip: `python -m pip install onlysnarf`  
clone repo & install: `git clone git@github.com:skeetzo/onlysnarf && python setup.py install`  

> usage: snarf [-h] [-version] ...
> 
> positional arguments:
> input       file or folder path for input to post or message
> 
> optional arguments:
>  -h, --help  show this help message and exit
>  -version    show program's version number and exit
>  -[refer to [menu](public/docs/menu.md) for more options] ...
>
> Shnarrf!
  
Example: `snarf -text "suck my giant balls" /path/to/balls.jpeg`

## Config
Example config files are provided. There are two main config files that should be provided to affect runtime behavior as well as one optional method to help distinguish between user logins.
1) the config for the general app's behavior: `$HOME/.onlysnarf/config.conf`
2) one config for each user containing their credentials: `$HOME/.onlysnarf/users/$username.conf`
3) (optional) one config containing the default user credentials to use: `$HOME/.onlysnarf/users/default.conf`

For example: `$HOME/.onlysnarf/users/alexdicksdown.conf`

**Note**: for Windows users the $HOME path works out to: "C:\Users\YOUR_USERNAME" so the base directory can be found at "C:\Users\YOUR_USERNAME\.onlysnarf"

**No**, the user credentials *are not* handled in the safest manner because they are very clearly stored in plain text and without any encryption. Yes, a better way can be figured out. Do I think a better way is necessary for this project? No. So please be careful with your own credentials.

## Dependencies
Selenium's webdriver manager should install everything it needs automatically. If you are using a Raspberry Pi 4, be sure to run `sudo apt-get install chromium-chromedriver` on your device to be able to launch chrome.

## Platforms
Runs successfully on:
- Linux Ubuntu
- Windows 11

## Tests
Basic unittesting:
- `python -m unittest tests/snarf/test_discount.py`
- `python -m unittest tests/snarf/test_post.py`
- `python -m unittest tests/snarf/test_message.py`
- `python -m unittest tests/snarf/test_users.py`

Pytests available under /tests:
- `pytest tests/selenium`
- `pytest tests/snarf`

## Updates
4/18/2023 : To further reduce repo size, preview gifs have been relocated to [IPFS](//ipfs.io/ipfs/QmVpjSy9NXy3VUM474hSDoPSsmsb5WVYkN9WN6N7nFxZuj).

## Referral
Feel free to make use of my referral code ;)  
//onlyfans.com/?ref=409408
