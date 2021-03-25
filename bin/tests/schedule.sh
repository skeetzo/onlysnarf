#!/usr/bin/env bash

# Schedule
echo "[*] Misc - Schedule"
onlysnarfpy \
-debug \
-action "post" -category "image" \
-bykeyword "pussycats" \
-skip-download \
-text "schedule testes" \
-schedule "6-6-2021:22:30" \
-debug-delay \
-keep \
-verbose -verbose -verbose \
-browser "$1" \
-source "$2"

echo "[*] Misc - Schedule (Date & Time)"
onlysnarfpy \
-debug \
-action "post" -category "image" \
-bykeyword "pussycats" \
-skip-download \
-text "schedule testes" \
-date "6-6-2021" \
-time "16:26" \
-debug-delay \
-keep \
-verbose -verbose -verbose \
-browser "$1" \
-source "$2"

echo "[*] Misc - Schedule (Date)"
onlysnarfpy \
-debug \
-action "post" -category "image" \
-bykeyword "pussycats" \
-skip-download \
-text "schedule testes" \
-date "6-6-2021" \
-debug-delay \
-keep \
-verbose -verbose -verbose \
-browser "$1" \
-source "$2"