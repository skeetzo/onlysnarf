import threading
import concurrent.futures
from .driver import Driver
from .classes import Message
from .user import User
from .settings import Settings

REFRESH_DURATION = 60*9
RUN_DURATION = 60*20

commands = [
	"0) menu",
	# "1) dick pic""
]

class Bot:

	def __init__(self):
		self.browser = None
		self.refreshing = None
		self.running = None
		##
		self.refresher()

	@staticmethod
	def parse(user):
		# check user for commands in unchecked messages
		# run command
		# print("user: {}".format(user))
		# print("parsing: {}".format(user.username))

		# if not user or not user.username or str(user) == "None" or str(user.username) == "None": return
		commands = ["0) menu"]
		unparsed = user.get_unparsed_messages()
		if len(unparsed) == 0:
			User.update_chat_logs(users=[user], browser=user.browser)
		for message in unparsed:
			successful = False
			isTip, amount = Message.isTip(message)
			if isTip:
				successful = Bot.tipped(user=user, amount=amount)
			elif "0) menu" in str(message).lower():
				bot.prompt(user=user)
			if successful:
				user.parse_message(message=message.message)

	def prompt(self, user=None):
		# show list of commands available
		User.message(browser=self.browser, message="Commands available:\n0) menu\n1) notice me senpai")

	# refresh the Driver
	def refresh(self):
		Driver.refresh(browser=self.browser)

	# handle the timer for refreshing the Driver
	def refresher(self):
		if not Settings.is_keep(): return
		if self.refreshing: self.refreshing.stop()
		self.refreshing = threading.Timer(REFRESH_DURATION, self.refresh).start()

	def run(self):
		if self.running: self.running.stop()
		self.running = threading.Timer(RUN_DURATION, self.run).start()
		self.browser = Driver.spawn_browser()
		# read all messages
		users = []
		if Settings.get_user() and Settings.get_user().username == "all":
			users = User.update_chat_logs(browser=self.browser)
		else:
			users = User.get_recent_messagers(browser=self.browser)
		print("Users to parse: {}".format(len(users)))

		def parse(user):
			browser = Driver.spawn_browser()
			user.browser = browser
			Bot.parse(user=user, browser=self.browser)
 
		# respond to messages
		with concurrent.futures.ThreadPoolExecutor() as executor:
			executor.map(parse, users)

		# for user in users:
		# 	setattr(user, "browser", self.browser)
		# 	Bot.parse(user=user)

	def tipped(user=None, amount=None):
		# for every $x amount, send 1 dick pic
		num = amount%5
		Settings.dev_print("tipped num: {}".format(num))
		user.send_dick_pics(num)
