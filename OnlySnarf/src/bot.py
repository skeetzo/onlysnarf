import threading
from .driver import Driver
from .message import Message
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
		self.refreshing = None
		self.running = None
		##
		self.refresher()

	def parse(user):
		# check user for commands in unchecked messages
		# run command
		commands = ["0) menu"]
		for message in user.get_unparsed_messages():
			successful = False
			isTip, amount = Message.isTip(message)
			if isTip:
				successful = Bot.tipped(user=user, amount=amount)
			elif "0) menu" in str(message).lower():
				Bot.prompt(user=user)
			if successful:
				user.parse_message(message=message.message)

	@staticmethod
	def prompt(user=None):
		# show list of commands available
		User.message(message="Commands available:\n0) menu\n1) notice me senpai")

	# refresh the Driver
	@staticmethod
	def refresh():
		Driver.refresh()

	# handle the timer for refreshing the Driver
	def refresher(self):
		if not Settings.is_keep(): return
		if self.refreshing: self.refreshing.stop()
		self.refreshing = threading.Timer(REFRESH_DURATION, Bot.refresh).start()

	def run(self):
		if self.running: self.running.stop()
		self.running = threading.Timer(RUN_DURATION, self.run).start()
		# read all messages
		users = User.update_chat_logs()
		# respond to messages
		for user in users:
			Bot.parse(user=user)

	def tipped(user=None, amount=None):
		# for every $x amount, send 1 dick pic
		num = amount%5
		Settings.dev_print("tipped num: {}".format(num))
		user.send_dick_pics(num)
