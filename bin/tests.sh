#!/usr/bin/env bash
sudo python3 setup.py install

/usr/local/bin/onlysnarfpy \
-show-window \
-debug \
-verbose \
-action "message" \
-method "recent" \
-text "suck my balls" \
-price "10.00" \
-prefer-local \
-debug-delay

exit 1

# Image
/usr/local/bin/onlysnarfpy \
-show-window \
-debug \
-verbose \
-action "upload" -type "image" \
-duration 3 \
-text "image testes" \
-questions "your mom","some toast","a nice sandwich" \
-date "6/6/2020" \
-time "6:26" \
-schedule "6/6/2020:6:26" \
-expires 3

# Video
/usr/local/bin/onlysnarfpy \
-show-window \
-debug \
-verbose \
-action "upload" -type "video" \
-duration 99 \
-text "video testes" \
-questions "your mom","some toast","a nice sandwich" \
-schedule "6/6/2020:6:26" \
-expires 3 \
-skip-reduce

# Gallery
/usr/local/bin/onlysnarfpy \
-show-window \
-debug \
-verbose \
-action "upload" -type "gallery" \
-duration 7 \
-text "gallery testes" \
-questions "your mom","some toast","a nice sandwich" \
-date "6/6/2020" \
-time "6:26" \
-expires 3

# Post
/usr/local/bin/onlysnarfpy \
-show-window \
-debug \
-verbose \
-action "post" \
-duration 7 \
-text "post testes" \
-questions "your mom","toast","a sandwich" \
-expires 3

# Discount
/usr/local/bin/onlysnarfpy \
-show-window \
-debug \
-verbose \
-action "discount" \
-user "recent" \
-amount 40 \
-months 3 

# Users
/usr/local/bin/onlysnarfpy \
-show-window \
-debug \
-verbose \
-action "message" \
-method "recent" \
-text "suck my balls" \
-price "10.00" \
-image /opt/apps/onlysnarf/tmp \
-prefer-local \
-debug-delay

# User
/usr/local/bin/onlysnarfpy \
-show-window \
-debug \
-verbose \
-action "message" \
-method "user" \
-user "jamescosmo" \
-text "suck my balls" \
-prefer-local

