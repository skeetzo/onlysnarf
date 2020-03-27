#!/usr/bin/env bash

# Users Recent - Image
echo "[*] Message - Recent & Image"
sudo onlysnarfpy \
-debug \
-$2 \
-action "message" \
-user "all" \
-force-upload \
-category "image" \
-text "message testes" \
-$1 \
-price "2.00"

# User
echo "[*] Message - User & Gallery"
sudo onlysnarfpy \
-debug \
-$2 \
-action "message" \
-bykeywords "pussycats" \
-user "1578380" \
-category "gallery" \
-text "message testes" \
-price "2.00" \
-$1 \
-prefer-local
