#!/usr/bin/env bash

# Image & Expiration
echo "[*] Misc - Expiration"
echo "############# Misc - Expiration ########">> ../onlysnarf/logs/tests.txt
sudo onlysnarfpy \
-debug \
-verbose \
-verboser \
-action "upload" -type "image" \
-skip-download \
-text "expiration testes" \
-debug-delay \
-debug-force \
-$1 \
-expires 3 >> ../onlysnarf/logs/tests.txt 2>&1
# -show-window 