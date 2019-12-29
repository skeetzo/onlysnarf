#!/usr/bin/env bash

# Users Recent - Image
echo "[*] Message - Recent & Image"
echo "############# Message - Recent & Image #########">> ../onlysnarf/logs/tests.txt
sudo onlysnarfpy \
-debug \
-verbose \
-verboser \
-action "message" \
-method "recent" \
-type "image" \
-text "message testes" \
-$1 \
-price "2.00" >> ../onlysnarf/logs/tests.txt 2>&1
# -show-window

# User
echo "[*] Message - User & Gallery"
echo "############# Message - User & Gallery #####################">> ../onlysnarf/logs/tests.txt
sudo onlysnarfpy \
-debug \
-verbose \
-verboser \
-action "message" \
-method "user" \
-user "1578380" \
-type "gallery" \
-text "message testes" \
-price "2.00" \
-$1 \
-prefer-local >> ../onlysnarf/logs/tests.txt 2>&1
# -show-window 