#!/usr/bin/env bash
rm -rf dist/ build/ *.egg-info logs
mkdir ../onlysnarf/logs
# git filter-branch -f --tree-filter 'rm -rf ./OnlySnarf/config.conf' HEAD