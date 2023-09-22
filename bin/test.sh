#!/bin/bash
# list of test scripts and other useful commands

git clone --depth 1  --branch development git@github.com:skeetzo/onlysnarf

python -m pip install -e .[dev]

snarf -debug -vvv post -text "balls"

# for live tests:
snarf post -text ""
snarf message -text ""


# formats:
python -m unittest $TEST_PATH
pytest $TEST_PATH

#############
# Unit Test #
#############

# single test format:
python -m unittest tests.webdriver.test_message.TestMessage_Webdriver.test_message_failure

# Webdriver #
python -m unittest tests/webdriver/test_discount.py
python -m unittest tests/webdriver/test_expiration.py
python -m unittest tests/webdriver/test_message.py
python -m unittest tests/webdriver/test_poll.py
python -m unittest tests/webdriver/test_post.py
python -m unittest tests/webdriver/test_schedule.py
python -m unittest tests/webdriver/test_users.py

# WORKING:
# TO TEST:

##########
# PyTest #
########## 

pytest tests
pytest tests/classes
pytest tests/selenium
pytest tests/webdriver

# Snarf Processes #

pytest tests/test_api.py
pytest tests/test_data.py

# Class Processes #
pytest tests/classes/test_message.py # NOT FINISHED
pytest tests/classes/test_user.py # NOT FINISHED

# Selenium Processes #
pytest tests/selenium/test_browsers.py # NOT FINISHED
pytest tests/selenium/test_reconnect.py # NOT FINISHED
pytest tests/selenium/test_remote.py # NOT FINISHED

pytest tests/selenium/browsers/test_brave.py
pytest tests/selenium/browsers/test_chrome.py
pytest tests/selenium/browsers/test_chromium.py
pytest tests/selenium/browsers/test_edge.py
pytest tests/selenium/browsers/test_firefox.py
pytest tests/selenium/browsers/test_ie.py
pytest tests/selenium/browsers/test_opera.py

# Webdriver Processes #

## Authentication ##
pytest tests/webdriver/auth/test_google.py # NOT FINISHED
pytest tests/webdriver/auth/test_onlyfans.py
pytest tests/webdriver/auth/test_twitter.py # NOT FINISHED

pytest tests/webdriver/test_auth.py

pytest tests/webdriver/test_discount.py
pytest tests/webdriver/test_expiration.py
pytest tests/webdriver/test_message.py
pytest tests/webdriver/test_poll.py
pytest tests/webdriver/test_post.py
pytest tests/webdriver/test_schedule.py
pytest tests/webdriver/test_users.py

# Unfinished
pytest tests/snarf/test_profile.py
pytest tests/snarf/test_promotion.py
