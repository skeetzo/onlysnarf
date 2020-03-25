#!/usr/bin/env bash

# Discount
echo "[*] Discount - Recent"
sudo onlysnarfpy \
-debug \
-verbose \
-verboser \
-verbosest \
-action "discount" \
-user "recent" \
-amount 40 \
-$1 \
-months 3
# -prefer-local