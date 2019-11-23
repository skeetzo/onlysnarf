#!/usr/bin/env bash
# sudo cp ../onlysnarf/OnlySnarf/config.conf /etc/onlysnarf
sudo python3 setup.py install
# sudo onlysnarf -debug -verbose -show-window -debug-delay -prefer-local
sudo onlysnarfpy -verbose -type gallery -notkeyword feet -show-window -debug -debug-delay