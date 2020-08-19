import threading
import concurrent.futures
from .driver import Driver
from .classes import Message
from .user import User
from .settings import Settings

REFRESH_DURATION = 60*9
RUN_DURATION = 60*2

# commands = [
# 	"0) menu",
# 	# "1) dick pic""
# ]

COMMANDS_AVAILABLE = "Commands available:\n0) menu\n1) notice me senpai"

class Bot:

	USERS = []

	def __init__(self):
		self.driver = Driver(browser=None)
		self.refreshing = None
		self.running = None
		##
		# self.refresher()

	@staticmethod
	def parse(user=None):
		print("Parsing: {} - {}".format(user.username, user.id))
		# check user for commands in unchecked messages
		# run command
		# print("user: {}".format(user))
		# print("parsing: {}".format(user.username))

		# if not user or not user.username or str(user) == "None" or str(user.username) == "None": return
		# commands = ["0) menu"]
		unparsed = user.get_unparsed_messages()
		for message in unparsed:
			successful = False
			isTip, amount = Message.isTip(message)
			if isTip:
				successful = Bot.tipped(user=user, amount=amount)
			elif "0) menu" in str(message).lower():
				successful = Bot.prompt(user=user)
			if successful:
				user.parse_message(message=message.message)

	@staticmethod
	def prompt(user=None):
		# show list of commands available
		user.message(message=COMMANDS_AVAILABLE)
		return True

	# refresh the Driver
	def refresh(self):
		self.driver.refresh()

	# handle the timer for refreshing the Driver
	def refresher(self):
		if not Settings.is_keep(): return
		if self.refreshing: self.refreshing.stop()
		self.refreshing = threading.Timer(REFRESH_DURATION, self.refresh).start()

	def run(self):
		if self.running: self.running.stop()
		# read all messages
		users = Bot.USERS
		if len(users) == 0:
			if Settings.get_user() and Settings.get_user().username == "all":
				users = User.update_chat_logs(driver=self.driver)
			else:
				users = User.get_recent_messagers(driver=self.driver)
				users = User.update_chat_logs(users=users, driver=self.driver)
			Bot.USERS = users
		else:
			users = User.update_chat_logs(users=users, driver=self.driver)
			users_ = User.get_recent_messagers(driver=self.driver)
			for user in users_:
				if user not in users:
					print("maybe doing something")
					users.append(user)

		print("Users to parse: {}".format(len(users)))
		self.running = threading.Timer(RUN_DURATION*len(users), self.run).start()

		def parse(user):
			user.driver = Driver(browser=None)
			# user.driver.browser = user.driver.spawn()
			Bot.parse(user=user) 

		# respond to messages
		# with concurrent.futures.ThreadPoolExecutor() as executor:
			# executor.map(parse, users)

		for user in users:
			if not user.driver or not user.browser:
				# setattr(user, "driver", Driver(browser=None))
				# setattr(user, "browser", user.driver.spawn())
				setattr(user, "driver", self.driver)
			Bot.parse(user=user)

	def tipped(user=None, amount=None):
		# for every $x amountsend 1 dick pic
		num = amount%5
		Settings.dev_print("tipped num: {}".format(num))
		user.send_dick_pics(num)
