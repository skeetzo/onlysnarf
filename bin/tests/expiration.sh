#!/usr/bin/env bash

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
-source "$2" \
"$1" \
"$3"

echo "[*] Misc - Expiration"
onlysnarfpy \
-debug \
-action "post" -category "image" \
-bykeyword "pussycats" \
-skip-upload \
-debug-delay \
-expiration 3 \
-source "$2" \
"$1" \
"$3"