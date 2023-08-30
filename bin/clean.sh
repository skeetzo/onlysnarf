#!/usr/bin/env bash
# git filter-branch -f --tree-filter 'rm -rf ./OnlySnarf/google_creds.txt' HEAD

rm -rf dist/ build/ *.egg-info .pytest_cache

# project logs
rm -rf log/* $HOME/OnlySnarf/snarf.log $HOME/.onlysnarf/log/* 

# session data and cookies
rm -rf $HOME/.onlysnarf/session.json $HOME/.onlysnarf/cookies.pkl

# any remaining files
# rm -rf $HOME/OnlySnarf/downloads/* $HOME/OnlySnarf/uploads/*

rm -rf OnlySnarf/__pycache__ OnlySnarf/classes/__pycache__ OnlySnarf/classes/webdriver/__pycache__ OnlySnarf/lib/__pycache__ OnlySnarf/util/__pycache__