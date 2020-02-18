#!/usr/bin/env bash
# sudo cp ../onlysnarf/OnlySnarf/config.conf /etc/onlysnarf
sudo python3 ../onlysnarf/setup.py install
wait
echo "-----------------------------------------------------"
echo "Testing OnlySnarf"
# mkdir ../onlysnarf/logs

echo "##################################################" >> ../onlysnarf/logs/test.txt 2>&1
echo "################## Start #########################" >> ../onlysnarf/logs/test.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/test.txt 2>&1

# sudo onlysnarfpy -debug -verbose -verboser -type gallery -debug-delay -show-window -skip-reduce

# sudo onlysnarf -debug -verbose -show-window -debug-delay -prefer-local
# sudo onlysnarfpy -debug -verbose -verboser -verbosest -action test -show-window
# sudo onlysnarfpy -debug -verbose -verboser -verbosest -action message -type image -method "all" -text "test pussy" -bykeyword "pussycats" -show-window
# sudo onlysnarfpy -debug -verbose -verboser -verbosest -action message -method "recent" -text "test pussy" -bykeyword "pussycats" -show-window
# sudo onlysnarfpy -debug -verbose -verboser -verbosest -action message -method "favorite" -text "test pussy" -bykeyword "pussycats" -show-window
# sudo onlysnarfpy -verbose -type gallery -notkeyword feet -show-window -debug -debug-delay
# sudo onlysnarf-config
# sudo onlysnarfpy -debug -verbose -verboser -verbosest -action test
# sudo onlysnarfpy -debug -verbose -show-window -type image -bykeyword "pussycats"
sudo onlysnarfpy -action "message" -type image -bykeyword "pussycats" -method "all" -text "10 min of stroking" -price "3.69" -debug -verbose -verboser -verbosest -show-window
# -method "input" -input "/opt/apps/onlysnarf/tmp/20200130_122808.mp4"
# -show-window
# sudo onlysnarfpy -debug -action post -text "shnarf!" -verbose -verboser -show-window

# # Message
# sudo onlysnarfpy \
# -debug \
# -verbose \
# -action "message" \
# -method "user" \
# -user "10041738" \
# -text "owed dick" \
# -price "0.00" \
# -bykeyword "mirror dick" \
# -type "gallery" \
# -prefer-local \
# -show-window \
# -skip-download \
# -image-upload-limit 20 \
# -image-download-limit 20 \
# -force-upload

echo "##################################################" >> ../onlysnarf/logs/test.txt 2>&1
echo "################### End ##########################" >> ../onlysnarf/logs/test.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/test.txt 2>&1