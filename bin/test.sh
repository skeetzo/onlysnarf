#!/usr/bin/env bash
# sudo cp ../onlysnarf/OnlySnarf/config.conf /etc/onlysnarf
sudo python3 setup.py install

echo "-----------------------------------------------------"
echo "Testing OnlySnarf"
# mkdir ../onlysnarf/logs

echo "##################################################" >> ../onlysnarf/logs/test.txt 2>&1
echo "################## Start #########################" >> ../onlysnarf/logs/test.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/test.txt 2>&1

# sudo onlysnarf -debug -verbose -show-window -debug-delay -prefer-local
# sudo onlysnarfpy -verbose -type gallery -notkeyword feet -show-window -debug -debug-delay
# sudo onlysnarf-config
# sudo onlysnarfpy -debug -verbose -action test
# sudo onlysnarf -debug -verbose -show-window

# Message
sudo onlysnarfpy \
-debug \
-verbose \
-action "message" \
-method "user" \
-user "10041738" \
-text "owed dick" \
-price "0.00" \
-bykeyword "mirror dick" \
-type "gallery" \
-prefer-local

echo "##################################################" >> ../onlysnarf/logs/test.txt 2>&1
echo "################### End ##########################" >> ../onlysnarf/logs/test.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/test.txt 2>&1