#!/usr/bin/env bash

# Settings
echo "[*] Settings - Sync From"
onlysnarfpy \
-debug \
-action "profile" \
-profile-method "syncfrom" \
-keep \
-verbose -verbose -verbose \
-browser "$1" \
-source "$2"
# -show \

# echo "[*] Settings - Sync To"
# onlysnarfpy \
# -debug \
# -action "profile" \
# -profile-method "syncto" \
# -keep \
# -verbose -verbose -verbose \
# -browser "$1" \
# -source "$2"
# # -show \