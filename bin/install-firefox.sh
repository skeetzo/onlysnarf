#!/usr/bin/env bash
wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux32.tar.gz -O /tmp/geckodriver.tar.gz
sudo tar -C /opt -xzf /tmp/geckodriver.tar.gz
sudo chmod 755 /opt/geckodriver
sudo ln -fs /opt/geckodriver /usr/bin/geckodriver
sudo ln -fs /opt/geckodriver /usr/local/bin/geckodriver