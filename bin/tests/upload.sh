#!/usr/bin/env bash

# Image
echo "[*] Upload - Image"
sudo onlysnarfpy \
-debug \
-action "post" -category "image" \
-bykeyword "pussycats" \
-text "image testes" \
-debug-delay \
-show \
-verbose -verbose -verbose
# -verbose
# -verbose -verbose

# Gallery
echo "[*] Upload - Gallery"
sudo onlysnarfpy \
-debug \
-action "post" -category "gallery" \
-bykeyword "pussycats" \
-text "gallery testes" \
-debug-delay \
-show \
-verbose -verbose -verbose
# -verbose
# -verbose -verbose

# Video
echo "[*] Upload - Video"
sudo onlysnarfpy \
-debug \
-action "post" -category "video" \
-bykeyword "pussycats" \
-text "video testes" \
-debug-delay \
-show \
-verbose -verbose -verbose
# -verbose
# -verbose -verbose