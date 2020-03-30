#!/usr/bin/env bash

# Users Recent - Image
echo "[*] Message - Recent & Image"
sudo onlysnarfpy \
-debug \
-action "message" \
-user "all" \
-force-upload \
-category "image" \
-text "message testes" \
-price "2.00" \
-show \
-verbose -verbose -verbose
# -verbose
# -verbose -verbose

# User
echo "[*] Message - User & Gallery"
sudo onlysnarfpy \
-debug \
-action "message" \
-bykeyword "pussycats" \
-user "1578380" \
-category "gallery" \
-text "message testes" \
-price "2.00" \
-prefer-local \
-show \
-verbose -verbose -verbose
# -verbose
# -verbose -verbose
