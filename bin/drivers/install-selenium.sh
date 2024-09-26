#!/usr/bin/env bash

# not necessary?
# echo "\n" | sudo add-apt-repository ppa:linuxuprising/java

sudo apt-get update
sudo apt-get install -y software-properties-common default-jre

# Selenium
selenium_version="4.24.0"
wget "https://github.com/SeleniumHQ/selenium/releases/download/selenium-$selenium_version/selenium-server-$selenium_version.jar"
# wget "http://selenium-release.storage.googleapis.com/$selenium_version/selenium-server-standalone-$selenium_version.jar"
sudo mv "selenium-server-$selenium_version.jar" "/opt/selenium-server-$selenium_version.jar"

# start server:
echo "to start selenium server:"
echo "java -jar /opt/selenium-server-$selenium_version.jar"
# -role hub

# copy updated service file
# start service for selenium server