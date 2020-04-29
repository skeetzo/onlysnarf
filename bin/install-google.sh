#!/usr/bin/env bash
# VERSION1="81.0.4044.69"
# VERSION2="81.0.4044.129"
# VERSION="83.0.4103.14"
# VERSION="83.0.4103.23"

sudo apt-get remove google-chrome-stable --purge -y
sudo apt-get remove google-chrome-beta --purge -y
sudo -H pip3 uninstall chromedriver-binary -y

wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt-get update

sudo apt-get install -y google-chrome-beta
sudo -H pip3 install chromedriver-binary --force --upgrade

# sudo apt-get install google-chrome-beta=$VERSION2 -y
# sudo -H pip3 install chromedriver-binary==$VERSION1 --force --upgrade

echo "
"
bin/check-google.sh