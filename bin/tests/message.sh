#!/usr/bin/env bash

echo "[*] Message - Recent & Image"
sudo onlysnarfpy \
-debug \
-action "message" \
-user "all" \
-category "image" \
-bykeyword "pussycats" \
-price "4.00" \
-prefer-local \
-recent-users-count 1 \
-show \
-verbose -verbose -verbose
# -verbose -verbose
# -verbose

echo "[*] Message - Recent & Gallery"
sudo onlysnarfpy \
-debug \
-action "message" \
-user "recent" \
-category "gallery" \
-notkeyword "dick" \
-text "message testes" \
-price "6.00" \
-prefer-local \
-recent-users-count 1 \
-show \
-verbose -verbose -verbose
# -verbose -verbose
# -verbose

echo "[*] Message - All & Video"
sudo onlysnarfpy \
-debug \
-action "message" \
-user "all" \
-category "video" \
-notkeyword "stroke" \
-text "message testes" \
-price "10.00" \
-prefer-local \
-show \
-verbose -verbose -verbose
# -verbose -verbose
# -verbose
