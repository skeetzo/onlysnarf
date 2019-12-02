#!/usr/bin/env bash
sudo python3 setup.py install
echo "-----------------------------------------------------"
echo "Testing OnlySnarf"
mkdir ../onlysnarf/logs
# echo "## MESSAGE - RECENT ##"

# /usr/local/bin/onlysnarfpy \
# -debug \
# -verbose \
# -action "message" \
# -method "recent" \
# -text "suck my balls" \
# -price "10.00" \
# -show-window

# sleep 2

echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "################## Start #########################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

echo "[*] Upload - Image & Poll"

# Image
/usr/local/bin/onlysnarfpy \
-debug \
-verbose \
-action "upload" -type "image" \
-duration 3 \
-text "image testes" \
-questions "your mom","some toast","a nice sandwich" >> ../onlysnarf/logs/tests.txt 2>&1

echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

sleep 2

echo "[*] Upload - Video & Schedule"

# Video
/usr/local/bin/onlysnarfpy \
-debug \
-verbose \
-action "upload" -type "video" \
-text "video testes" \
-schedule "6/6/2020:6:26" \
-skip-download >> ../onlysnarf/logs/tests.txt 2>&1

echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

sleep 2

echo "[*] Upload - Gallery & Expiration"

# Gallery
/usr/local/bin/onlysnarfpy \
-debug \
-verbose \
-action "upload" -type "gallery" \
-text "gallery testes" \
-expires 3 >> ../onlysnarf/logs/tests.txt 2>&1

echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

sleep 2

echo "[*] Post - Text"

# Post
/usr/local/bin/onlysnarfpy \
-debug \
-verbose \
-action "post" \
-text "post testes" >> ../onlysnarf/logs/tests.txt 2>&1

echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

sleep 2

echo "[*] Discount - Recent"

# Discount
/usr/local/bin/onlysnarfpy \
-debug \
-verbose \
-action "discount" \
-user "recent" \
-amount 40 \
-months 3 \
-prefer-local >> ../onlysnarf/logs/tests.txt 2>&1

echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

sleep 2

echo "[*] Message - Recent & Local Image"

# Users
/usr/local/bin/onlysnarfpy \
-debug \
-verbose \
-action "message" \
-method "recent" \
-text "suck my balls" \
-price "10.00" \
-image /opt/apps/onlysnarf/tmp \
-prefer-local >> ../onlysnarf/logs/tests.txt 2>&1

echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

sleep 2

echo "[*] Message - User"

# User
/usr/local/bin/onlysnarfpy \
-debug \
-verbose \
-action "message" \
-method "user" \
-text "suck my balls" \
-prefer-local >> ../onlysnarf/logs/tests.txt 2>&1

echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "################### End ##########################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1