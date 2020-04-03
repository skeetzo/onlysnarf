#!/usr/bin/env bash

# Image & Poll
echo "[*] Misc - Poll"
sudo onlysnarfpy \
-debug \
-action "post" -category "image" \
-bykeyword "pussycats" \
-skip-download \
-text "poll testes" \
-duration 7 \
-question "your mom" \
-question "some toast" \
-question "a nice sandwich" \
-debug-delay \
-verbose
# -verbose -verbose -verbose
# -show \
# -verbose -verbose