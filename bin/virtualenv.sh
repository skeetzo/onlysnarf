#!/bin/bash
sudo apt-get install python3-venv python3-setuptools libjpeg-dev zlib1g-dev
python -m pip install --user virtualenv
virtualenv --python=/usr/bin/python3.10.6 venv
python -m pip install --upgrade pip setuptools wheel build twine
# python3 -m venv venv
# wait
# source venv/bin/activate
# pip install --upgrade pip
# pip install setuptools_rust
# deactivate
