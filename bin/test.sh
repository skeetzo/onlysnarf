#!/usr/bin/env bash
# sudo cp ../onlysnarf/OnlySnarf/config.conf /etc/onlysnarf
sudo python3 ../onlysnarf/setup.py install
wait
mkdir -p ../onlysnarf/logs
echo "-----------------------------------------------------"
echo "Testing OnlySnarf"

echo "##################################################" >> ../onlysnarf/logs/test.txt 2>&1
echo "################## Start #########################" >> ../onlysnarf/logs/test.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/test.txt 2>&1

# video
# sudo onlysnarfpy -category video -notkeyword stroke -verbose -verbose -debug

# post request
# sudo onlysnarfpy -show -debug -verbose -verbose -verbose -action post -text "Weekly Requests Post                                                                                                            Comment below what you'd like to see more of! 8=======D~~ O:"

# stroke
# sudo onlysnarfpy -show -debug -verbose -verbose -verbose -action post -category gallery -bykeyword stroke -text 'weekly stroke tease'
# sudo onlysnarfpy -show -debug -verbose -verbose -verbose -action message -category video -bykeyword stroke -user all -text 'stroking away boredom' -price '6.69'

# menu
# sudo onlysnarf -debug -verbose -verbose -verbose -debug-delay -prefer-local -show

#############

sudo onlysnarfpy -bykeyword challenge -text "more gumby fun" -category gallery -debug -verbose -verbose -verbose -force-backup

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