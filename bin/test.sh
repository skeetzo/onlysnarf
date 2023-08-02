#!/bin/bash
# list of test scripts and other useful commands

git clone --depth 1  --branch development git@github.com:skeetzo/onlysnarf

python -m pip install -e .[dev]

snarf -debug -vvv post -text "balls"

pytest tests/selenium
pytest tests/selenium/browsers
pytest tests/selenium/reconnect

pytest tests/snarf

# does not work for some reason due to imports
pytest tests/api

#############
# Unit Test #
#############

python -m unittest tests/selenium/test_browsers.py
python -m unittest tests/selenium/browsers/test_firefox.py

python -m unittest tests/snarf/auth/test_twitter.py


python -m unittest tests/snarf/test_auth.py
python -m unittest tests/snarf/test_discount.py
python -m unittest tests/snarf/test_expiration.py
python -m unittest tests/snarf/test_message.py
python -m unittest tests/snarf/test_poll.py
python -m unittest tests/snarf/test_post.py
python -m unittest tests/snarf/test_schedule.py
python -m unittest tests/snarf/test_users.py

##########
# pytest #
########## 

## API ##
python -m unittest tests/api/test_api.py
python -m pytest tests/api/test_api.py

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
pytest tests/snarf/test_expiration.py
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
