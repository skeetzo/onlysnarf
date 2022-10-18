#!/usr/bin/env bash
VERSION="106.0.5249.21"

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
# sudo apt-get install google-chrome-stable=$VERSION2-1 -y
# sudo apt-get install google-chrome-beta=$VERSION2-1 -y
# pip install chromedriver-binary==$VERSION.0 --force --upgrade

echo "
"
MYDIR="$(dirname "$(realpath "$0")")"
$MYDIR/check-chrome.sh