#!/usr/bin/env bash

echo $1

# Image & Expiration
echo "[*] Misc - Expiration"
onlysnarfpy \
-debug \
-action "post" -category "image" \
-bykeyword "pussycats" \
-skip-download \
-text "expiration testes" \
-debug-delay \
-expiration 3 \
"$1" \

echo "[*] Misc - Expiration"
onlysnarfpy \
-debug \
-action "post" -category "image" \
-bykeyword "pussycats" \
-skip-upload \
-debug-delay \
-expiration 3 \
"$1"
