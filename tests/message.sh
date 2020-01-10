#!/usr/bin/env bash

# Users Recent - Image
echo "[*] Message - Recent & Image"
sudo onlysnarfpy \
-debug \
-verbose \
-verboser \
-action "message" \
-method "recent" \
-type "image" \
-text "message testes" \
-$1 \
-price "2.00"

# User
echo "[*] Message - User & Gallery"
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
-prefer-local
