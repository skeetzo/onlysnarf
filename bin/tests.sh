#!/usr/bin/env bash
sudo python3 setup.py install
wait
echo "-----------------------------------------------------"
echo "Testing OnlySnarf"
mkdir ../onlysnarf/logs

echo "##################################################" 2>&1 | tee >> ../onlysnarf/logs/tests.txt 2>&1
echo "################## Start #########################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

# Image
echo "[*] Upload - Image & Poll"
echo "############# Upload - Image & Poll ##############">> ../onlysnarf/logs/tests.txt
sudo onlysnarfpy \
-debug \
-verbose \
-action "upload" -type "image" \
-duration 3 \
-text "image testes" \
-bykeyword "pussycats" \
-skip-download \
-questions "your mom","some toast","a nice sandwich" | tee ../onlysnarf/logs/tests.txt

echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

sleep 2

# Video
echo "[*] Upload - Image & Schedule"
echo "############# Upload - Image & Schedule ##########">> ../onlysnarf/logs/tests.txt
sudo onlysnarfpy \
-debug \
-verbose \
-action "upload" -type "image" \
-text "image testes" \
-bykeyword "pussycats" \
-schedule "6/6/2020:6:26" \
-skip-download | tee ../onlysnarf/logs/tests.txt

echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

sleep 2

# Gallery
echo "[*] Upload - Image & Expiration"
echo "############# Upload - Image & Expiration ########">> ../onlysnarf/logs/tests.txt
sudo onlysnarfpy \
-debug \
-verbose \
-action "upload" -type "image" \
-text "image testes" \
-bykeyword "pussycats" \
-skip-download \
-expires 3 | tee ../onlysnarf/logs/tests.txt

echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

sleep 2

# Post
echo "[*] Post - Text"
echo "############# Post - Text ########################">> ../onlysnarf/logs/tests.txt
sudo onlysnarfpy \
-debug \
-verbose \
-action "post" \
-text "post testes" | tee ../onlysnarf/logs/tests.txt

echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

sleep 2

# Discount
echo "[*] Discount - Recent"
echo "############# Discount - Recent ##################">> ../onlysnarf/logs/tests.txt
sudo onlysnarfpy \
-debug \
-verbose \
-action "discount" \
-user "recent" \
-amount 40 \
-months 3 \
-prefer-local | tee ../onlysnarf/logs/tests.txt

echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

sleep 2

# Users
echo "[*] Message - Recent & Gallery"
echo "############# Message - Recent & Gallery #########">> ../onlysnarf/logs/tests.txt
sudo onlysnarfpy \
-debug \
-verbose \
-action "message" \
-method "recent" \
-text "pussycat" \
-price "10.00" \
-bykeyword "pussycats" \
-type "gallery" \
-skip-download \
-prefer-local | tee ../onlysnarf/logs/tests.txt

echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

sleep 2

# User
echo "[*] Message - User"
echo "############# Message - User #####################">> ../onlysnarf/logs/tests.txt
sudo onlysnarfpy \
-debug \
-verbose \
-action "message" \
-method "user" \
-user "10041738" \
-bykeyword "pussycats" \
-text "pussycat" \
-skip-download \
-prefer-local | tee ../onlysnarf/logs/tests.txt

echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "################### End ##########################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1