#!/bin/bash
# python3 -m unittest tests/test_snarf.py
# python -m unittest test_snarf.TestSnarf.test_users
# python tests/test_snarf.py -p "users"

git clone --depth 1  --branch development git@github.com:skeetzo/onlysnarf

python -m pip install -e .[dev]

snarf -debug -vvv post -text "balls"

pytest tests/selenium
pytest tests/selenium/browsers
pytest tests/selenium/reconnect

pytest tests/snarf

python -m unittest tests/snarf/test_auth.py
python -m unittest tests/snarf/test_discount.py
python -m unittest tests/selenium/browsers/test_firefox.py
python -m unittest tests/snarf/test_poll.py

## Selenium Processes ##
pytest tests/selenium/test_browsers.py
pytest tests/selenium/test_reconnect.py
pytest tests/selenium/test_remote.py

pytest tests/selenium/browsers/test_brave.py
pytest tests/selenium/browsers/test_chrome.py
pytest tests/selenium/browsers/test_chromium.py
pytest tests/selenium/browsers/test_edge.py
pytest tests/selenium/browsers/test_firefox.py
pytest tests/selenium/browsers/test_ie.py
pytest tests/selenium/browsers/test_opera.py

pytest tests/selenium/reconnect
pytest tests/selenium/reconnect/...

## Snarf Processes ##

## Authentication ##
pytest tests/snarf/auth/test_onlyfans.py

pytest tests/snarf/test_auth.py
pytest tests/snarf/test_discount.py
pytest tests/snarf/test_message.py
pytest tests/snarf/test_poll.py
pytest tests/snarf/test_post.py
pytest tests/snarf/test_schedule.py
pytest tests/snarf/test_users.py

# Unfinished
pytest tests/snarf/auth/test_google.py
pytest tests/snarf/auth/test_twitter.py
pytest tests/snarf/test_profile.py
pytest tests/snarf/test_promotion.py

##################
## Demo Scripts ##
##################

# Discount
snarf -debug discount -user random -amount max -months max

# Message
snarf -debug message -user random -text shnarf! -price min ~/Projects/onlysnarf/public/images/snarf-missionary.jpg

# Post
snarf -debug post -text "shnarf" -tags "suck" -tags "my" -tags "balls" -performers "yourmom" -performers  "yourdad" ~/Projects/onlysnarf/public/images/snarf-missionary.jpg

# Poll
snarf -debug post -text shnarff! -question "sharnf shnarf?" -question "shnarf shhhnarff snarf?" -duration min

# Schedule
snarf -debug post -text shnarff! -schedule "10/31/2022 16:20:00"

# User
snarf -debug users

snarf -debug -browser brave users

snarf post -text "are you ready for nft nudes?" -question "yes" -question "maybe?" -question "no" -question "double no" -duration "min"

# debug remote path upload
snarf -debug -debug-delay -verbose -verbose -verbose -show post -text "shnarrff" "https://github.com/skeetzo/onlysnarf/blob/master/public/images/shnarf.jpg?raw=true"