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

### Testing ###
### Working ###
# discount users
# image & expiration
# image & poll
# image & schedule
# post
# message recent users - image
# message user - gallery

echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "################## Start #########################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

# Image & Expiration
# echo "[*] Upload - Image & Expiration"
# echo "############# Upload - Image & Expiration ########">> ../onlysnarf/logs/tests.txt
# sudo onlysnarfpy \
# -debug \
# -verbose \
# -verboser \
# -action "upload" -type "image" \
# -text "image testes" \
# -bykeyword "pussycats" \
# -skip-download \
# -debug-delay \
# -debug-force \
# -expires 3 \
# -show-window 
# >> ../onlysnarf/logs/tests.txt 2>&1

# echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
# echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
# echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

# sleep 2

# Image
# echo "[*] Upload - Image"
# echo "############# Upload - Image ##############">> ../onlysnarf/logs/tests.txt
# sudo onlysnarfpy \
# -debug \
# -verbose \
# -verboser \
# -action "upload" -type "image" \
# -text "image testes" \
# -bykeyword "pussycats" \
# -debug-delay \
# -show-window
# # -skip-download \
# # >> ../onlysnarf/logs/tests.txt 2>&1

# echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
# echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
# echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

# sleep 2

# # Image & Poll
# echo "[*] Upload - Image & Poll"
# echo "############# Upload - Image & Poll ##############">> ../onlysnarf/logs/tests.txt
# sudo onlysnarfpy \
# -debug \
# -verbose \
# -verboser \
# -action "upload" -type "image" \
# -duration 3 \
# -text "image testes" \
# -bykeyword "pussycats" \
# -debug-delay \
# -debug-force \
# -questions "your mom","some toast","a nice sandwich" \
# -show-window
# # -skip-download \
# # >> ../onlysnarf/logs/tests.txt 2>&1

# echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
# echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
# echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1


# sleep 2

# # Image & Schedule
# echo "[*] Upload - Image & Schedule"
# echo "############# Upload - Image & Schedule ##########">> ../onlysnarf/logs/tests.txt
# sudo onlysnarfpy \
# -debug \
# -verbose \
# -verboser \
# -action "upload" -type "image" \
# -text "image testes" \
# -bykeyword "pussycats" \
# -schedule "6/6/2020:6:26" \
# -debug-delay \
# -debug-force \
# -skip-download \
# -show-window
# # >> ../onlysnarf/logs/tests.txt 2>&1

# echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
# echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
# echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

# sleep 2

# # Post
# echo "[*] Post - Text"
# echo "############# Post - Text ########################">> ../onlysnarf/logs/tests.txt
# sudo onlysnarfpy \
# -debug \
# -verbose \
# -verboser \
# -action "post" \
# -text "post testes" \
# -show-window
# # >> ../onlysnarf/logs/tests.txt 2>&1

# echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
# echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
# echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

# sleep 2

# # Discount
# echo "[*] Discount - Recent"
# echo "############# Discount - Recent ##################">> ../onlysnarf/logs/tests.txt
# sudo onlysnarfpy \
# -debug \
# -verbose \
# -action "discount" \
# -user "recent" \
# -amount 40 \
# -months 3 \
# -show-window 
# # -prefer-local
# # >> ../onlysnarf/logs/tests.txt 2>&1

# echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
# echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
# echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

# sleep 2

# # Users Recent - Image
# echo "[*] Message - Recent & Image"
# echo "############# Message - Recent & Image #########">> ../onlysnarf/logs/tests.txt
# sudo onlysnarfpy \
# -debug \
# -verbose \
# -action "message" \
# -method "recent" \
# -text "pussycat" \
# -price "10.00" \
# -bykeyword "pussycats" \
# -prefer-local \
# -show-window
# # >> ../onlysnarf/logs/tests.txt 2>&1

# echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
# echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
# echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

# sleep 2

# # User
# echo "[*] Message - User & Gallery"
# echo "############# Message - User & Gallery #####################">> ../onlysnarf/logs/tests.txt
# sudo onlysnarfpy \
# -debug \
# -verbose \
# -action "message" \
# -method "user" \
# -user "1578380" \
# -type "gallery" \
# -text "pussy" \
# -bykeyword "pussycats" \
# -show-window >> ../onlysnarf/logs/tests.txt 2>&1

# echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
# echo "################### End ##########################" >> ../onlysnarf/logs/tests.txt 2>&1
# echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1