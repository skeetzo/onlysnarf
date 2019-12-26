#!/usr/bin/env bash
# messages all users a non nude teaser for free
# and a nude for $10
sudo python3 ../onlysnarf/setup.py install
wait
echo "-----------------------------------------------------"
echo "Merry XMAS"

# Gallery
# sudo onlysnarfpy \
# -action "upload" \
# -type "gallery" \
# -text "xmas nudes" \
# -bykeyword "xmas nudes" \
# -image-upload-limit 10 \
# -image-download-limit 10

# Freebies
sudo onlysnarfpy \
-debug \
-verbose \
-action "message" \
-type "gallery" \
-method "all" \
-input "/home/schizo/Documents/xmas tease" \
-text "Merry Christmas! ;*" \
-price "0.00" \
-image-upload-limit 10 \
-image-download-limit 10

# Nudes
sudo onlysnarfpy \
-debug \
-verbose \
-action "message" \
-type "video" \
-method "all" \
-input "/home/schizo/Documents/xmas-dick.mp4" \
-text "Santa left a present for you to unwrap..." \
-price "10.00" \
-bykeyword "xmas dick" \
-prefer-local