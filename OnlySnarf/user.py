#!/usr/bin/python
# 3/25/2019: Skeetzo
# User Class

from . import driver as OnlySnarf

class User:
    def __init__(self, name=None, username=None, id_=None):
    	self.name = name
        self.username = username
        self.id = id_
        self.messages = []
        self.sent_images = []
        print("User: %s - %s - %s" % (self.name, self.username, self.id))

    def sendMessage(self, message=None, image=None, price=None):
    	print("Sending Message: %s - %s - %s" % (message, image, price))
    	OnlySnarf.goto_user(self.id)
    	OnlySnarf.enter_message(message)
    	if image in self.sent_images:
    		print("Image Already Sent: %s -> %s" % (image, self.id))
    		return
    	OnlySnarf.enter_image(image)
    	if not settings.DEBUG:
	    	self.sent_images.append(str(image))
	    else
	    	sent.sent_images.append("DEBUG")
    	OnlySnarf.enter_price(price)
    	OnlySnarf.confirm_message()

    def equals(user):
    	if user.id == self.id:
    		return True
    	return False