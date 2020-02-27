#!/usr/bin/env bash

# Image & Expiration
echo "[*] Misc - Expiration"
sudo onlysnarfpy \
-debug \
-$2 \
-action "upload" -type "image" \
-skip-download \
-text "expiration testes" \
-debug-delay \
-debug-force \
-$1 \
-expires 3