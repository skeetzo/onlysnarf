#!/usr/bin/env bash

# Promotion
echo "[*] Promotion - Free Trial"
onlysnarfpy \
-debug \
-action "promotion" \
-user "recent" \
-promotion "trial" \
-duration "6 months" \
-promotion-limit 0 \
-promotion-expiration 0 \
-prefer-local \
-keep \
-verbose -verbose -verbose \
-browser "$1" \
-source "$2"
# -show \

# Promotion
echo "[*] Promotion - Campaign"
onlysnarfpy \
-debug \
-action "promotion" \
-user "recent" \
-promotion "campaign" \
-amount 40 \
-promotion-expiration 0 \
-promotion-limit 0 \
-text "fuck balls" \
-debug-delay \
-prefer-local \
-keep \
-verbose -verbose -verbose \
-browser "$1" \
-source "$2"
# -show \