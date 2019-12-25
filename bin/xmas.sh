#!/usr/bin/env bash
# messages all users a non nude teaser for free
# and a nude for $10
sudo python3 ../onlysnarf/setup.py install
wait
echo "-----------------------------------------------------"
echo "Merry XMAS"

# Freebies
sudo onlysnarfpy \
-debug \
-verbose \
-action "message" \
-user "all" \
-text "Merry Christmas! ;*" \
-price "0.00" \
-bykeyword "xmas" \
-type "image"

# Nudes
sudo onlysnarfpy \
-debug \
-verbose \
-action "message" \
-user "all" \
-text "Santa left you some presents to unwrap..." \
-price "10.00" \
-bykeyword "xmas dick" \
-type "gallery"