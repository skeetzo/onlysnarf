#!/usr/bin/env bash
rm -rf dist/ build/ *.egg-info
# git filter-branch -f --tree-filter 'rm -rf ./OnlySnarf/config.conf' HEAD