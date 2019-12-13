#!/usr/bin/env bash
sudo python3 setup.py install
wait
echo "-----------------------------------------------------"
echo "Testing OnlySnarf"
mkdir -p ../onlysnarf/logs

## Add
# read messages
# promotional trial link
# settings

### Working ###
# image & expiration
# image & poll
# image & schedule
# gallery & message recent users
# message user
# post
# discount users
### Not Working ###

echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "################## Start #########################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

# Image & Expiration
echo "[*] Upload - Image & Expiration"
echo "############# Upload - Image & Expiration ########">> ../onlysnarf/logs/tests.txt
sudo onlysnarfpy \
-debug \
-verbose \
-action "upload" -type "image" \
-text "image testes" \
-bykeyword "pussycats" \
-skip-download \
-debug-delay \
-expires 3 | tee ../onlysnarf/logs/tests.txt

echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

sleep 2

# Image & Poll
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
-debug-delay \
-questions "your mom","some toast","a nice sandwich" | tee ../onlysnarf/logs/tests.txt

echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

sleep 2

# Image & Schedule
echo "[*] Upload - Image & Schedule"
echo "############# Upload - Image & Schedule ##########">> ../onlysnarf/logs/tests.txt
sudo onlysnarfpy \
-debug \
-verbose \
-action "upload" -type "image" \
-text "image testes" \
-bykeyword "pussycats" \
-schedule "6/6/2020:6:26" \
-debug-delay \
-skip-download | tee ../onlysnarf/logs/tests.txt

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
-show-window | tee ../onlysnarf/logs/tests.txt

echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

sleep 2

# Users Recent - Gallery
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
-debug-delay \
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
-debug-delay \
-prefer-local | tee ../onlysnarf/logs/tests.txt

echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "################### End ##########################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1