#!/usr/bin/env bash
rm -rf dist/ build/ *.egg-info geckodriver.log log/*
# git filter-branch -f --tree-filter 'rm -rf ./OnlySnarf/google_creds.txt' HEAD
rm $HOME/OnlySnarf/*.log $HOME/.onlysnarf/log/*