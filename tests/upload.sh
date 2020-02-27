#!/usr/bin/env bash

# Image
echo "[*] Upload - Image"
sudo onlysnarfpy \
-debug \
-$2 \
-action "upload" -type "image" \
-text "image testes" \
-$1 \
-debug-delay

# Gallery
echo "[*] Upload - Gallery"
sudo onlysnarfpy \
-debug \
-$2 \
-action "upload" -type "gallery" \
-text "gallery testes" \
-$1 \
-debug-delay

# Video
echo "[*] Upload - Video"
sudo onlysnarfpy \
-debug \
-$2 \
-action "upload" -type "video" \
-text "video testes" \
-skip-reduce \
-$1 \
-quietdev \
-debug-delay