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
# discount
# expiration
# poll
# schedule
# post
# message
show="blank"
show="show-window"

verbose="verbose"
verbose="verbose -verboser"
verbose="verbose -verboser -verbosest"

declare -a testing
testing=("discount" "expiration" "message" "poll" "post" "schedule" "upload")
testing=("schedule")

echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "################## Start #########################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

function testes() {
	echo "Running: "$test

	../onlysnarf/tests/$test.sh $show $verbose
	# ../onlysnarf/tests/$test.sh $show >> ../onlysnarf/logs/tests.txt 2>&1

	echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
	echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
	echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

	sleep 2
}

for test in ${testing[@]}; do
	testes $test
done