#!/usr/bin/env bash
# ../onlysnarf/bin/save.sh
# rm -rf dist/ build/ *.egg-info
git filter-branch -f --tree-filter 'rm -rf ./OnlySnarf/config.conf' HEAD