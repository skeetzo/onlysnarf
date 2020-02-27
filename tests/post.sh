#!/usr/bin/env bash

# Post
echo "[*] Post - Text"
sudo onlysnarfpy \
-debug \
-$2 \
-action "post" \
-$1 \
-text "post testes"