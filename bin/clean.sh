#!/usr/bin/env bash
rm -rf dist/ build/ *.egg-info
git filter-branch --tree-filter 'rm -rf ./OnlySnarf/profile.conf' HEAD