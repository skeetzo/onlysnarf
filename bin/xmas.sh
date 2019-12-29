#!/usr/bin/env bash
# releases teasers and free nudes
# messages a short nude video for $6

sudo python3 ../onlysnarf/setup.py install
wait
echo "-----------------------------------------------------"
echo "Merry XMAS"

##
# Freebies
##

sudo onlysnarfpy \
-action "upload" \
-type "gallery" \
-text "xmas tease" \
-bykeyword "xmas tease" \
-image-upload-limit 10 \
-image-download-limit 10 \
-force-upload

# could be run as a cron to schedule itself later in the day
# sudo onlysnarfpy \
# -action "upload" \
# -type "gallery" \
# -method "input" \
# -input "/home/schizo/Documents/xmas nudes" \
# -text "Christmas 2019" \
# -image-upload-limit 10 \
# -image-download-limit 10 \
# -force-upload

##
# Nudes
# ##
# sudo onlysnarfpy \
# -verbose \
# -action "message" \
# -type "video" \
# -method "all" \
# -image "/home/schizo/Documents/xmas-dick.mp4" \
# -text "Merry Christmas! Santa left a present for you to unwrap...  ;*" \
# -price "6.00" \
# -prefer-local