#!/usr/bin/env bash
# https://raspberrypi.stackexchange.com/questions/63258/selenium-firefox-oserror-errno-8-exec-format-error
wget "https://github.com/mozilla/geckodriver/releases/download/v0.19.1/geckodriver-v0.19.1-arm7hf.tar.gz" -O /tmp/geckodriver.tar.gz
sudo tar -xvzf /tmp/geckodriver*
sudo chmod +x ./geckodriver
sudo mv ./geckodriver /usr/local/bin/