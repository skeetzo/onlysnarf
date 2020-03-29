#!/usr/bin/env bash

# Image & Expiration
echo "[*] Misc - Expiration"
sudo onlysnarfpy \
-debug \
-action "post" -category "image" \
-bykeywords "pussycats" \
-skip-download \
-text "expiration testes" \
-debug-delay \
-expiration 3 \
-$1 \
-verbose -verbose -verbose
# -verbose
# -verbose -verbose