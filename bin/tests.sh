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
show="show"

verbose="blank"
verbose="verbose -verbose -verbose"

declare -a testing
testing=("schedule")
testing=("discount" "expiration" "message" "poll" "post" "schedule")

echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "################## Start #########################" >> ../onlysnarf/logs/tests.txt 2>&1
echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

function testes() {
	echo "Running: "$test

	bin/tests/$test.sh $show $verbose
	# ../onlysnarf/$test.sh $show >> ../onlysnarf/logs/tests.txt 2>&1

	echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
	echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1
	echo "##################################################" >> ../onlysnarf/logs/tests.txt 2>&1

	sleep 2
}

for test in ${testing[@]}; do
	testes $test
done