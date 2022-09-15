#!/usr/bin/env bash
rm -rf dist/ build/ *.egg-info geckodriver.log log/*
# git filter-branch -f --tree-filter 'rm -rf ./OnlySnarf/google_creds.txt' HEAD

# project logs
rm $HOME/OnlySnarf/snarf.log $HOME/.onlysnarf/log/*

# session data and cookies
rm $HOME/.onlysnarf/session.json $HOME/.onlysnarf/cookies.pkl

# any remaining files
rm $HOME/OnlySnarf/downloads/* $HOME/OnlySnarf/uploads/*