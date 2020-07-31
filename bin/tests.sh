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
show="-show"
show=""

declare -a browsers
browsers=("auto" "firefox" "google" "auto-remote" "remote" "remote-chrome" "remote-firefox" "reconnect")
browsers=("remote" "remote-chrome" "remote-firefox")
browsers=("auto-remote")

declare -a sources
sources=("local" "dropbox" "google" "remote")
sources=("google")

declare -a testing
# testing=("schedule")
# testing=("discount" "expiration" "message" "poll" "post" "schedule" "upload")
testing=("message" "schedule" "upload")
testing=("upload")
testing=("post")
testing=("expiration" "message" "poll" "post" "schedule" "upload")

verbose=""
verbose="-verbose -verbose"
verbose="-verbose -verbose -verbose"

echo "##################################################" >> /var/log/onlysnarf/tests.txt 2>&1
echo "################## Start #########################" >> /var/log/onlysnarf/tests.txt 2>&1
echo "##################################################" >> /var/log/onlysnarf/tests.txt 2>&1

function testes() {

	for browser in ${browsers[@]}; do

		for source in ${sources[@]}; do

			echo "Running Test: $source - $browser"
			bin/tests/$test.sh $browser $source
			# >> /var/log/onlysnarf/tests.txt

		done
	done
	
	echo "##################################################" >> /var/log/onlysnarf/tests.txt 2>&1
	echo "##################################################" >> /var/log/onlysnarf/tests.txt 2>&1
	echo "##################################################" >> /var/log/onlysnarf/tests.txt 2>&1

	sleep 2
}

for test in ${testing[@]}; do
	testes $test
done