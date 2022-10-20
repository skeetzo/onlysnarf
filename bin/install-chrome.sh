#!/usr/bin/env bash

sudo apt-get remove google-chrome-stable --purge -y
sudo apt-get remove google-chrome-beta --purge -y
pip uninstall chromedriver-binary -y

#
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
# echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
# sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
# sudo sh -c "echo 'deb http://dl.google.com/linux/chrome/deb/ stable main' >>   /etc/apt/sources.list"
sudo apt-get update
#

# sudo apt-get install -y google-chrome-stable
sudo apt-get install -y google-chrome-beta
pip install chromedriver-binary

## by version
# VERSION="106.0.5249.21"
# sudo apt-get install google-chrome-stable=$VERSION-1 -y
# sudo apt-get install google-chrome-beta=$VERSION-1 -y
# pip install chromedriver-binary==$VERSION.0 --force --upgrade



## didn't work for rpi4
# or
# Chrome 			Chromedriver
# 81.0.4044.129  |  106.0.5249.61
version=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget -qP "/tmp/" "https://chromedriver.storage.googleapis.com/${version}/chromedriver_linux64.zip"
sudo apt-get install unzip
sudo unzip -o /tmp/chromedriver_linux64.zip -d /usr/bin

echo "
"
MYDIR="$(dirname "$(realpath "$0")")"
$MYDIR/check-chrome.sh