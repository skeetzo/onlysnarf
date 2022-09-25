#!/usr/bin/env bash
echo "Firefox Version Check:"
geckodriver --version | head -n 1 | (echo -n "geckodriver => " && cat)