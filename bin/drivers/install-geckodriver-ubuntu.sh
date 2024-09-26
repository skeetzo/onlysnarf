#!/usr/bin/env bash
geckodriver_version="0.35.0"
wget "https://github.com/mozilla/geckodriver/releases/download/v$geckodriver_version/geckodriver-v$geckodriver_version-linux64.tar.gz"
tar -xvf "geckodriver-v$geckodriver_version-linux64.tar.gz"
sudo mv geckodriver /usr/local/bin/