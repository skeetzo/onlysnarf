#!/bin/bash
# ubuntu dependencies
sudo apt-get install python3-setuptools libjpeg-dev zlib1g-dev
cp -r OnlySnarf/conf ~/.onlysnarf
# install with dev dependencies
# pip install -e .[dev]