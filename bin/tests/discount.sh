#!/usr/bin/env bash

# Discount
echo "[*] Discount - Recent"
sudo onlysnarfpy \
-debug \
-action "discount" \
-user "recent" \
-amount 40 \
-months 3 \
-prefer-local \
-verbose -verbose -verbose
# -show \
# -verbose -verbose
# -verbose