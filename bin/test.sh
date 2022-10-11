#!/bin/bash
# python3 -m unittest tests/test_snarf.py
# python -m unittest test_snarf.TestSnarf.test_users
# python tests/test_snarf.py -p "users"

pytest tests/selenium
pytest tests/snarf

pytest tests/snarf/test_discount.py
pytest tests/snarf/test_message.py
pytest tests/snarf/test_post.py
pytest tests/snarf/test_profile.py
pytest tests/snarf/test_users.py


## Authentication ##
python setup.py install && python tests/selenium/test_auth.py

## Selenium Processes ##
python setup.py install && python tests/selenium/test_browsers.py
python setup.py install && python tests/selenium/test_reconnect.py
python setup.py install && python tests/selenium/test_remote.py

## Snarf Processes ##
python setup.py install && python tests/snarf/test_discount.py
python setup.py install && python tests/snarf/test_message.py
python setup.py install && python tests/snarf/test_post.py
python setup.py install && python tests/snarf/test_profile.py
python setup.py install && python tests/snarf/test_promotion.py
python setup.py install && python tests/snarf/test_users.py

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
