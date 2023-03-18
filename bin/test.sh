#!/bin/bash
# python3 -m unittest tests/test_snarf.py
# python -m unittest test_snarf.TestSnarf.test_users
# python tests/test_snarf.py -p "users"

python -m pip install -e .[dev]

onlysnarf -debug -vvv post -text "balls"

pytest tests/selenium
pytest tests/selenium/browsers
pytest tests/selenium/reconnect

pytest tests/snarf

pytest tests/snarf/test_discount.py
pytest tests/snarf/test_message.py
pytest tests/snarf/test_post.py
pytest tests/snarf/test_profile.py
pytest tests/snarf/test_users.py

## Authentication ##
<<<<<<< HEAD
python -m pip install -e .[dev] && python tests/selenium/test_auth.py

## Selenium Processes ##
python -m pip install -e .[dev] && pytest tests/selenium/browsers
python -m pip install -e .[dev] && python tests/selenium/test_browsers.py

python -m pip install -e .[dev] && python tests/selenium/browsers/test_brave.py
python -m pip install -e .[dev] && python tests/selenium/browsers/test_chrome.py
python -m pip install -e .[dev] && python tests/selenium/browsers/test_chromium.py
python -m pip install -e .[dev] && python tests/selenium/browsers/test_edge.py
python -m pip install -e .[dev] && python tests/selenium/browsers/test_firefox.py
python -m pip install -e .[dev] && python tests/selenium/browsers/test_ie.py
python -m pip install -e .[dev] && python tests/selenium/browsers/test_opera.py

## Reconnect Browsers ##
python -m pip install -e .[dev] && python tests/selenium/test_reconnect.py

python -m pip install -e .[dev] && python tests/selenium/reconnect/test_brave.py
python -m pip install -e .[dev] && python tests/selenium/reconnect/test_chrome.py
python -m pip install -e .[dev] && python tests/selenium/reconnect/test_chromium.py
python -m pip install -e .[dev] && python tests/selenium/reconnect/test_edge.py
python -m pip install -e .[dev] && python tests/selenium/reconnect/test_firefox.py
python -m pip install -e .[dev] && python tests/selenium/reconnect/test_ie.py
python -m pip install -e .[dev] && python tests/selenium/reconnect/test_opera.py

## Remote Browsers ##
python -m pip install -e .[dev] && python tests/selenium/test_remote.py
# python -m pip install -e .[dev] && python tests/selenium/remote/test_remote_chrome.py

## Snarf Processes ##
python -m pip install -e .[dev] && python tests/snarf/test_discount.py
python -m pip install -e .[dev] && python tests/snarf/test_message.py
python -m pip install -e .[dev] && python tests/snarf/test_post.py
python -m pip install -e .[dev] && python tests/snarf/test_profile.py
python -m pip install -e .[dev] && python tests/snarf/test_promotion.py
python -m pip install -e .[dev] && python tests/snarf/test_users.py
=======
python setup.py install && pytest tests/selenium/test_auth.py

## Selenium Processes ##
python setup.py install && pytest tests/selenium/test_browsers.py
python setup.py install && pytest tests/selenium/test_reconnect.py
python setup.py install && pytest tests/selenium/test_remote.py

## Snarf Processes ##
python setup.py install && pytest tests/snarf/test_discount.py
python setup.py install && pytest tests/snarf/test_message.py
python setup.py install && pytest tests/snarf/test_post.py
python setup.py install && pytest tests/snarf/test_profile.py
python setup.py install && pytest tests/snarf/test_promotion.py
python setup.py install && pytest tests/snarf/test_users.py
>>>>>>> master

#############################################################################

# Pass:

## Selenium:
# auth
# browsers
# reconnect

## Snarf:
# discount
# message
# post (basic)
# post - schedule, date, time
# post - poll
# users

#############################################################################

# Fail


#############################################################################

# Untested

# profile
# promotion
# remote

# (individual driver / message tests)

#############################################################################

##################
## Demo Scripts ##
##################

# Discount
onlysnarf -debug -show discount -user random -amount max -months max

# Message
onlysnarf -debug -show message -user random -text shnarf! -price min ~/Projects/onlysnarf/public/images/snarf-missionary.jpg

# Post
onlysnarf -debug -show post -text "shnarf" -tags "suck" -tags "my" -tags "balls" -performers "yourmom" -performers  "yourdad" ~/Projects/onlysnarf/public/images/snarf-missionary.jpg

# Poll
onlysnarf -debug -show post -text shnarff! -question "sharnf shnarf?" -question "shnarf shhhnarff snarf?" -duration min

# Schedule
onlysnarf -debug -show post -text shnarff! -schedule "10/31/2022 16:20:00"

# User
onlysnarf -debug -show users

onlysnarf -debug -show -browser brave users

onlysnarf post -text "are you ready for nft nudes?" -question "yes" -question "maybe?" -question "no" -question "double no" -duration "max"
