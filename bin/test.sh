#!/bin/bash
# python3 -m unittest tests/test_snarf.py
# python -m unittest test_snarf.TestSnarf.test_users
# python tests/test_snarf.py -p "users"

## Selenium Processes ##
python setup.py install && python tests/test_browsers.py
python setup.py install && python tests/test_reconnect.py
python setup.py install && python tests/test_remote.py

## Login ##
python setup.py install && python tests/test_auth.py

## Snarf Processes ##
python setup.py install && python tests/test_discount.py
python setup.py install && python tests/test_message.py
python setup.py install && python tests/test_post.py
python setup.py install && python tests/test_profile.py
python setup.py install && python tests/test_promotion.py
python setup.py install && python tests/test_users.py

## IPFS ##
python setup.py install && python tests/test_ipfs.py

## XMAS ##
python setup.py install && python tests/test_xmas.py

#############################################################################

# Pass:

## Selenium:
# browsers
# reconnect

## Snarf:
# auth
# discount
# message
# post (basic)
# users

#############################################################################

# Fail

# post - schedule, date, time
# post - poll (?)


#############################################################################

# Untested

# ipfs
# xmas
# profile
# promotion
# remote

# (individual driver / message tests)