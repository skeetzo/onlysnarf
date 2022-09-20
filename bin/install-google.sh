#!/usr/bin/env bash
VERSION="81.0.4044.69"
VERSION2="81.0.4044.129"
VERSION3="106.0.5249.21"
# VERSION="83.0.4103.14.0"
# VERSION="83.0.4103.23"
# VERSION2="81.0.4044.92"

sudo apt-get remove google-chrome-stable --purge -y
sudo apt-get remove google-chrome-beta --purge -y
pip uninstall chromedriver-binary -y

wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt-get update

# sudo apt-get install -y google-chrome-stable
sudo apt-get install -y google-chrome-beta
pip install chromedriver-binary

# sudo apt-get install google-chrome-stable=$VERSION2-1 -y
# sudo apt-get install google-chrome-beta=$VERSION2-1 -y
# sudo -H pip3 install chromedriver-binary==$VERSION.0 --force --upgrade

# or
# Chrome 			Chromedriver
# 81.0.4044.129  |  81.0.4044.69
# version=$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
# wget -qP "/tmp/" "https://chromedriver.storage.googleapis.com/${version}/chromedriver_linux64.zip"
# sudo unzip -o /tmp/chromedriver_linux64.zip -d /usr/bin

echo "
"
bin/check-google.sh