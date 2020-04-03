#!/usr/bin/env bash

# Image & Expiration
echo "[*] Misc - Expiration"
sudo onlysnarfpy \
-debug \
-action "post" -category "image" \
-bykeyword "pussycats" \
-skip-download \
-text "expiration testes" \
-debug-delay \
-expiration 3 \
-show \
-verbose -verbose -verbose
# -verbose -verbose
# -verbose

echo "[*] Misc - Expiration"
sudo onlysnarfpy \
-debug \
-action "post" -category "image" \
-bykeyword "pussycats" \
-skip-upload \
-debug-delay \
-expiration 3 \
-show \
-verbose -verbose -verbose
# -verbose -verbose
# -verbose