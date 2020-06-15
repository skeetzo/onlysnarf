from datetime import datetime
from .classes import Poll, Schedule
from .driver import Driver
from .file import File, Google_File, Google_Folder
from .settings import Settings
from .user import User
from .validators import NumberValidator, TimeValidator, DateValidator, DurationValidator, ExpirationValidator, ListValidator
import PyInquirer
from PyInquirer import Validator, ValidationError

class Message():
	def __init__(self):
		self.text = None
		self.files = []
		##
		self.keywords = []
		self.tags = []
		self.performers = []
		## messages
		self.price = None
		self.recipients = [] # users to send to
		self.users = [] # prepared recipients
		## posts
		self.expiration = None
		self.poll = None
		self.schedule = None
		##
		self.gotten = False

	###########################################################################

	def backup_files(self):
		for file in self.files:
			file.backup()

	def delete_files(self):
		for file in self.files:
			file.delete()

	def cleanup_files(self):
		self.backup_files()
		self.delete_files()

	@staticmethod
	def format_keywords(keywords):
		if len(keywords) > 0: return " #{}".format(" #".join(keywords))
		return ""

	@staticmethod
	def format_performers(performers):
		if len(performers) > 0: return " w/ @{}".format(" @".join(performers))
		return ""
			
	@staticmethod
	def format_tags(tags):
		if len(tags) > 0: return " @{}".format(" @".join(tags))
		return ""

	def format_text(self):
		return "{}{}{}{}".format(self.get_text(), Message.format_performers(self.get_performers()), Message.format_tags(self.get_tags()),
			Message.format_keywords(self.get_keywords())).strip()

	def get_keywords(self):
		# if self.keywords: return self.keywords
		if len(self.keywords) > 0: return self.keywords
		keywords = Settings.get_keywords() or []
		if len(keywords) > 0: return keywords
		if not Settings.prompt("keywords"): return []
		question = {
			'type': 'input',
			'name': 'keywords',
			'message': 'Keywords:',
			'validate': ListValidator
		}
		answers = PyInquirer.prompt(question)
		keywords = answers["keywords"]
		keywords = keywords.split(",")
		keywords = [n.strip() for n in keywords]
		if not Settings.confirm(keywords): return self.get_keywords()
		self.keywords = keywords
		return self.keywords

	def get_performers(self):
		# if self.performers: return self.performers
		if len(self.performers) > 0: return self.performers
		performers = Settings.get_tags() or []
		if len(performers) > 0: return performers
		if not Settings.prompt("performers"): return []
		question = {
			'type': 'input',
			'name': 'performers',
			'message': 'Performers:',
			'validate': ListValidator
		}
		answers = PyInquirer.prompt(question)
		performers = answers["performers"]
		performers = performers.split(",")
		performers = [n.strip() for n in performers]
		if not Settings.confirm(performers): return self.get_performers()
		self.performers = performers
		return self.performers

	def get_tags(self):
		# if self.tags: return self.tags
		if len(self.tags) > 0: return self.tags
		tags = Settings.get_tags() or []
		if len(tags) > 0: return tags
		if not Settings.prompt("tags"): return []
		question = {
			'type': 'input',
			'name': 'tags',
			'message': 'Tags:',
			'validate': ListValidator
		}
		answers = PyInquirer.prompt(question)
		tags = answers["tags"]
		tags = tags.split(",")
		tags = [n.strip() for n in tags]
		if not Settings.confirm(tags): return self.get_tags()
		self.tags = tags
		return self.tags

	# ensures File references exist and are downloaded
	# files are File references
	# file references can be GoogleId references which need to download their source
	# files exist when checked for size
	# ?
	def get_files(self):
		if len(self.files) > 0: return self.files[:int(Settings.get_upload_max())]
		files = []
		if len(self.files) == 0 and len(Settings.get_input()) > 0:
			files.append(Settings.get_input_as_files())
		elif len(self.files) == 0:
			files = File.select_file_upload_method()
		if len(files) == 0 and len(Google_File.get_files()) > 0:
			files = Google_File.select_files()
		filed = []
		for file in files:
			if isinstance(file, Google_Folder): filed.extend(file.get_files())
			else: filed.append(file)
		self.files = filed[:int(Settings.get_upload_max())]
		return self.files

	def get_expiration(self):
		if self.expiration: return self.expiration
		expires = Settings.get_expiration() or None
		if expires: return expires
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

	def get_poll(self):
		if self.poll and self.poll.check(): return self.poll
		if not Settings.prompt("poll"): return None
		poll = Poll()
		poll.get()
		if not poll.check(): return None
		self.poll = poll
		return poll

	def get_price(self):
		if self.price: return self.price
		price = Settings.get_price() or None
		if price: return price
		if not Settings.prompt("price"): return ""
		question = {
			'type': 'input',
			'name': 'price',
			'message': 'Price',
			'validate': NumberValidator,
			'filter': lambda val: int(val)
		}
		answers = PyInquirer.prompt(question)
		price = answers["price"]
		if not Settings.confirm(price): return self.get_price()
		self.price = price
		return self.price

	# ensures listed recipients are users
	# Settings.USERS and self.recipients should be usernames
	# if includes [all, recent, favorite] & usernames it only uses the 1st found of [all,...]
	def get_recipients(self):
		if len(self.users) > 0: return self.users
		users = []
		if len(self.recipients) == 0 and len(Settings.get_users()) > 0: 
			users = Settings.get_users()
		elif len(self.recipients) == 0 and Settings.get_user(): 
			users = [Settings.get_user()]
		elif len(self.recipients) == 0:
			users = User.select_users()
		# users = []
		# for user in recipients:
		#     if str(user.username).lower() == "all":
		#         users = User.get_all_users()
		#         break
		#     elif str(user.username).lower() == "recent":
		#         users = User.get_recent_users()
		#         break
		#     elif str(user.username).lower() == "favorite":
		#         users = User.get_favorite_users()
		#         break
		#     else: users.append(user)
		self.users = users
		return self.users

	def get_schedule(self):
		if self.schedule: return self.schedule
		if not Settings.prompt("schedule"): return None
		schedule = Schedule()
		schedule.get()
		if not schedule.check(): return None
		self.schedule = schedule
		return schedule
		
	def get_text(self):
		if self.text: return self.text
		text = Settings.get_text() or None
		if text: 
			self.text = text
			return text
		if not Settings.prompt("text"): return None
		question = {
			'type': 'input',
			'name': 'text',
			'message': 'Text:'
		}
		answers = PyInquirer.prompt(question)
		text = answers["text"]
		if not Settings.confirm(text): return self.get_text()
		self.text = text
		return self.text

	def get(self):
		if self.gotten: return
		self.get_text()
		self.get_keywords()
		self.get_tags()
		self.get_price()
		self.get_poll()
		self.get_schedule()
		self.get_files()
		self.get_recipients()
		if not self.text:
			if len(self.files) > 0:
				self.text = self.files[0].get_title()
		if Settings.get_performer_category():
			self.get_performers()
		self.gotten = True

	def get_post(self):
		if self.gotten: return
		self.get_text()
		self.get_keywords()
		self.get_tags()
		self.get_poll()
		self.get_schedule()
		self.get_files()
		if not self.text:
			if len(self.files) > 0:
				self.text = self.files[0].get_title()
		if Settings.get_performer_category():
			self.get_performers()
		self.gotten = True

	def get_message(self):
		if self.gotten: return
		self.get_recipients()
		self.get_text()
		self.get_price()
		self.get_files()
		if not self.text:
			if len(self.files) > 0:
				self.text = self.files[0].get_title()
		if Settings.get_performer_category():
			self.get_performers()
		self.gotten = True

	@staticmethod
	def Post():
		message = Message()
		message.post()

	def post(self):
		self.get_post()
		if Settings.is_prompt():
			if not Settings.prompt("Post"): return
		successful = False
		try: successful = Driver.post(self)
		except Exception as e:
			Settings.dev_print(e)
			successful = False
		if successful: self.cleanup_files()

	@staticmethod
	def Send():
		message = Message()
		message.send()

	# sends to recipients
	# 'post' as recipient will post message instead
	def send(self):
		self.get_message()
		if Settings.is_prompt():
			if not Settings.prompt("Send"): return
		successful = False
		try: 
			# for user in self.get_recipients():
			for user in self.users:
				# if isinstance(user, str) and str(user) == "post": successful_ = Driver.post(self)
				# print("Messaging: {}".format(user.username))
				if isinstance(user, User): successful_ = User.message_user(user.username, self)
				else: successful_ = User.message_user(user, self)
				if not successful_: continue
				successful_ = Driver.message(user.username)
		except Exception as e:
			Settings.dev_print(e)
			successful = False
		if successful: self.cleanup_files()