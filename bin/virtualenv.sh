#!/bin/bash
sudo apt-get -y install python3-virtualenv python3-pip python3-venv python3-setuptools libjpeg-dev zlib1g-dev
python3 -m pip install --user virtualenv
virtualenv venv
echo "run:"
echo "source venv/bin/activate"
echo "python -m pip install --upgrade pip setuptools wheel build twine pytest"
# python3 -m venv venv
# wait
# source venv/bin/activate
# pip install --upgrade pip
# pip install setuptools_rust
# deactivate
