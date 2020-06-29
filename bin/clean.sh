#!/usr/bin/env bash
rm -rf dist/ build/ *.egg-info geckodriver.log
# git filter-branch -f --tree-filter 'rm -rf ./OnlySnarf/google_creds.txt' HEAD