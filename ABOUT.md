# OnlySnarf

Hi all, I'm Skeetzo / Alex D.

I've been working on OnlySnarf for ~2 years now and I guess a write up is pretty overdue.
-
OnlySnarf is an automation tool written in Python (3). I personally use it every week (that it works) to upload content to my OnlyFans account, [alexdicksdown](https://onlyfans.com/alexdicksdown). Well at least every week that it is in a working state as it has required constant maintenance to ensure scraping accuracy as well as adding features that OnlyFans provides or hasn't provided as-of-yet. 

The aim of this tool is to provide a means for me to easily provide content to my fans.

For example, for a brief time my tool was the only way for me to mass message fans, which was cool. Then they added an easier way to "Mass Message" all your fans, followers, recent, etc which I then re-implemented into the OnlySnarf tool. My approach is organized into 3 basic categories: images, galleries, and video. The additional category of 'performer' is provided to allow for uploading content that specifically involves another Sex Worker, as that is my reason for using OnlyFans. I intend to include additional tools to ease my use of this app in such a way, for example, with capacities to share the content specifically with the fellow performer as a means to ease/automate sharing with fellow Sex Workers.

## Login

Currently this tool has been making use of the 'Two Factor Authentication' via Twitter to properly log into my account. This provides me with a notification in Twitter that my 'account is being accessed blabla' so that I am informed via default notifications that my script is not only running but has gained proper access to my account. As my Twitter has recently been uh flagged for 'possible bullshit' I don't know I've since added more features to login ala the typical username/password combo offered by OnlyFans as well as the Google auth. I had specifically designed my tool to solely use Twitter not out of laziness but by the simplicity that doing so provided the least complications: no captcha, no extra clicking on usernames. Just a simple redirect w/ username & password. So, while now my tool offers potentially up to 3 ways of logging in, only 2 of which are really feasible. 1 of which happens to prefer to provide a captcha. The final remaining option is Twitter which.... works perfectly so-- I highly recommend simply linking a Twitter account to facilitate OnlyFans login.

Though I am in doubt it will work at all, the Google auth requires more debugging

## Content

I initially coded this tool to upload content from my Google Drive account. I setup my folders to organize my uploads in a basic layout of: images, galleries, videos. This is a reflection of the purpose the content will be expressed with in OnlyFans- as images, galleries, and video uploads. It is rarer that the images folder is used, though it exists to specifically upload single images as messages to users more than as single file uploads. Galleries are the most common uploads to exist as content with videos being a likely close second.

I've since begun adding methods to upload / host content in other locations such as a remote server or Dropbox.

## Menu

The menu system via `onlysnarf` exists to provide a means for selecting content for upload without the burden of logging in, uploading the files and text, and closing the browser hours later when its finished. I try to maintain the menu system to allow for any possible upload / message combination.

## Script

I typically skip the menu system and run the package as an unprompted script via `onlysnarfpy`. This was extremely useful for me when I was suffering from incredibly slow upload speeds and didn't want to wait around to hit the post button hours later at my desktop or on my phone.