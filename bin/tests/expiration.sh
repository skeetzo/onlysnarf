#!/usr/bin/env bash

# Image & Expiration
echo "[*] Misc - Expiration"
sudo onlysnarfpy \
-debug \
-$2 \
-action "post" -category "image" \
-bykeywords "pussycats" \
-skip-download \
-text "expiration testes" \
-debug-delay \
-$1 \
-expiration 3