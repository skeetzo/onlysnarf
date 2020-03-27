#!/usr/bin/env bash

# Schedule
echo "[*] Misc - Schedule"
sudo onlysnarfpy \
-debug \
-$2 \
-action "post" -category "image" \
-bykeywords "pussycats" \
-skip-download \
-text "schedule testes" \
-schedule "6/6/2020:6:26" \
-debug-delay \
-$1 