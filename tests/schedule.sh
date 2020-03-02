#!/usr/bin/env bash

# Schedule
echo "[*] Misc - Schedule"
sudo onlysnarfpy \
-debug \
-verbose \
-verboser \
-verbosest \
-action "upload" -type "image" \
-skip-download \
-text "schedule testes" \
-schedule "6/6/2020:6:26" \
-debug-delay \
-$1 \
-debug-force