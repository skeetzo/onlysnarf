#!/usr/bin/env bash

echo "[*] Message - Recent & Image"
onlysnarfpy \
-debug \
-action "message" \
-user "all" \
-category "image" \
-bykeyword "pussycats" \
-price "4.00" \
-prefer-local \
-recent-users-count 1 \
-keep \
-verbose -verbose -verbose \
-browser "$1" \
-source "$2"
# -show \

echo "[*] Message - Recent & Gallery"
onlysnarfpy \
-debug \
-action "message" \
-user "recent" \
-category "gallery" \
-notkeyword "dick" \
-text "message testes" \
-price "6.00" \
-prefer-local \
-recent-users-count 1 \
-keep \
-verbose -verbose -verbose \
-browser "$1" \
-source "$2"
# -show \

echo "[*] Message - All & Video"
onlysnarfpy \
-debug \
-action "message" \
-user "all" \
-category "video" \
-notkeyword "stroke" \
-text "message testes" \
-price "10.00" \
-prefer-local \
-keep \
-verbose -verbose -verbose \
-browser "$1" \
-source "$2"
# -show \