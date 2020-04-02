#!/usr/bin/env bash

# Users Recent - Image
echo "[*] Message - Recent & Image"
sudo onlysnarfpy \
-debug \
-action "message" \
-user "recent" \
-force-upload \
-category "image" \
-text "message testes" \
-bykeyword "pussycats" \
-price "2.00" \
-show \
-verbose -verbose -verbose
# -verbose -verbose
# -verbose

# User
echo "[*] Message - Recent & Gallery"
sudo onlysnarfpy \
-debug \
-action "message" \
-user "recent" \
-category "gallery" \
-text "message testes" \
-price "6.00" \
-prefer-local \
-show \
-verbose -verbose -verbose
# -verbose -verbose
# -verbose
