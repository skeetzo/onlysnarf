#!/usr/bin/env bash

# Schedule
echo "[*] Misc - Schedule"
echo "############# Misc - Schedule ##########">> ../onlysnarf/logs/tests.txt
sudo onlysnarfpy \
-debug \
-verbose \
-verboser \
-action "upload" -type "image" \
-skip-download \
-text "schedule testes" \
-schedule "6/6/2020:6:26" \
-debug-delay \
-$1 \
-debug-force >> ../onlysnarf/logs/tests.txt 2>&1
# -show-window