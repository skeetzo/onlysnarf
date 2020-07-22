#!/usr/bin/env bash

# Post
echo "[*] Post - Text"
onlysnarfpy \
-debug \
-action "post" \
-text "post testes" \
-source "$2" \
"$1" \
"$3"
# -show \
# -verbose
# -verbose -verbose -verbose
# -verbose -verbose

echo "[*] Post - No Text"
onlysnarfpy \
-debug \
-action "post" \
-source "$2" \
"$1" \
"$3"
# -show \
# -verbose
# -verbose -verbose -verbose
# -verbose -verbose