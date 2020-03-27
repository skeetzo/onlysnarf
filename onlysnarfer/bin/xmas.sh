#!/usr/bin/env bash
# needs to be updated w/ cron
# ideally runs tasks on different days
# 1) release teaser pics
# 2) message nude pay per message
# 3) release nude pics

sudo python3 ../onlysnarf/setup.py install
wait
echo "-----------------------------------------------------"
echo "Merry XMAS"

##
# Teaser
##

# sudo onlysnarfpy \
# -action "upload" \
# -type "gallery" \
# -text "xmas tease" \
# -bykeyword "xmas tease" \
# -image-upload-limit 10 \
# -image-download-limit 10 \
# -force-upload

##
# Nudes
##
# sudo onlysnarfpy \
# -action "upload" \
# -type "gallery" \
# -text "xmas was fun" \
# -bykeyword "xmas nudes" \
# -image-upload-limit 10 \
# -image-download-limit 10 \
# -force-upload

# sudo onlysnarfpy \
# -verbose \
# -action "message" \
# -type "video" \
# -method "all" \
# -image "/home/schizo/Documents/xmas-dick.mp4" \
# -text "Merry Christmas! Santa left a present for you to unwrap...  ;*" \
# -price "6.00" \
# -prefer-local