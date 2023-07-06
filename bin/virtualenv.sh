#!/bin/bash
# basic setup script for python3 virtual environments
sudo apt-get -y install python3-virtualenv python3-pip python3-venv python3-setuptools 

# TODO:
# are these required still?
# sudo apt-get -y install libjpeg-dev zlib1g-dev

python3 -m pip install --user virtualenv
virtualenv venv
echo "This script fails to update source automatically so copy and paste or type the following code to update the virtual environment for development:"
echo "source venv/bin/activate"
echo "python -m pip install --upgrade pip setuptools wheel build twine pytest"