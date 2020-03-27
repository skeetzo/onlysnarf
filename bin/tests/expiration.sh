#!/usr/bin/env bash

# Image & Expiration
echo "[*] Misc - Expiration"
sudo onlysnarfpy \
-debug \
-$2 \
-action "post" -category "image" \
-bykeyword "pussycats" \
-skip-download \
-text "expiration testes" \
-debug-delay \
-$1 \
-expires 3