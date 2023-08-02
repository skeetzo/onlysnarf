#!/bin/bash

# AWS Linux setup steps:

# ssh keys
ssh-keygen -t ed25519 -C "WebmasterSkeetzo@gmail.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
cat ~/.ssh/id_ed25519.pub
# > add to github

# basic dependencies
sudo yum -y install git python-pip

git clone git@github.com:skeetzo/onlysnarf --single-branch
sudo cp onlysnarf/notes/onlysnarf_api.service /etc/systemd/system
sudo systemctl start onlysnarf_api.service
sudo systemctl enable onlysnarf_api.service

# add user
sudo useradd -m snarf
sudo passwd snarf
su snarf

pip install onlysnarf