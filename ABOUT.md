# OnlySnarf

Hi all, I'm Skeetzo / Alex D.

I've been working on OnlySnarf for ~2 years now and I guess a write up is pretty overdue.
-
OnlySnarf is an automation tool written in Python (3). I personally use it every week (that it works) to upload content to my OnlyFans account, [alexdicksdown](https://onlyfans.com/alexdicksdown). Well at least every week that I it is in a working state as it has required constant maintenance to ensure scraping accuracy as well as adding features that OnlyFans provides or hasn't provided as-of-yet. 

The aim of this tool is to provide a means for me to easily provide content to my fans.

For example, for a brief time my tool was the only way for me to mass message fans, which was cool. Then they added an easier way to "Mass Message" all your fans, followers, recent, etc which I then re-implemented into the OnlySnarf tool. My approach is organized into 3 basic categories: images, galleries, and video. The additional category of 'performer' is provided to allow for uploading content that specifically involves another Sex Worker, as that is my reason for using OnlyFans. I intend to include additional tools to ease my use of this app in such a way, for example, with capacities to share the content specifically with the fellow performer as a means to ease/automate sharing with fellow Sex Workers.

## Login

Currently this tool has been making use of the 'Two Factor Authentication' via Twitter to properly log into my account. This provides me with a notification in Twitter that my 'account is being accessed blabla' so that I am informed via default notifications that my script is not only running but has gained proper access to my account. As my Twitter has recently been uh flagged for 'possible bullshit' I don't know I've since added more features to login ala the typical username/password combo offered by OnlyFans as well as the Google auth. I had specifically designed my tool to solely use Twitter not out of laziness but by the simplicity that doing so provided the least complications: no captcha, no extra clicking on usernames. Just a simple redirect w/ username & password. So, while now my tool offers potentially up to 3 ways of logging in, only 2 of which are really feasible. 1 of which happens to prefer to provide a captcha. The final remaining option is Twitter which.... works perfectly so-- I highly recommend simply linking a Twitter account to facilitate OnlyFans login.

Though I am in doubt it will work at all, the Google auth requires more debugging

## Content

I initially coded this tool to upload content from my Google Drive account. I setup my folders and the tool theresuch to find them so that I could organize my photos/videos in the the basic categories of: images, galleries, videos. This is a reflection of the purpose the content will be expressed with in OnlyFans- as images, galleries, and video uploads. It is rarer that the images folder is used, though it exists to specifically upload single images as messages to users more than as single file uploads. Galleries are the most common uploads to exist as content with videos being a likely close second.

All 'sources' which is how the tool recognizes locations to search for files [Google, Local, Dropbox, Remote], should follow the set out layout as described to properly utilize the way the OnlySnarf tool searches for files. However, it wouldn't be impossible to sort/search for files however you wish and simply utilize OnlySnarf to upload those files afterwards by specifying their input locations. So while this method works best for me, I hope it can work at all for others.



## Goals