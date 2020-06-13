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
-verbose -verbose -verbose
# -show \
# -verbose -verbose
# -verbose

echo "[*] Misc - Expiration"
onlysnarfpy \
-debug \
-action "post" -category "image" \
-bykeyword "pussycats" \
-skip-upload \
-debug-delay \
-expiration 3 \
-verbose -verbose -verbose
# -show \
# -verbose -verbose
# -verbose