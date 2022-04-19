#!/usr/bin/env bash

echo "[*] Misc - Poll 0"
onlysnarfpy \
-debug \
-action "post" -category "image" \
-skip-download \
-text "poll testes" \
-duration 7 \
-question "your mom" \
-question "some toast" \
-question "a nice sandwich" \
-debug-delay \
-keep \
-verbose -verbose -verbose \
-browser "$1"

# Image & Poll
echo "[*] Misc - Poll 1"
onlysnarfpy \
-debug \
-action "post" -category "image" \
-skip-download \
-text "poll testes" \
-duration 7 \
-question "your mom" \
-question "some toast" \
-question "a nice sandwich" \
-debug-delay \
-keep \
-verbose -verbose -verbose \
-browser "$1" \
-source "$2"

echo "[*] Misc - Poll 2"
onlysnarfpy \
-debug \
-action "post" -category "image" \
-skip-download \
-duration 7 \
-question "your mom" \
-question "some toast" \
-question "a nice sandwich1" \
-question "a nice sandwich2" \
-question "a nice sandwich3" \
-question "a nice sandwich4" \
-question "a nice sandwich5" \
-debug-delay \
-keep \
-verbose -verbose -verbose \
-browser "$1" \
-source "$2"
