#!/usr/bin/env bash

# Post
echo "[*] Post - Text"
sudo onlysnarfpy \
-debug \
-$2 \
-action "post" \
-$1 \
-text "post testes"

# Image
echo "[*] Upload - Image"
sudo onlysnarfpy \
-debug \
-$2 \
-action "post" -category "image" \
-bykeywords "pussycats" \
-text "image testes" \
-$1 \
-debug-delay

# Gallery
echo "[*] Upload - Gallery"
sudo onlysnarfpy \
-debug \
-$2 \
-action "post" -category "gallery" \
-bykeywords "pussycats" \
-text "gallery testes" \
-$1 \
-debug-delay

# Video
echo "[*] Upload - Video"
sudo onlysnarfpy \
-debug \
-$2 \
-action "post" -category "video" \
-bykeywords "pussycats" \
-text "video testes" \
-$1 \
-debug-delay