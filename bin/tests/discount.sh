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
"$1"