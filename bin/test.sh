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

<<<<<<< HEAD
# sudo onlysnarfpy -debug -verbose -verboser -type gallery -debug-delay -show-window -skip-reduce

# sudo onlysnarf -debug -verbose -show-window -debug-delay -prefer-local
# sudo onlysnarfpy -debug -verbose -verboser -verbosest -action test -show-window
sudo onlysnarfpy -debug -verbose -verboser -verbosest -action message -type image -method "all" -text "test pussy" -bykeyword "pussycats" -show-window
# sudo onlysnarfpy -debug -verbose -verboser -verbosest -action message -method "recent" -text "test pussy" -bykeyword "pussycats" -show-window
# sudo onlysnarfpy -debug -verbose -verboser -verbosest -action message -method "favorite" -text "test pussy" -bykeyword "pussycats" -show-window
# sudo onlysnarfpy -verbose -type gallery -notkeyword feet -show-window -debug -debug-delay
=======
# sudo onlysnarfpy -debug -verbose -category gallery -debug-delay -show -skip-reduce

# sudo onlysnarf -debug -verbose -show -debug-delay -prefer-local
sudo onlysnarfpy -debug -verbose -verbose -action test -show
# sudo onlysnarfpy -debug -verbose -action message -category image -user "all" -text "test pussy" -bykeyword "pussycats" -show
# sudo onlysnarfpy -debug -verbose -action message -user "recent" -text "test pussy" -bykeyword "pussycats" -show
# sudo onlysnarfpy -debug -verbose -action message -user "favorite" -text "test pussy" -bykeyword "pussycats" -show
# sudo onlysnarfpy -verbose -category gallery -notkeyword feet -show -debug -debug-delay
>>>>>>> 7ae4811cfbb6d0c110ac8d1030589dda786e51e4
# sudo onlysnarf-config
# sudo onlysnarfpy -debug -verbose -action test
# sudo onlysnarfpy -debug -verbose -show -category image -bykeyword "pussycats"
# sudo onlysnarfpy -action "message" -category image -bykeyword "pussycats" -user "all" -text "10 min of stroking" -price "3.69" -debug -verbose -show
# -user "input" -input "/opt/apps/onlysnarf/tmp/20200130_122808.mp4"
# -show
# sudo onlysnarfpy -debug -action post -text "shnarf!" -verbose -show

# sudo onlysnarfpy -debug -verbose -action "message" -user "all" -category "image" -bykeyword "dailydick" -text "daily dick" -price "3.69" -show



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