#!/bin/bash
# doesn't work

sudo apt-get upgrade
sudo apt-get update
sudo pip3 install selenium
sudo apt-get install iceweasel
curl -O https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-arm7hf.tar.gz
tar -xzvf geckodriver-v0.19.1-arm7hf.tar.gz
sudo cp geckodriver /usr/local/bin/