#!/bin/bash
# doesn't work

echo "removing chromium-browser"
sudo apt-get purge chromium-browser
rm ~/.config/chromium/ -rf
echo "removing chrome"
sudo apt-get purge google-chrome-stable
rm ~/.config/google-chrome/ -rf
sudo apt-get install libxss1 libappindicator1 libindicator7
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome*.deb
echo "installing Chrome"
echo "getting libxi6"
sudo apt-get install libxi6 libgconf-2-4
echo "getting chromedriver"
wget -N https://launchpad.net/ubuntu/trusty/armhf/chromium-chromedriver/65.0.3325.181-0ubuntu0.14.04.1 chromedriver
echo "unzipping chromedriver"
unzip chromedriver*.zip
echo "exe chromedriver"
chmod +x chromedriver
echo "removing /usr/local/share/chromedriver"
sudo rm -rf /usr/local/share/chromedriver
echo "removing /usr/local/bin/chromedriver"
sudo rm -rf /usr/local/bin/chromedriver
echo "removing /usr/bin/chromedriver"
sudo rm -rf /usr/bin/chromedriver
echo "moving chromedriver to local/share"
sudo mv -f chromedriver /usr/local/share/chromedriver
echo "linking to bin"
sudo ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
echo "linking to local bin"
sudo ln -s /usr/local/share/chromedriver /usr/bin/chromedriver




# wget https://launchpad.net/ubuntu/trusty/armhf/chromium-chromedriver/34.0.1847.116-0ubuntu2
# dpkg -i chromium-chromedriver*.deb
# Then chromedriver will be available in /usr/lib/chromium-browser/chromedriver