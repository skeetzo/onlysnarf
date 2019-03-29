#!/usr/bin/python
# 3/25/2019: Skeetzo
# User Class

from . import driver as OnlySnarf

class User:
    def __init__(self, username):
        self.username = username

    def sendMessage(self, message=None, image=None, price=None):
    	print("Sending Message: %s - %s - %s" % (message, image, price))
    	OnlySnarf.goto_user(self.username)
    	OnlySnarf.enter_message(message)
    	OnlySnarf.enter_image(image)
    	OnlySnarf.enter_price(price)
    	OnlySnarf.confirm_message()