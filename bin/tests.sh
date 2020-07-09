#!/usr/bin/env bash
sudo python3 setup.py install
wait
sudo mkdir -p /var/log/onlysnarf
sudo chown -R $USER /var/log/onlysnarf
echo "-----------------------------------------------------"
echo "Testing OnlySnarf"

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
show="show"
show=""

verbose="blank"
verbose="verbose -verbose -verbose"
verbose="-verbose -verbose"

declare -a testing
# testing=("schedule")
# testing=("discount" "expiration" "message" "poll" "post" "schedule" "upload")
testing=("message" "schedule" "upload")
testing=("upload")
testing=("post")
testing=("expiration" "message" "poll" "post" "schedule" "upload")

echo "##################################################" >> /var/log/onlysnarf/tests.txt 2>&1
echo "################## Start #########################" >> /var/log/onlysnarf/tests.txt 2>&1
echo "##################################################" >> /var/log/onlysnarf/tests.txt 2>&1

function testes() {
	# echo "Running: "$test

	bin/tests/$test.sh $show $verbose
	# bin/tests/$test.sh $show $verbose >> /var/log/onlysnarf/tests.txt

	echo "##################################################" >> /var/log/onlysnarf/tests.txt 2>&1
	echo "##################################################" >> /var/log/onlysnarf/tests.txt 2>&1
	echo "##################################################" >> /var/log/onlysnarf/tests.txt 2>&1

	sleep 2
}

for test in ${testing[@]}; do
	testes $test
done