#!/usr/bin/env bash

# Image
echo "[*] Upload - Image"
onlysnarfpy \
-debug \
-action "post" -category "image" \
-bykeyword "test" \
-text "image testes" \
-keywords "ballsacks" -keywords "tits" \
-tags "sexy" \
-performers "justalexxxd" \
-debug-delay \
-keep \
-verbose -verbose -verbose \
-browser "$1" \
-source "$2"

# Gallery
echo "[*] Upload - Gallery"
onlysnarfpy \
-debug \
-action "post" -category "gallery" \
-bykeyword "test" \
-text "gallery testes" \
-performers "balls" -performers "sacks" \
-debug-delay \
-keep \
-verbose -verbose -verbose \
-browser "$1" \
-source "$2"

# Video
echo "[*] Upload - Video"
onlysnarfpy \
-debug \
-action "post" -category "video" \
-bykeyword "test" \
-text "fuck my upload speeds in the face" \
-debug-delay \
-keep \
-verbose -verbose -verbose \
-browser "$1" \
-source "$2"