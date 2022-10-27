#!/usr/bin/env bash

# didn't work

# https://stackoverflow.com/questions/65617246/issues-running-selenium-with-chromedriver-on-raspberry-pi-4
sudo apt install chromium-chromedriver
pip3 install selenium 
sudo chmod 755 /usr/lib/chromium-browser/chromedriver

sudo apt purge --remove chromium-browser -y
sudo apt autoremove && sudo apt autoclean -y
sudo apt install chromium-chromedriver

# https://serverfault.com/questions/1091926/running-chrome-on-ubuntu-server-how-to-solve-xdg-settings-not-found-using
 sudo apt-get install xdg-utils