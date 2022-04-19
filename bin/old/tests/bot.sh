#!/usr/bin/env bash

echo "[*] Bot"
onlysnarfpy \
-debug \
-action "bot" \
-user "recent" \
-prefer-local \
-keep \
-verbose -verbose -verbose \
-browser "$1" \
-source "$2"
# -show \