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
show=""
show="-show"

declare -a browsers
browsers=("auto" "firefox" "google" "auto-remote" "remote" "remote-chrome" "remote-firefox" "reconnect")
browsers=("remote" "remote-chrome" "remote-firefox")
browsers=("reconnect")
browsers=("auto")
browsers=("auto-remote")
browsers=("firefox")

declare -a sources
sources=("local" "dropbox" "google" "remote")
sources=("local" "google" "remote")
sources=("local")
sources=("google")

declare -a testing
testing=("post")
testing=("promotion")
testing=("settings")
testing=("poll" "post" "schedule" "settings" "upload")
testing=("bot")
testing=("message" "schedule")
testing=("message")
testing=("upload")
testing=("schedule")
testing=("discount" "expiration" "message" "poll" "post" "schedule" "settings" "upload")

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
			../onlysnarf/bin/tests/$test.sh $browser $source
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