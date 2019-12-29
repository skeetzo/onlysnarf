#!/usr/bin/env bash

# Image & Poll
echo "[*] Misc - Poll"
echo "############# Misc - Poll ##############">> ../onlysnarf/logs/tests.txt
sudo onlysnarfpy \
-debug \
-verbose \
-verboser \
-action "upload" -type "image" \
-skip-download \
-text "poll testes" \
-duration 3 \
-questions "your mom","some toast","a nice sandwich" \
-debug-delay \
-$1 \
-debug-force >> ../onlysnarf/logs/tests.txt 2>&1
# -show-window