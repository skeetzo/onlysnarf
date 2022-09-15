#!/usr/bin/env bash
# git filter-branch -f --tree-filter 'rm -rf ./OnlySnarf/google_creds.txt' HEAD

rm -rf dist/ build/ *.egg-info

# project logs
rm -rf log/* $HOME/OnlySnarf/snarf.log $HOME/.onlysnarf/log/* 

# session data and cookies
rm -rf $HOME/.onlysnarf/session.json $HOME/.onlysnarf/cookies.pkl

# any remaining files
rm -rf $HOME/OnlySnarf/downloads/* $HOME/OnlySnarf/uploads/*