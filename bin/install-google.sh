#!/usr/bin/env bash
sudo apt-get remove google-chrome --purge -y
sudo apt-get remove google-chrome-stable --purge -y
sudo apt-get remove google-chrome-beta --purge -y
sudo -H pip3 uninstall chromedriver-binary -y
# wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
# echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt-get update 
# sudo apt-get install google-chrome-beta -y
# sudo -H pip3 install chromedriver-binary --force --upgrade
sudo apt-get install google-chrome-beta=80.0.3987.16-1 -y
sudo -H pip3 install chromedriver-binary==80.0.3987.16 --force --upgrade
bin/check-google.sh