#!/usr/bin/env bash

echo "[*] Message - Recent & Image"
sudo onlysnarfpy \
-debug \
-action "message" \
-user "recent" \
-force-upload \
-category "image" \
-text "message testes" \
-bykeyword "pussycats" \
-price "4.00" \
-prefer-local \
-recent-users-count 1 \
-verbose -verbose
# -verbose
# -verbose -verbose -verbose
# -show \

# echo "[*] Message - Recent & Gallery"
# sudo onlysnarfpy \
# -debug \
# -action "message" \
# -user "recent" \
# -category "gallery" \
# -notkeyword "dick" \
# -text "message testes" \
# -price "6.00" \
# -prefer-local \
# -verbose -verbose
# # -verbose
# # -verbose -verbose -verbose
# # -show \
