#!/usr/bin/env bash

# Image & Poll
echo "[*] Misc - Poll 1"
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
-verbose -verbose -verbose
# -verbose
# -show \
# -verbose -verbose

echo "[*] Misc - Poll 2"
sudo onlysnarfpy \
-debug \
-action "post" -category "image" \
-bykeyword "pussycats" \
-duration 7 \
-question "your mom" \
-question "some toast" \
-question "a nice sandwich1" \
-question "a nice sandwich2" \
-question "a nice sandwich3" \
-question "a nice sandwich4" \
-question "a nice sandwich5" \
-debug-delay \
-verbose -verbose -verbose
# -verbose
# -show \
# -verbose -verbose