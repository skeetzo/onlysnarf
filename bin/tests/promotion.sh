#!/usr/bin/env bash

# Promotion
echo "[*] Promotion - Free Trial"
onlysnarfpy \
-debug \
-action "promotion" \
-user "recent" \
-promotion "trial" \
-duration "6 months" \
-limit 0 \
-promotion-expiration 0 \
-prefer-local \
-keep \
-show \
-verbose -verbose -verbose \
-browser "$1" \
-source "$2"

# Promotion
# echo "[*] Promotion - Campaign"
# onlysnarfpy \
# -debug \
# -action "discount" \
# -user "recent" \
# -promotion "campaign" \
# -amount 40 \
# -expiration 9 \
# -limit 5 \
# -prefer-local \
# -keep \
# -show \
# -verbose -verbose -verbose \
# -browser "$1" \
# -source "$2"