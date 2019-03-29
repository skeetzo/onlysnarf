#!/usr/bin/python
# 3/25/2019: Skeetzo
# User Class

class User:
    def __init__(self, username):
        self.username = username

    def sendMessage(self, message=None, image=None, price=None):
    	print("Sending Message: %s - %s - %s" % (message, image, price))
