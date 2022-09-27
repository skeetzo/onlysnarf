<!-- ![shnarf](public/images/snarf-missionary.jpg "Shnarf") -->

<img src="public/images/snarf-missionary.jpg" alt="Shnarf" width="200" style="width: 50%;
  margin: 0 auto;"/>

# OnlySnarf

`python3 -m pip install OnlySnarf`  
or  
`git clone git@github.com:skeetzo/onlysnarf && python3 setup.py install`


## Description

OnlySnarf is a python based automation tool to assist with uploading content to OnlyFans by interacting with the site via web scraping. OnlySnarf carries no weapons, but he has been known to use his tail, teeth and claws.

Previous versions included the ability to download/upload from Google Drive. I have decided to drop Drive in favor of IPFS (which will be available in whichever next major version). A majority of previously funtional operations remain untested after a code "cleanup" including the original menu feature (the first part initially built). Currently, the only reliable / working way to upload is with locally available files. The runtime command has changed as well dropping the "py" previously meant to distinguish it from the menu. For example:

`onlysnarf -text "suck my giant balls" /path/to/balls.jpeg`

## Config
The config process has been updated as well from the previous format. There are now 2 main config files that should be created:
1) the config for the general app behavior
2) one for each user w/ their credentials

The config files are located in the private OnlySnarf home directory: `$HOME/.onlysnarf/`  
The general config file should be located at: `$HOME/.onlysnarf/config.conf`  
All user configs should be located at: `$HOME/.onlysnarf/users/`  
For example: `$HOME/.onlysnarf/users/alexdicksdown.conf`  

**Why Twitter credentials?**
OnlyFans uses a captcha to prevent malicious bots from accessing user accounts. However, this captcha is only necessary when logging in with your OnlyFans username and password. Logging in with the provided Twitter authentication does not provide a captcha and thus allows a more accessible automated entrance. Once logged in, saving cookies will enable sessions to be remembered thus skipping any future login checks.

## Dependencies
Selenium requires either Google Chrome or Firefox which can be installed with their respective install-* scripts in /bin. The chromedriver binary is installed with the package, however, due to being a bunch of finnicky bitches the install scripts are available to ensure proper installation and operation (I mostly have no idea what I'm doing anyways so it's safer this way).

Running `bin/install-google.sh` should result in matching version numbers. If they do not, the browser may fail to spawn properly.

## Menu
Please refer to here for help with the available arguments and config settings: [Menu](https://github.com/skeetzo/onlysnarf/blob/master/menu.md)

## Referral
Feel free to make use of my referral code ;)  
https://onlyfans.com/?ref=409408