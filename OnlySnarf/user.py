#!/usr/bin/python
# 3/25/2019: Skeetzo
# User Class

import json
import time
from re import sub
from decimal import Decimal
from . import driver as OnlySnarf
from . import settings

class User:
    def __init__(self, name=None, username=None, id=None):
        self.name = name
        self.username = username
        self.id = id
        self.messages = []
        self.sent_images = []

        self.preferences = []
        self.last_messaged_on = None
        self.subscribed_on = None

        self.isFavorite = False

        settings.maybePrint("User: %s - %s - %s" % (self.name, self.username, self.id))

    def sendMessage(self, message=None, image=None, price=None):
        print("Sending Message: %s - %s - %s" % (message, image, price))
        OnlySnarf.goto_user(self.id)
        OnlySnarf.enter_message(message)
        if image in self.sent_images:
            print("Image Already Sent: %s -> %s" % (image, self.id))
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

    def equals(self, user):
        if user.id == self.id:
            return True
        return False

    def toJSON(self):
        return json.dumps({
            "name":self.name,
            "username":self.username,
            "id":self.id
        })

    # greet user if new
    def greet(self):
        if self.last_messaged_on != None:
            print("Error: User Not New")
            return
        pass

    # send refresher message to user
    def refresh(self):
        if self.last_messaged_on == None:
            return self.greet()
        pass

    # saves chat log to user
    def readChat(self, chat):
        pass

    # saves statement / payment history
    def statement_history(self, history):
        pass

    # sets as favorite
    def favor(self):
        self.isFavorite = True

    # unsets as favorite
    def unfavor(self):
        self.isFavorite = False