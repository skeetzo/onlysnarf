import argparse, os
from datetime import datetime
from . import defaults as DEFAULT

# Validators

#
# Args

# def valid_action(s):
# 	try:
# 		if str(s) in DEFAULT.ACTIONS:
# 			return str(s)
# 	except ValueError:
# 		msg = "Not a valid action: '{0}'.".format(s)
# 		raise argparse.ArgumentTypeError(msg)

def valid_amount(s):
	try:
		if str(s) == "max": return DEFAULT.DISCOUNT_MAX_AMOUNT
		elif str(s) == "min": return DEFAULT.DISCOUNT_MIN_AMOUNT
		elif int(s) >= DEFAULT.DISCOUNT_MIN_AMOUNT and int(s) <= DEFAULT.DISCOUNT_MAX_AMOUNT:
			return int(s)
	except ValueError:
		msg = "Not a valid discount amount: '{0}'.".format(s)
		raise argparse.ArgumentTypeError(msg)

def valid_date(s):
	try: return datetime.strptime(s, DEFAULT.DATE_FORMAT)
	except ValueError:
		msg = "Not a valid date: '{0}'.".format(s)
		raise argparse.ArgumentTypeError(msg)

def valid_duration(s):
	try:
		if str(s) == "max": return DEFAULT.DURATION_ALLOWED[-1]
		elif str(s) == "min": return DEFAULT.DURATION_ALLOWED[0]
		elif str(s) in DEFAULT.DURATION_ALLOWED: return str(s)
	except ValueError:
		msg = "Not a valid duration: '{0}'.".format(s)
		raise argparse.ArgumentTypeError(msg)
	return int(s)

def valid_promo_duration(s):
	try:
		if str(s) in DEFAULT.PROMOTION_DEFAULT.DURATION_ALLOWED: return str(s)
	except ValueError:
		msg = "Not a valid promo duration: '{0}'.".format(s)
		raise argparse.ArgumentTypeError(msg)
	return int(s)

def valid_promo_expiration(s):
	try:
		if int(s) in DEFAULT.PROMOTION_EXPIRATION_ALLOWED: return int(s)
	except ValueError:
		msg = "Not a valid promo expiration: '{0}'.".format(s)
		raise argparse.ArgumentTypeError(msg)

def valid_expiration(s):
	try:
		if str(s) == "max": return DEFAULT.EXPIRATION_MAX
		elif str(s) == "min": return DEFAULT.EXPIRATION_MIN
		elif int(s) <= DEFAULT.EXPIRATION_MAX: return int(s)
	except ValueError:
		msg = "Not a valid expiration: '{0}'.".format(s)
		raise argparse.ArgumentTypeError(msg)

def valid_limit(s):
	try:
		if str(s) == "max": return DEFAULT.LIMIT_ALLOWED[-1]
		elif str(s) == "min": return DEFAULT.LIMIT_ALLOWED[0]
		elif int(s) in DEFAULT.LIMIT_ALLOWED: return int(s)
	except ValueError:
		msg = "Not a valid limit: '{0}'.".format(s)
		raise argparse.ArgumentTypeError(msg)
	return int(s)

def valid_month(s):
	try:
		if str(s) == "max": return DEFAULT.DISCOUNT_MAX_MONTHS
		elif str(s) == "min": return DEFAULT.DISCOUNT_MIN_MONTHS
		elif int(s) >= DEFAULT.DISCOUNT_MIN_MONTHS and int(s) <= DEFAULT.DISCOUNT_MAX_MONTHS:
			return int(s)
	except ValueError:
		msg = "Not a valid month number: '{0}'.".format(s)
		raise argparse.ArgumentTypeError(msg)

def valid_path(s):
	try:
		if isinstance(s, list):
			for f in s: os.stat(s)
		else: os.stat(s)
	except FileNotFoundError:
		msg = "Not a valid path: '{0}'.".format(s)
		raise argparse.ArgumentTypeError(msg)
	return s

def valid_price(s):
	if str(s) == "max": return DEFAULT.PRICE_MAXIMUM
	elif str(s) == "min": return DEFAULT.PRICE_MINIMUM
	try: return "{:.2f}".format(float(s))
	except ValueError:
		msg = "Not a valid price: '{0}'.".format(s)
		raise argparse.ArgumentTypeError(msg)

def valid_schedule(s):
	try: return datetime.strptime(s, DEFAULT.SCHEDULE_FORMAT)
	except ValueError:
		msg = "Not a valid schedule: '{0}'.".format(s)
		raise argparse.ArgumentTypeError(msg)

def valid_time(s):
	try: return datetime.strptime(s, DEFAULT.TIME_FORMAT)
	except ValueError:
		msg = "Not a valid time: '{0}'.".format(s)
		raise argparse.ArgumentTypeError(msg)

# check against min/max amounts & months
# def valid_discount(s):
  # pass

# def valid_category(s):
#   if str(s) not in DEFAULT.CATEGORIES_DEFAULT:
#     msg = "Not a valid category: '{0}'.".format(s)
#     raise argparse.ArgumentTypeError(msg)
