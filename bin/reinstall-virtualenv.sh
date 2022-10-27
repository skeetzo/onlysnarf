#!/bin/bash

deactivate
sudo rm -r venv
virtualenv --python=/usr/local/bin/python3.8 venv

# this still doesn't work in termial
source venv/bin/activate
exec $SHELL



python -m pip install --upgrade pip setuptools wheel build twine
python -m pip install -e .[dev]