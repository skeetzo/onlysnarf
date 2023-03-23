<h1 align="center">OnlySnarf</h1>
<p align="center"><img src="public/images/snarf-missionary.jpg" alt="Shnarf" width="400"/></p>
<p align="center">Please refer to the <a href="OnlySnarf/docs/menu.md">Menu</a> for help with the available arguments and config settings.</p> 

## Description
OnlySnarf is a python based automation tool to assist with uploading content to OnlyFans by interacting with the site via web scraping. OnlySnarf carries no weapons, but it has been known to use its tail, teeth and claws when improperly configured.

Here are some debugging previews of how it looks when everything works:
- [Discount](public/previews/discount.gif)
- [Message](public/previews/message.gif)
- [Poll](public/previews/poll.gif)
- [Post](public/previews/post.gif)
- [Schedule](public/previews/schedule.gif)
- [Users](public/previews/users.gif)

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
>  -[refer to [menu](OnlySnarf/dogs/menu.md) for more options] ...
>
> Shnarrf!
  
Example: `snarf -text "suck my giant balls" /path/to/balls.jpeg`

## Config
The config process has been updated as well from the previous format. Example config files are provided. There are now 2 main config files that should be provided to affect runtime behavior as well as 1 optional method to distinguish between user logins.
1) the config for the general app's behavior: `$HOME/.onlysnarf/config.conf`
2) one config for each user containing their credentials: `$HOME/.onlysnarf/users/$username.conf`
3) an optional default user config containing the default credentials to use: `$HOME/.onlysnarf/users/default.conf`

For example: `$HOME/.onlysnarf/users/alexdicksdown.conf`

**No**, the user credentials *are not* handled in the safest manner because they are very clearly stored in plain text and without any encryption. Yes, a better way can be figured out. Do I think a better way is necessary for this project? No. So please be careful with your own credentials.

## Dependencies
Selenium's webdriver manager should install everything it needs automatically. If you are using a Raspberry Pi 4, be sure to run `sudo apt-get install chromium-chromedriver` on your device to be able to launch chrome.

## Referral
Feel free to make use of my referral code ;)  
https://onlyfans.com/?ref=409408
