#!/usr/bin/env bash
echo "Version Check:"
google-chrome --version | (echo -n "stable => " && cat)
google-chrome-beta --version | (echo -n "beta => " && cat)
pip show chromedriver-binary | grep "Version: " | (echo -n "binary => " && cat)