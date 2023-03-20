#!/usr/bin/env bash
###############################
VERSION="0.31.0"
BIT="64"
#
wget "https://github.com/mozilla/geckodriver/releases/download/v$VERSION/geckodriver-v$VERSION-linux$BIT.tar.gz" -O /tmp/geckodriver.tar.gz
# sudo tar -C /opt -xvzf /tmp/geckodriver.tar.gz
sudo tar -xvzf /tmp/geckodriver*
sudo chmod +x ./geckodriver
# sudo chmod 755 ./geckodriver
sudo mv ./geckodriver /usr/local/bin/