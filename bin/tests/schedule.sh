#!/usr/bin/env bash

# Schedule
echo "[*] Misc - Schedule"
sudo onlysnarfpy \
-debug \
-action "post" -category "image" \
-bykeyword "pussycats" \
-skip-download \
-text "schedule testes" \
-schedule "6-7-2020:6:26" \
-debug-delay \
-show \
-verbose -verbose -verbose
# -verbose
# -verbose -verbose

echo "[*] Misc - Schedule (Date & Time)"
sudo onlysnarfpy \
-debug \
-action "post" -category "image" \
-bykeyword "pussycats" \
-skip-download \
-text "schedule testes" \
-date "6-7-2020" \
-time "6:26" \
-debug-delay \
-show \
-verbose -verbose -verbose
# -verbose
# -verbose -verbose

echo "[*] Misc - Schedule (Date)"
sudo onlysnarfpy \
-debug \
-action "post" -category "image" \
-bykeyword "pussycats" \
-skip-download \
-text "schedule testes" \
-date "6-7-2020" \
-debug-delay \
-show \
-verbose -verbose -verbose
# -verbose
# -verbose -verbose