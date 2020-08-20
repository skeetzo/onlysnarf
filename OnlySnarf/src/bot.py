import threading
import concurrent.futures
from .driver import Driver
from .classes import Message
from .user import User
from .settings import Settings
from .snarf import Snarf

REFRESH_DURATION = 60*9
RUN_DURATION = 60*2

# commands = [
# 	"0) menu",
# 	# "1) dick pic""
# ]

COMMANDS_AVAILABLE = "Commands available:\n0) menu\n1) notice me senpai"

class Bot(Snarf):

	USERS = []

	def __init__(self):
		Snarf.__init__(self)
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

		user.update_chat_log()

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
			users = User.get_recent_messagers(driver=self.driver)
		else:
			users = User.get_recent_messagers(notusers=users, driver=self.driver)
		Bot.USERS = users

		print("Users to parse: {}".format(len(users)))
		self.running = threading.Timer(RUN_DURATION*len(users), self.run).start()


		# respond to messages

		def threaded():
			def parse(user):
				if not user.driver or not user.browser:
					user.driver = Driver(browser=None)
				# user.driver.browser = user.driver.spawn()
				Bot.parse(user=user)

			MAX = 3
			if "remote" in str(Settings.get_browser_type()): MAX = 10
			with concurrent.futures.ThreadPoolExecutor(max_workers=MAX) as executor:
				executor.map(parse, users)

		def single():
			for user in users:
				if not user.driver or not user.browser:
					# setattr(user, "driver", Driver(browser=None))
					# setattr(user, "browser", user.driver.spawn())
					setattr(user, "driver", self.driver)
				Bot.parse(user=user)

		if "remote" in Settings.get_browser_type() or "reconnect" in Settings.get_browser_type():
			single()
		else:
			threaded()

	@staticmethod
	def tipped(user=None, amount=None):
		# for every $x amountsend 1 dick pic
		num = amount%5
		Settings.dev_print("tipped num: {}".format(num))
		return user.send_dick_pics(num)