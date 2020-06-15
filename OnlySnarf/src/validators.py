import argparse, os
from datetime import datetime
from PyInquirer import Validator, ValidationError

ACTIONS = ['discount','post','message','test','backup','profile']
CATEGORIES_DEFAULT = [
  "images",
  "galleries",
  "videos"
]
DISCOUNT_MAX_AMOUNT = 55
DISCOUNT_MIN_AMOUNT = 10
DISCOUNT_MAX_MONTHS = 7
DISCOUNT_MIN_MONTHS = 1
DURATION_ALLOWED = [1,3,7,30,99]
EXPIRATION_ALLOWED = [1,3,7,30,99]
LIMIT_MIN = 1
LIMIT_MAX = 10

# Validators

#
# Args

def valid_action(s):
	try:
		if str(s) in ACTIONS:
			return str(s)
	except ValueError:
		msg = "Not a valid action: '{0}'.".format(s)
		raise argparse.ArgumentTypeError(msg)

def valid_amount(s):
	try:
		if int(s) > DISCOUNT_MIN_AMOUNT and int(s) < DISCOUNT_MAX_AMOUNT:
			return int(s)
	except ValueError:
		msg = "Not a valid discount amount: '{0}'.".format(s)
		raise argparse.ArgumentTypeError(msg)

def valid_date(s):
	try: return datetime.strptime(s, "%Y-%m-%d")
	except ValueError:
		msg = "Not a valid date: '{0}'.".format(s)
		raise argparse.ArgumentTypeError(msg)

def valid_time(s):
	try: return datetime.strptime(s, "%H:%M")
	except ValueError:
		msg = "Not a valid time: '{0}'.".format(s)
		raise argparse.ArgumentTypeError(msg)

def valid_price(s):
	try: return "{:.2f}".format(float(s))
	except ValueError:
		msg = "Not a valid price: '{0}'.".format(s)
		raise argparse.ArgumentTypeError(msg)

def valid_duration(s):
	try:
		if int(s) in DURATION_ALLOWED: return int(s)
	except ValueError:
		msg = "Not a valid duration: '{0}'.".format(s)
		raise argparse.ArgumentTypeError(msg)
	return int(s)

def valid_expiration(s):
	try:
		if int(s) in EXPIRATION_ALLOWED: return int(s)
	except ValueError:
		msg = "Not a valid expiration: '{0}'.".format(s)
		raise argparse.ArgumentTypeError(msg)

def valid_schedule(s):
	try: return datetime.strptime(s, "%m-%d-%Y:%H:%M")
	except ValueError:
		msg = "Not a valid schedule: '{0}'.".format(s)
		raise argparse.ArgumentTypeError(msg)

def valid_month(s):
	try:
		if int(s) > DISCOUNT_MIN_MONTHS and int(s) < DISCOUNT_MAX_MONTHS:
			return int(s)
	except ValueError:
		msg = "Not a valid month number: '{0}'.".format(s)
		raise argparse.ArgumentTypeError(msg)

def valid_path(s):
	try:
		if isinstance(s, list):
			for f in s: os.stat(s)
			return s
		else: return os.stat(s)
	except FileNotFoundError:
		msg = "Not a valid path: '{0}'.".format(s)
		raise argparse.ArgumentTypeError(msg)

# check against min/max amounts & months
# def valid_discount(s):
  # pass

# def valid_category(s):
#   if str(s) not in CATEGORIES_DEFAULT:
#     msg = "Not a valid category: '{0}'.".format(s)
#     raise argparse.ArgumentTypeError(msg)

##
# Questions

class MonthValidator(Validator):
	def validate(self, document):
		if int(document.text) < DISCOUNT_MIN_MONTHS or int(document.text) > DISCOUNT_MAX_MONTHS:
			raise ValidationError(
				message='Please enter a month number (1-12)',
				cursor_position=len(document.text))

class AmountValidator(Validator):
	def validate(self, document):
		if int(document.text) < DISCOUNT_MIN_AMOUNT or int(document.text) > DISCOUNT_MAX_AMOUNT:
			raise ValidationError(
				message='Please enter an amount as a multiple of 5 between {} and {}'.format(DISCOUNT_MIN_AMOUNT, DISCOUNT_MAX_AMOUNT),
				cursor_position=len(document.text))

class NumberValidator(Validator):
	def validate(self, document):
		try:
			int(document.text)
		except ValueError:
			raise ValidationError(
				message='Please enter a number',
				cursor_position=len(document.text))  # Move cursor to end

class TimeValidator(Validator):
	def validate(self, document):
		try:
			datetime.strptime(document.text, '%H:%M')
		except ValueError:
			raise ValidationError(
				message='Please enter a time (HH:mm)',
				cursor_position=len(document.text))  # Move cursor to end

class DateValidator(Validator):
	def validate(self, document):
		try:
			datetime.strptime(document.text, '%m-%d-%Y')
		except ValueError:
			raise ValidationError(
				message='Please enter a date (mm/dd/YYYY)',
				cursor_position=len(document.text))  # Move cursor to end

class DurationValidator(Validator):
	def validate(self, document):
		if str(document.text).lower() not in str(Settings.get_duration_allowed()).lower():
			raise ValidationError(
				message='Please enter a duration ({})'.format(", ".join(Settings.get_duration_allowed())),
				cursor_position=len(document.text))  # Move cursor to end

class ExpirationValidator(Validator):
	def validate(self, document):
		try:
			int(document.text)
		except ValueError:
			raise ValidationError(
				message='Please enter an expiration ({})'.format(", ".join(Settings.get_expiration_allowed())),
				cursor_position=len(document.text))  # Move cursor to end

class ListValidator(Validator):
	def validate(self, document):
		return True
		try:
			pass
			# import ast
			# ast.literal_eval(document.text)
		except Exception as e:
			raise ValidationError(
				message='Please enter a comma separated list of values',
				cursor_position=len(document.text))  # Move cursor to end

class LimitValidator(Validator):
	def validate(self, document):
		return True
		try:
			pass
		except Exception as e:
			raise ValidationError(
				message='Please enter a number between {} and {}'.format(LIMIT_MIN, LIMIT_MAX),
				cursor_position=len(document.text))  # Move cursor to end