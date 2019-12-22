#!/usr/bin/env bash
sudo apt-get remove google-chrome --purge -y
sudo apt-get remove google-chrome-stable --purge -y
sudo apt-get remove google-chrome-beta --purge -y
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt-get update 
sudo apt-get install google-chrome-beta -y

# Google Chrome 80.0.3987.16 beta

# If you are using Chrome version 80, please download ChromeDriver 80.0.3987.16
# If you are using Chrome version 79, please download ChromeDriver 79.0.3945.36
# If you are using Chrome version 78, please download ChromeDriver 78.0.3904.105
# ChromeDriver 77.0.3865.40s