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

**Note: this package has been updated from its previous "do a lot" design to a slim "do few things right" build. Meaning all previous methods for internally handling files and media should now be done by an alternative project / package.**

## Installation

Python 3.8.3

pip: `python -m pip install onlysnarf`  
clone repo & install: `git clone git@github.com:skeetzo/onlysnarf && python setup.py install`  

> usage: onlysnarf [-h] [-version] ...
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
  
Example: `onlysnarf -text "suck my giant balls" /path/to/balls.jpeg`

## Config
The config process has been updated as well from the previous format. Example config files are provided. There are now 2 main config files that should be provided to affect runtime behavior as well as 1 optional method to distinguish between user logins.
1) the config for the general app's behavior: `$HOME/.onlysnarf/config.conf`
2) one config for each user containing their credentials: `$HOME/.onlysnarf/users/$username.conf`
3) an optional default user config containing the default credentials to use: `$HOME/.onlysnarf/users/default.conf`

For example: `$HOME/.onlysnarf/users/alexdicksdown.conf`

**No**, the user credentials *are not* handled in the safest manner because they are very clearly stored in plain text and without any encryption. Yes, a better way can be figured out. Do I think a better way is necessary for this project? No. So please be careful with your own credentials.

**Why Twitter credentials?**
OnlyFans uses a captcha to prevent malicious bots from accessing user accounts. However, this captcha is only necessary when logging in with your OnlyFans username and password. Logging in with the provided Twitter authentication does not provide a captcha and thus allows a more accessible automated entrance. Once logged in, saving cookies will enable sessions to be remembered thus skipping any future login checks. This is possible to accomplish via regular login with OnlyFans, however, if the captcha is prompted on the first session then you will need to handle that by mouse. Once a session / cookies have been created then the same configuration settings must be used. Ergo, if the window was kept open to pass the captcha then the window must be opened each time for the session/cookies to do their job. For a headless experience one must login via Twitter or simply get lucky and not flag from overuse like I do from frequent testing.

## Dependencies
Selenium requires either Google Chrome or Firefox which can be installed with their respective install-* scripts in /bin. The chromedriver binary is installed with the package, however, due to being a bunch of finnicky bitches the install scripts are available to ensure proper installation and operation (I mostly have no idea what I'm doing anyways so it's safer this way).

Running `bin/install-google.sh` should result in matching version numbers. If they do not, the browser may fail to spawn properly.

From my current understanding, Selenium 4 may have a better method for handling binaries. If so then in a future version the above steps may be removed and instead properly handled  internally.

## Removed
Previous versions (before v4.1) included the ability to download/upload from Google Drive (and was supposed to add Dropbox). I have decided to drop everything that is not a core function of interacting with the OnlyFans site. Any extraneous file handling should be just that. I will likely create a companion tool that interacts with OnlySnarf and IPFS to automate uploads. I recommend you do the same with any file service you wish to use.

The runtime command has changed as well dropping the "py" previously meant to distinguish it from being the menu command from "onlysnarfpy" to now just "onlysnarf". Once the menu has been updated, which I only really do for personal pleasure and practice because it's quite a wonderfully useless feature, it's command will be "snarf"

## Referral
Feel free to make use of my referral code ;)  
https://onlyfans.com/?ref=409408
