#!/usr/bin/env bash

# Discount
echo "[*] Discount - Recent"
onlysnarfpy \
-debug \
-action "discount" \
-user "recent" \
-amount 40 \
-months 3 \
-keep \
-prefer-local \
-verbose -verbose -verbose \
-browser "$1" \
-source "$2"
# -show \