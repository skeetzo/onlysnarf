#!/usr/bin/env bash
# doesn't work and unnecessary
# handled by:
# import geckodriver_autoinstaller
# geckodriver_autoinstaller.install()
###############################
wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux32.tar.gz -O /tmp/geckodriver.tar.gz
# sudo tar -C /opt -xvzf /tmp/geckodriver.tar.gz
sudo tar -xvzf /tmp/geckodriver*
sudo chmod +x ./geckodriver
# sudo chmod 755 ./geckodriver
sudo mv geckodriver /usr/local/bin/