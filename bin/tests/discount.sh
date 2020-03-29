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
-show \
-verbose -verbose -verbose
# -verbose
# -verbose -verbose