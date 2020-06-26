#!/usr/bin/env bash

# Post
echo "[*] Post - Text"
onlysnarfpy \
-debug \
-action "post" \
-text "post testes" \
"$1" \
"$2"
# -show \
# -verbose
# -verbose -verbose -verbose
# -verbose -verbose

echo "[*] Post - No Text"
onlysnarfpy \
-debug \
-action "post" \
"$1" \
"$2"
# -show \
# -verbose
# -verbose -verbose -verbose
# -verbose -verbose