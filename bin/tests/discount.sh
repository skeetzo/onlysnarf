#!/usr/bin/env bash

# Discount
echo "[*] Discount - Recent"
onlysnarfpy \
-debug \
-action "discount" \
-user "recent" \
-amount 40 \
-months 3 \
-prefer-local \
-keep \
-verbose -verbose -verbose \
-browser "$1" \
-source "$2"
# -show \