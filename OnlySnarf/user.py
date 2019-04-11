#!/usr/bin/python
# 3/25/2019: Skeetzo
# User Class

import json
import time
from datetime import datetime
from re import sub
from decimal import Decimal
from . import driver as OnlySnarf
from . import settings

class User:
    def __init__(self, name=None, username=None, id=None, messages_from=[], messages_to=[], messages=[], preferences=[], last_messaged_on=None, sent_images=[], subscribed_on=None, isFavorite=False, statement_history=[]):
        self.name = name
        self.username = username.encode("utf-8")
        self.id = id
        # messages receieved from the user
        self.messages_from = messages_from
        # messages sent to the user
        self.messages_to = messages_to
        # combined chatlog
        self.messages = messages
        # anal, cock, etc
        self.preferences = preferences
        # date and time last messaged on
        self.last_messaged_on = last_messaged_on
        # images already sent to the user
        self.sent_images = sent_images
        # date subscription began
        self.subscribed_on = subscribed_on
        # if user is a favorite
        self.isFavorite = isFavorite
        # statement history
        self.statement_history = statement_history
        settings.maybePrint("User: {} - {} - {}".format(self.name, self.username, self.id))

    def sendMessage(self, message=None, image=None, price=None):
        print("Sending Message: {} - {} - {}".format(message, image, price))
        OnlySnarf.goto_user(self.id)
        OnlySnarf.enter_message(message)
        if image in self.sent_images:
            print("Image Already Sent: {} -> {}".format(image, self.id))
            return
        OnlySnarf.enter_image(image)
        OnlySnarf.enter_price(price)
        if not settings.DEBUG:
            self.sent_images.append(str(image))
        else:
            self.sent_images.append("DEBUG")
        if Decimal(sub(r'[^\d.]', '', price)) < 5:
            print("Warning: Price Too Low, Skipping")
            return
        if settings.DEBUG:
	        settings.maybePrint("30...")
	        time.sleep(10)
	        settings.maybePrint("20...")
	        time.sleep(10)
	        settings.maybePrint("10...")
	        time.sleep(7)
	        settings.maybePrint("3...")
	        time.sleep(1)
	        settings.maybePrint("2...")
	        time.sleep(1)
	        settings.maybePrint("1...")
	        time.sleep(1)
        OnlySnarf.confirm_message()
        if not settings.DEBUG:
            self.last_messaged_on = datetime()

    def equals(self, user):
        if user.id == self.id:
            return True
        return False

    def toJSON(self):
        return json.dumps({
            "name":str(self.name),
            "username":str(self.username),
            "id":str(self.id),
            "messages_from":str(self.messages_from),
            "messages_to":str(self.messages_to),
            "messages":str(self.messages),
            "preferences":str(self.preferences),
            "last_messaged_on":str(self.last_messaged_on),
            "sent_images":str(self.sent_images),
            "subscribed_on":str(self.subscribed_on),
            "isFavorite":str(self.isFavorite)
        })

    # greet user if new
    def greet(self):
        if self.last_messaged_on == None:
            return print("Error: User Not New")
        print("Sending User Greeting: {}".format(self.username))
        self.sendMessage(message=settings.user_DEFAULT_GREETING)

    # send refresher message to user
    def refresh(self):
        if self.last_messaged_on == None:
            print("Warning: Never Greeted, Greeting Instead")
            return self.greet()
        elif (timedelta(self.last_messaged_on)-timedelta(datetime())).days < 30:
            return print("Error: Refresher Date Too Early - {}".format((timedelta(self.last_messaged_on)-timedelta(datetime())).days))
        print("Sending User Refresher: {}".format(self.username))
        self.sendMessage(message=settings.user_DEFAULT_REFRESHER)

    # saves chat log to user
    def readChat(self):
        print("Reading Chat: {} - {}".format(self.username, self.id))
        messages = OnlySnarf.read_chat(self.id)
        self.messages = messages[0]
        self.messages_to = messages[1]
        self.messages_from = messages[2]
        settings.maybePrint("Chat Read: {} - {}".format(self.username, self.id))

    # saves statement / payment history
    def statementHistory(self, history):
        print("Reading Statement History: {} - {}".format(self.username, self.id))
        OnlySnarf.read_statements(user=self.id)

    # sets as favorite
    def favor(self):
        print("Favoring: {}".format(self.username))
        self.isFavorite = True

    # unsets as favorite
    def unfavor(self):
        print("Unfavoring: {}".format(self.username))
        self.isFavorite = False