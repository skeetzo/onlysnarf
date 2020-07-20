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
		self.hasPerformers = False
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
	def format_performers(performers): # spaced added after @ to close performer search modal
		if len(performers) > 0: return " w/ @{} ".format(" @".join(performers))
		return ""
			
	@staticmethod
	def format_tags(tags):
		if len(tags) > 0: return " @{}".format(" @".join(tags))
		return ""

	def format_text(self):
		return "{}{}{}{}".format(self.get_text(), Message.format_performers(self.get_performers()), Message.format_tags(self.get_tags()),
			Message.format_keywords(self.get_keywords())).strip()

	def get_keywords(self):
		if str(self.keywords) == "unset": return []
		# if self.keywords: return self.keywords
		if len(self.keywords) > 0: return self.keywords
		keywords = Settings.get_keywords() or []
		if len(keywords) > 0: return keywords
		if not Settings.prompt("keywords"):
			self.keywords = "unset"
			return []
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
		if str(self.performers) == "unset": return []
		# if self.performers: return self.performers
		if len(self.performers) > 0: return self.performers
		performers = Settings.get_performers() or []
		if len(performers) > 0: return performers

		if len(self.files) > 0:
			for file in self.files:
				if hasattr(file, "performer"):
					p = getattr(file, "performer")
					if p not in performers:
						performers.append(p)
			if len(performers) > 0:
				self.performers = performers
				return performers

		if not Settings.prompt("performers"):
			self.performers = "unset"
			return []
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
		if str(self.tags) == "unset": return []
		# if self.tags: return self.tags
		if len(self.tags) > 0: return self.tags
		tags = Settings.get_tags() or []
		if len(tags) > 0: return tags
		if not Settings.prompt("tags"):
			self.tags = "unset"
			return []
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
		if str(self.files) == "unset": return []
		if len(self.files) > 0: return self.files[:int(Settings.get_upload_max())]
		if (Settings.is_prompt() and not Settings.prompt("upload files")) or (not Settings.is_prompt() and Settings.get_category() == None):
			self.files = "unset"
			return []
		files = []
		if len(self.files) == 0 and len(Settings.get_input()) > 0:
			files.append(Settings.get_input_as_files())
		elif len(self.files) == 0:
			files = File.select_file_upload_method()
		if files == None: files = []
		if Settings.get_source() == "google" and len(files) == 0 and len(Google_File.get_files()) > 0:
			files = Google_File.select_files()
		# elif Settings.get_source() == "dropbox" and len(files) == 0 and len(Dropbox.get_files()) > 0:
		# 	files = Dropbox.select_files()
		elif Settings.get_source() == "remote" and len(files) == 0 and len(Remote.get_files()) > 0:
			files = Remote.select_files()
		elif Settings.get_source() == "local" and len(files) == 0 and len(File.get_files()) > 0:
			files = File.select_files()
		filed = []
		for file in files:
			if isinstance(file, Google_Folder): filed.extend(file.get_files())
			else:
				if hasattr(file, "performer"):
					self.hasPerformers = True
				filed.append(file)
		self.files = filed[:int(Settings.get_upload_max())]
		return self.files

	def get_expiration(self):
		if str(self.expiration) == "unset": return None
		if self.expiration: return self.expiration
		expires = Settings.get_expiration() or None
		if expires: return expires
		if not Settings.prompt("expiration"):
			self.expiration = "unset"
			return None
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
		if str(self.poll) == "unset": return None
		if self.poll and self.poll.check(): return self.poll
		if not Settings.prompt("poll"):
			self.poll = "unset"
			return None
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
		if str(self.schedule) == "unset": return None
		if self.schedule: return self.schedule
		if not Settings.prompt("schedule"):
			self.schedule = "unset"
			return None
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
		self.get_expiration()
		self.get_files()
		self.get_recipients()
		if not self.text:
			if len(self.files) > 0:
				self.text = self.files[0].get_title()
		if Settings.get_performer_category() or self.hasPerformers:
			self.get_performers()
		else: # might as well skip asking if not pulling from performer category
			self.performers = "unset"
		self.gotten = True

	def get_post(self):
		if self.gotten: return
		self.get_text()
		self.get_keywords()
		self.get_tags()
		self.get_poll()
		self.get_schedule()
		self.get_expiration()
		self.get_files()
		if not self.text:
			if len(self.files) > 0:
				self.text = self.files[0].get_title()
		if Settings.get_performer_category() or self.hasPerformers:
			self.get_performers()
		else:
			self.performers = "unset"
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
		if Settings.get_performer_category() or self.hasPerformers:
			self.get_performers()
		else:
			self.performers = "unset"
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

		# this should all be here instead of Driver.post
		# print("Posting:")
  #       print("- Files: {}".format(len(files)))
  #       print("- Keywords: {}".format(keywords))
  #       print("- Performers: {}".format(performers))
  #       print("- Tags: {}".format(tags))
  #       print("- Text: {}".format(text))
  #       print("- Tweeting: {}".format(Settings.is_tweeting()))


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