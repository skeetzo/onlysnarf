#!/usr/bin/env bash
# sudo cp ../onlysnarf/OnlySnarf/config.conf /etc/onlysnarf
sudo python3 setup.py install
sudo onlysnarf -debug -show-window -debug-delay