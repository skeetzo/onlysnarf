#!/usr/bin/env bash
rm -rf dist/ build/ *.egg-info geckodriver.log
# git filter-branch -f --tree-filter 'rm -rf ./OnlySnarf/config.conf' HEAD