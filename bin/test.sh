#!/bin/bash
# python3 -m unittest tests/test_snarf.py
# python -m unittest test_snarf.TestSnarf.test_users
# python tests/test_snarf.py -p "users"

pytest tests/selenium
pytest tests/snarf

pytest tests/snarf/test_message.py
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

## IPFS ##
python setup.py install && python tests/test_ipfs.py

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

# ipfs
# profile
# promotion
# remote

# (individual driver / message tests)


#############################################################################

##################
## Demo Scripts ##
##################

# Discount
ENV=test onlysnarf -debug discount -user random

# Message
ENV=test onlysnarf -debug message -user random -text shnarf! -price min public/images/snarf-missionary.jpg

# Post
ENV=test onlysnarf -debug post -text random public/images/snarf-missionary.jpg

# Schedule, Date, Time
ENV=test onlysnarf -debug post -text shnarff! -schedule 10/8/2022:16:20
ENV=test onlysnarf -debug post -text shnarff! -date 10/10/2022 -time 16:20 
ENV=test onlysnarf -debug post -text shnarff! -question "sharnf shnarf?" -question "shnarf shhhnarff snarf?" -duration min -expiration min

# User
ENV=test onlysnarf -debug users
