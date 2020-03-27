#!/usr/bin/env bash

# Schedule
echo "[*] Misc - Schedule"
sudo onlysnarfpy \
-debug \
-$2 \
-action "upload" -category "image" \
-bykeyword "pussycats" \
-skip-download \
-text "schedule testes" \
-schedule "6/6/2020:6:26" \
-debug-delay \
-$1 