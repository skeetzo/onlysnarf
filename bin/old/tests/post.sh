#!/usr/bin/env bash

# Post
echo "[*] Post - Text"
onlysnarfpy \
-debug \
-action "post" \
-text "post testes" \
-keep \
-verbose -verbose -verbose \
-browser "$1" \
-source "$2"

echo "[*] Post - No Text"
onlysnarfpy \
-debug \
-action "post" \
-keep \
-verbose -verbose -verbose \
-browser "$1" \
-source "$2"