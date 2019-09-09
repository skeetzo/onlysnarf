#!/usr/bin/env bash
sudo onlysnarf/bin/clean.sh
git add . && git commit -m $1 && git push