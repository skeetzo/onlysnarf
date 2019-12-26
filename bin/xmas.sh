#!/usr/bin/env bash
# messages all users a non nude teaser for free
# and a nude for $10
sudo python3 ../onlysnarf/setup.py install
wait
echo "-----------------------------------------------------"
echo "Merry XMAS"

# Gallery
sudo onlysnarfpy \
-debug \
-verbose \
-action "upload" \
-type "gallery" \
-text "xmas nudes" \
-bykeyword "xmas nudes" \
-image-upload-limit 10 \
-image-download-limit 10

# Freebies
sudo onlysnarfpy \
-debug \
-verbose \
-action "message" \
-type "gallery" \
-method "all" \
-text "Merry Christmas! ;*" \
-price "0.00" \
-bykeyword "xmas tease" \
-image-upload-limit 10 \
-image-download-limit 10

# Nudes
sudo onlysnarfpy \
-debug \
-verbose \
-action "message" \
-type "video" \
-method "all" \
-text "Santa left a present for you to unwrap..." \
-price "10.00" \
-bykeyword "xmas dick"

