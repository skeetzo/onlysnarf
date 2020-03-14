#!/usr/bin/env bash

# Image
echo "[*] Upload - Image"
sudo onlysnarfpy \
-debug \
-verbose \
-verboser \
-verbosest \
-action "upload" -type "image" \
-bykeyword "pussycats" \
-text "image testes" \
-$1 \
-debug-delay

# Gallery
echo "[*] Upload - Gallery"
sudo onlysnarfpy \
-debug \
-verbose \
-verboser \
-verbosest \
-action "upload" -type "gallery" \
-bykeyword "pussycats" \
-text "gallery testes" \
-$1 \
-debug-delay

# Video
echo "[*] Upload - Video"
sudo onlysnarfpy \
-debug \
-verbose \
-verboser \
-verbosest \
-action "upload" -type "video" \
-bykeyword "pussycats" \
-text "video testes" \
-skip-reduce \
-$1 \
-quietdev \
-debug-delay