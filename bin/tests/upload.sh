#!/usr/bin/env bash

# Image
echo "[*] Upload - Image"
sudo onlysnarfpy \
-debug \
-action "post" -category "image" \
-bykeywords "pussycats" \
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
-bykeywords "pussycats" \
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
-bykeywords "pussycats" \
-text "video testes" \
-debug-delay \
-show \
-verbose -verbose -verbose
# -verbose
# -verbose -verbose