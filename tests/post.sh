#!/usr/bin/env bash

# Post
echo "[*] Post - Text"
echo "############# Post - Text ########################">> ../onlysnarf/logs/tests.txt
sudo onlysnarfpy \
-debug \
-verbose \
-verboser \
-action "post" \
-$1 \
-text "post testes" >> ../onlysnarf/logs/tests.txt 2>&1
# -show-window