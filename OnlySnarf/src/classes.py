from .driver import Driver
from .settings import Settings
import PyInquirer
from .validators import AmountValidator, MonthValidator, LimitValidator, NumberValidator, TimeValidator, DateValidator, DurationValidator, ExpirationValidator, ListValidator

class Discount:

	def __init__(self):
		self.amount = None
		self.months = None

	def apply(self):
		return Driver.discount_user(self)

	def get(self):
		self.get_amount()
		self.get_months()

	def get_amount(self):
		if self.amount: return self.amount
		amount = Settings.get_amount() or None
		if amount: return amount
		if not Settings.prompt("amount"): return None
		question = {
			'type': 'input',
			'name': 'amount',
			'message': 'Months:',
			'validate': AmountValidator
		}
		answers = PyInquirer.prompt(question)
		amount = answers["amount"]
		if not Settings.confirm(amount): return self.get_amount()
		self.amount = amount
		return self.amount

	def get_months(self):
		if self.months: return self.months
		months = Settings.get_months() or None
		if months: return months
		if not Settings.prompt("months"): return None
		question = {
			'type': 'input',
			'name': 'months',
			'message': 'Months:',
			'validate': MonthValidator
		}
		answers = PyInquirer.prompt(question)
		months = answers["months"]
		if not Settings.confirm(months): return self.get_months()
		self.months = months
		return self.months

class Poll:

	def __init__(self):
		self.duration = None
		self.questions = []

	def check(self):
		if len(self.get_questions()) > 0: return True
		if self.get_duration(): return True

	def get(self):
		self.get_duration()
		self.get_questions()

	def get_questions(self):
		if len(self.questions) > 0: return self.questions
		questions = Settings.get_questions() or []
		if len(questions) > 0: return questions
		if not Settings.prompt("questions"): return []
		print("Enter Questions")
		while True:
			question = {
				'type': 'input',
				'name': 'question',
				'message': 'Question:',
			}
			answers = PyInquirer.prompt(question)
			question = answers["question"]
			if str(question) == "": break
			questions.append(question)
		if not Settings.confirm(questions): return self.get_questions()
		self.questions = questions
		return self.questions
	
	def get_duration(self): # months
		if self.duration: return self.duration
		duration = Settings.get_duration() or None
		if duration: return duration
		if not Settings.prompt("duration"): return None
		question = {
			'type': 'input',
			'name': 'duration',
			'message': 'Duration [1, 3, 7, 99 (\'No Limit\')]',
			'validate': DurationValidator
		}
		answers = PyInquirer.prompt(question)
		duration = answers["duration"]
		if not Settings.confirm(duration): return self.get_duration()
		self.duration = duration
		return self.duration


class Promotion:

	def __init__(self):
		self.subscriptionLimit = None
		self.expiration = None
		self.duration = None
		self.user = None
		self.message = None

	# requires the copy/paste and email steps
	def create_trial_link(self):
		# limit, expiration, months, user
		Driver.create_trial_link(self)

	# apply discount directly to user on user's profile page
	def apply_to_user():
		# user, expiration, months, message
		Driver.promotion_user_directly(self)

	def get():
		self.get_expiration()
		self.get_limit()
		self.get_duration()
		self.get_message()

	def get_expiration(self):
		if self.expiration: return self.expiration
		expiration = Settings.get_expiration() or None
		if expiration: return expiration
		if not Settings.prompt("expiration"): return None
		question = {
			'type': 'input',
			'name': 'expiration',
			'message': 'Expiration [1, 3, 7, 99 (\'No Limit\')]',
			'validate': ExpirationValidator
		}
		answers = PyInquirer.prompt(question)
		expiration = answers["expiration"]
		if not Settings.confirm(expiration): return self.get_expiration()
		self.expiration = expiration
		return self.expiration

	def get_limit():
		if self.limit: return self.limit
		limit = Settings.get_limit() or None
		if limit: return limit
		if not limit.prompt("limit"): return None
		question = {
			'type': 'input',
			'name': 'limit',
			'message': 'Expiration [1, 3, 7, 99 (\'No Limit\')]',
			'validate': LimitValidator
		}
		answers = PyInquirer.prompt(question)
		limit = answers["limit"]
		if not Settings.confirm(limit): return self.get_limit()
		self.limit = limit
		return self.limit

	def get_message(self):
		if self.message != "": return self.message
		message = Settings.get_text() or None
		if message: return message
		if not Settings.prompt("message"): return ""
		question = {
			'type': 'input',
			'name': 'message',
			'message': 'Message:'
		}
		answers = PyInquirer.prompt(question)
		message = answers["message"]
		if not Settings.confirm(message): return self.get_text()
		self.message = message
		return self.message

	def get_duration(self): # months
		if self.duration: return self.duration
		duration = Settings.get_duration() or None
		if duration: return duration
		if not Settings.prompt("duration"): return None
		question = {
			'type': 'input',
			'name': 'duration',
			'message': 'Duration [1, 3, 7, 99 (\'No Limit\')]',
			'validate': DurationValidator
		}
		answers = PyInquirer.prompt(question)
		duration = answers["duration"]
		if not Settings.confirm(duration): return self.get_duration()
		self.duration = duration
		return self.duration

	def get_user():
		if self.user: return self.user
		user = User.select_user()
		self.user = user
		return self.user
