#!/usr/bin/env bash

# Image & Poll
echo "[*] Misc - Poll"
sudo onlysnarfpy \
-debug \
-verbose \
-verboser \
-verbosest \
-action "upload" -type "image" \
-bykeyword "pussycats" \
-skip-download \
-text "poll testes" \
-duration 3 \
-questions "your mom","some toast","a nice sandwich" \
-debug-delay \
-$1 \
-debug-force
