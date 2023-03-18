#!/bin/bash
# https://support.mozilla.org/en-US/kb/install-firefox-linux#w_install-firefox-from-mozilla-builds-for-advanced-users
wget https://www.mozilla.org/en-US/firefox/download/thanks/ -P ~/Downloads
cd ~/Downloads 
tar xjf firefox-*.tar.bz2 
sudo mv firefox /opt 
sudo ln -s /opt/firefox/firefox /usr/local/bin/firefox 
sudo wget https://raw.githubusercontent.com/mozilla/sumo-kb/main/install-firefox-linux/firefox.desktop -P /usr/local/share/applications 