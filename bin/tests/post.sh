#!/usr/bin/env bash

# Post
echo "[*] Post - Text"
sudo onlysnarfpy \
-debug \
-action "post" \
-text "post testes" \
-$1 \
-verbose -verbose -verbose
# -verbose
# -verbose -verbose

# Image
echo "[*] Upload - Image"
sudo onlysnarfpy \
-debug \
-action "post" -category "image" \
-bykeywords "pussycats" \
-text "image testes" \
-debug-delay \
-$1 \
-verbose -verbose -verbose
# -verbose
# -verbose -verbose

# Gallery
echo "[*] Upload - Gallery"
sudo onlysnarfpy \
-debug \
-action "post" -category "gallery" \
-bykeywords "pussycats" \
-text "gallery testes" \
-debug-delay \
-$1 \
-verbose -verbose -verbose
# -verbose
# -verbose -verbose

# Video
echo "[*] Upload - Video"
sudo onlysnarfpy \
-debug \
-action "post" -category "video" \
-bykeywords "pussycats" \
-text "video testes" \
-debug-delay \
-$1 \
-verbose -verbose -verbose
# -verbose
# -verbose -verbose