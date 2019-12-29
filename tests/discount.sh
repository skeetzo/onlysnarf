#!/usr/bin/env bash

# Discount
echo "[*] Discount - Recent"
echo "############# Discount - Recent ##################">> ../onlysnarf/logs/tests.txt
sudo onlysnarfpy \
-debug \
-verbose \
-action "discount" \
-user "recent" \
-amount 40 \
-$1 \
-months 3 >> ../onlysnarf/logs/tests.txt 2>&1
# -prefer-local