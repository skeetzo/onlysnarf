#!/usr/bin/env bash

# Image
echo "[*] Upload - Image"
echo "############# Upload - Image ##############">> ../onlysnarf/logs/tests.txt
sudo onlysnarfpy \
-debug \
-verbose \
-verboser \
-action "upload" -type "image" \
-text "image testes" \
-$1 \
-debug-delay >> ../onlysnarf/logs/tests.txt 2>&1
# -show-window

# Gallery
echo "[*] Upload - Gallery"
echo "############# Upload - Gallery ##########">> ../onlysnarf/logs/tests.txt
sudo onlysnarfpy \
-debug \
-verbose \
-verboser \
-action "upload" -type "gallery" \
-text "gallery testes" \
-$1 \
-debug-delay >> ../onlysnarf/logs/tests.txt 2>&1
# -show-window

# Video
echo "[*] Upload - Video"
echo "############# Upload - Video ##########">> ../onlysnarf/logs/tests.txt
sudo onlysnarfpy \
-debug \
-verbose \
-verboser \
-action "upload" -type "video" \
-text "video testes" \
-skip-reduce \
-$1 \
-debug-delay >> ../onlysnarf/logs/tests.txt 2>&1
# -show-window