#!/usr/bin/env bash
# sudo cp ../onlysnarf/OnlySnarf/config.conf /etc/onlysnarf
sudo python3.8 ../onlysnarf/setup.py install
wait
mkdir -p ../onlysnarf/logs
echo "-----------------------------------------------------"
echo "Testing OnlySnarf"

echo "##################################################" >> ../onlysnarf/logs/test.txt 2>&1
echo "################## Start #########################" >> ../onlysnarf/logs/test.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/test.txt 2>&1

## Bot
# screen -dmSL snarfbot /usr/local/bin/onlysnarfpy -debug -verbose -verbose -verbose -browser firefox -action bot

# /usr/local/bin/onlysnarfpy -debug -action "bot" -verbose -verbose -verbose -browser "firefox" -source "google" >> /var/log/onlysnarf/bot.log 2>&1

# onlysnarfpy -debug -action "bot" -verbose -verbose -verbose -browser "firefox" -source "google" -prefer-local >> /var/log/onlysnarf/bot.log
# onlysnarfpy -debug -action "bot" -verbose -verbose -verbose -browser reconnect -source google

# onlysnarfpy -debug -verbose -verbose -verbose -action post -category "performer" -source google -category-performer "video"

onlysnarfpy -verbose -verbose -verbose -action promotion -promotion-method "grandfather" -browser remote

# onlysnarfpy -debug -verbose -verbose -category image
# onlysnarfpy -debug -verbose -verbose -browser firefox -action bot -keep -prefer-local
# onlysnarfpy -debug -verbose -verbose -verbose -browser remote-firefox -action bot -keep -prefer-local
# onlysnarfpy -debug -verbose -verbose -verbose -browser remote-firefox -action post -category gallery
# onlysnarfpy -debug -verbose -verbose -verbose -browser reconnect -action bot -keep -prefer-local

# onlysnarfpy -debug -verbose -verbose -verbose -browser remote -prefer-local -remote-host 192.168.1.99 -source google -category video
# onlysnarfpy -debug -verbose -verbose -verbose -browser remote-firefox -prefer-local -remote-host 47.156.172.175 -remote-port 8888 -source google -category video -keep -show -login google -skip-download
# onlysnarfpy -debug -verbose -verbose -verbose -browser auto-remote -source google -category video -keep -skip-download -login google -remote-host 47.156.172.175 -remote-port 8888

# onlysnarfpy -debug -verbose -verbose -verbose -source local -category video
# onlysnarfpy -debug -verbose -verbose -verbose -source remote -remote-username skeetzo

# onlysnarfpy -debug -verbose -verbose -verbose -user "recent" -action discount -prefer-local -show -amount 10 -months 12
# onlysnarfpy -debug -verbose -verbose -verbose -user "recent" -action discount -prefer-local -show -amount 30 -months 1

# onlysnarf -debug -verbose -verbose -verbose

# onlysnarfpy -action test -debug -verbose -verbose -verbose -browser firefox -login google \
# -prefer-local \
# -user "recent" \
# -amount 40 \
# -promotion-expiration 0 \
# -limit 0 \
# -text "fuck balls"

# onlysnarf-config

# video
# onlysnarfpy -category video -notkeyword stroke -verbose -verbose -debug -browser firefox
# onlysnarfpy -category gallery -source google -notkeyword stroke -verbose -verbose -verbose -debug -browser firefox -login onlyfans -show

# post request
# sudo onlysnarfpy -show -debug -verbose -verbose -verbose -action post -text "Weekly Requests Post                                                                                                            Comment below what you'd like to see more of! 8=======D~~ O:"

# stroke
# sudo onlysnarfpy -show -debug -verbose -verbose -verbose -action post -category gallery -bykeyword stroke -text 'weekly stroke tease'
# sudo onlysnarfpy -show -debug -verbose -verbose -verbose -action message -category video -bykeyword stroke -user all -text 'stroking away boredom' -price '6.69'

# menu
# onlysnarf -debug -verbose -verbose -verbose -debug-delay -prefer-local -show

# onlysnarfpy -category gallery -bykeyword run -debug -verbose

# profile
# sudo onlysnarfpy -debug -verbose -verbose -verbose -debug-delay -prefer-local -show -action profile -profile-backup
# sudo onlysnarfpy -debug -verbose -verbose -verbose -debug-delay -prefer-local -show -action profile -profile-syncto
# sudo onlysnarfpy -debug -verbose -verbose -verbose -debug-delay -prefer-local -show -action profile -profile-syncfrom
# sudo onlysnarfpy -debug -verbose -verbose -verbose -debug-delay -prefer-local -show -action promotion -promotion-user
# sudo onlysnarfpy -debug -verbose -verbose -verbose -debug-delay -prefer-local -show -action promotion -promotion-trial

#############

# sudo onlysnarfpy -bykeyword challenge -text "more gumby fun" -category gallery -debug -verbose -verbose -verbose -force-backup

# sudo onlysnarfpy -action post -text "gumby & shampoo + dick" -category gallery -bykeyword challenge -upload-max 10

# sudo onlysnarfpy -debug -verbose -category gallery -debug-delay -show -skip-reduce
# sudo onlysnarfpy -debug -verbose -action message -category image -user "all" -text "test pussy" -bykeyword "pussycats" -show
# sudo onlysnarf-config

# # Message
# sudo onlysnarfpy \
# -debug \
# -verbose \
# -action "message" \
# -user "user" \
# -user "10041738" \
# -text "owed dick" \
# -price "0.00" \
# -bykeyword "mirror dick" \
# -category "gallery" \
# -prefer-local \
# -show \
# -skip-download \
# -image-upload-limit 20 \
# -image-download-limit 20 \
# -force-upload

echo "##################################################" >> ../onlysnarf/logs/test.txt 2>&1
echo "################### End ##########################" >> ../onlysnarf/logs/test.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/test.txt 2>&1