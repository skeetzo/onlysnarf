#!/usr/bin/env bash
rm -rf dist/ build/ *.egg-info
git filter-branch --tree-filter 'rm -rf /home/skeetzo/Projects/onlysnarf/OnlySnarf/profile.conf' HEAD