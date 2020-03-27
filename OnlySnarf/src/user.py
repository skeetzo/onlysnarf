#!/usr/bin/python3
# 3/25/2019: Skeetzo
# User Class

import json
import time
import os
import threading
from datetime import datetime
from re import sub
from decimal import Decimal
##
from .colorize import colorize
from .driver import Driver
from .settings import Settings
import PyInquirer

class User:

    def __init__(self, data):
        data = json.loads(json.dumps(data))
        # print(data)
        self.name = data.get('name') or ""
        self.username = data.get('username') or ""
        self.id = data.get('id') or ""
        self.messages_from = data.get('messages_from') or []
        self.messages_to = data.get('messages_to') or []
        self.messages = data.get('messages') or []
        self.preferences = data.get('preferences') or []
        self.last_messaged_on = data.get('last_messaged_on')
        self.sent_images = data.get('sent_images') or []
        self.subscribed_on = data.get('subscribed_on')
        self.isFavorite = data.get('isFavorite') or False
        self.statement_history = data.get('statement_history') or []
        self.started = data.get('started')
        ###### fucking json #####
        self.messages_from = ",".join(self.messages_from).split(",")
        self.messages_to = ",".join(self.messages_from).split(",")
        self.messages = ",".join(self.messages_from).split(",")
        self.preferences = ",".join(self.messages_from).split(",")
        self.sent_images = ",".join(self.messages_from).split(",")
        self.statement_history = ",".join(self.messages_from).split(",")
        #########################
        try:
            Settings.maybe_print("User: {} - {} - {}".format(self.name, self.username, self.id))
        except Exception as e:
            Settings.dev_print(e)
            Settings.maybe_print("User: {}".format(self.id))

    def discount(self, discount={}):
        amount = getattr(discount, "amount")
        months = getattr(discount, "months")
        if not amount: amount = input("Discount: ")
        if not months: months = input("Months: ")
        discount = {"amount":amount,"months":months}
        successful = Driver.discount_user(self.username, discount)
        return successful

    def message(self, message=None):
        if str(self.username) == "": return print("User Error: Missing Message Username")
        print("Messaging: {}".format(self.username))
        successful = Driver.message(self.username, message)
        if not successful: return False
        successful = User.enter_message(message)
        if not successful: return False
        print("Messaged: {}".format(self.username))

    @staticmethod
    def message_user(username="", message=None):
        user = User()
        setattr(user, "username", username)
        user.message(message=message)    

    @staticmethod
    def enter_message(message=None):
        try:
            print("Entering Message: {} - ${}".format(message, price))
            def enter_text(text):
                success = Driver.message_text(text)
                if not success: return False
                return True
            def enter_price(price):
                if path == "": return False
                if path != None and Decimal(sub(r'[^\d.]', '', price)) < Settings.get_price_minimum():
                    print("Warning: Price Too Low, Free Image")
                    print("Price Minimum: ${}".format(Settings.get_price_minimum()))
                else:
                    success = Driver.message_price(price)
                    if not success: return False
                Settings.debug_delay_check()
                return True
            def enter_file(path):
                if path == "": return False
                image_name = os.path.basename(path)
                if str(image_name) in self.sent_images:
                    print("Error: Image Already Sent: {} -> {}".format(image_name, self.username))
                    return False
                success = Driver.message_files(path)
                if not success: return False
                if not Settings.is_debug():
                    self.sent_images.append(str(image_name))
                Settings.debug_delay_check()
                return True
            def confirm():
                success = Driver.message_confirm()
                if not success: return False
                return True
            if not enter_text(message.text): return False # not allowed to fail
            enter_price(message.price) # allowed to fail
            for file in message.files:
                enter_file(file.get_path()) # allowed to fail
            if not confirm(): return False # not allowed to fail
            print("Message Entered")
            return True
        except Exception as e:
            Settings.maybe_print(e)
            return False

    def equals(self, user):
        # print(str(user.username)+" == "+str(self.username))
        if user.username == self.username:
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
        # self.send_message(message=Settings.DEFAULT_GREETING)
        User.enter_message(message=Settings.get_default_greeting())

    # send refresher message to user
    def refresh(self):
        if self.last_messaged_on == None:
            print("Warning: Never Greeted, Greeting Instead")
            return self.greet()
        elif (timedelta(self.last_messaged_on)-timedelta(datetime())).days < 30:
            return print("Error: Refresher Date Too Early - {}".format((timedelta(self.last_messaged_on)-timedelta(datetime())).days))
        print("Sending User Refresher: {}".format(self.username))
        # self.send_message(message=Settings.user_DEFAULT_REFRESHER)
        User.enter_message(message=Settings.get_default_refresher())

    # saves chat log to user
    def readChat(self, Driver):
        print("Reading Chat: {} - {}".format(self.username, self.id))
        messages = Driver.read_user_messages(self.id)
        self.messages = messages[0]
        # self.messages_and_timestamps = messages[1]
        self.messages_to = messages[2]
        self.messages_from = messages[3]
        Settings.maybe_print("Chat Read: {} - {}".format(self.username, self.id))

    # saves statement / payment history
    def statementHistory(self, history):
        print("Reading Statement History: {} - {}".format(self.username, self.id))
        Driver.read_statements(user=self.id)

    # sets as favorite
    def favor(self):
        print("Favoring: {}".format(self.username))
        self.isFavorite = True

    # unsets as favorite
    def unfavor(self):
        print("Unfavoring: {}".format(self.username))
        self.isFavorite = False

    @staticmethod
    def get_all_users():
        return User.get_active_users()

    # gets users from local or refreshes from onlyfans.com
    @staticmethod
    def get_active_users():
        if Settings.is_prefer_local(): return User.read_users_local()
        active_users = []
        users = Driver.users_get()
        for user in users:
            try:
                user = User(user)
                user = User.skipUserCheck(user)
                if user is None: continue
                active_users.append(user)
            except Exception as e:
                Settings.maybe_print(e)
        Settings.maybe_print("pruning memberlist")
        Settings.maybe_print("users: {}".format(len(active_users)))
        User.write_users_local(users=active_users)
        Settings.set_prefer_local(True)
        return active_users

    @staticmethod
    def get_user_by_username(username):
        if not username or username == None:
            print("Error: Missing Username")
            return None
        users = User.read_users_local()
        for user in users:
            if str(user.username) == "@u"+str(username) or str(user.username) == "@"+str(username) or str(user.username) == str(username):
                Settings.maybe_print("Found User: Local")
                return user
        users = User.get_all_users()
        for user in users:
            if str(user.username) == "@u"+str(username) or str(user.username) == "@"+str(username) or str(user.username) == str(username):
                Settings.maybe_print("Found User: Members")
                return user
        print("Error: Missing User by Username - {}".format(username))
        return None

    @staticmethod
    def get_favorite_users():
        Settings.maybe_print("Getting Fav Users")
        users = User.get_all_users()
        favUsers = []
        favorites = ",".join(str(Settings.get_users_favorite()))
        for user in users:
            if user in favorites:
                Settings.maybe_print("Fav User: {}".format(user.username))
                user = User.skipUserCheck(user)
                if user is None: continue
                favUsers.append(user)
        return favUsers

    # returns users that have no messages sent to them
    @staticmethod
    def get_new_users():
        Settings.maybe_print("Getting New Users")
        users = User.get_all_users()
        newUsers = []
        date_ = datetime.today() - timedelta(days=10)
        for user in users:
            started = datetime.strptime(user.started,"%b %d, %Y")
            # Settings.maybe_print("date: "+str(date_)+" - "+str(started))
            if started < date_: continue
            Settings.maybe_print("New User: {}".format(user.username))
            user = User.skipUserCheck(user)
            if user is None: continue
            newUsers.append(user)
        return newUsers

    @staticmethod
    def get_never_messaged_users():
        Settings.maybe_print("Getting New Users")
        update_chat_logs()
        users = User.get_all_users()
        newUsers = []
        for user in users:
            if len(user.messages_to) == 0:
                Settings.maybe_print("Never Messaged User: {}".format(user.username))
                user = User.skipUserCheck(user)
                if user is None: continue
                newUsers.append(user)
        return newUsers

    @staticmethod
    def get_recent_users():
        Settings.maybe_print("Getting Recent Users")
        users = User.get_all_users()
        i = 0
        users_ = []
        for user in users:
            Settings.maybe_print("Recent User: {}".format(user.username))
            user = User.skipUserCheck(user)
            if user is None: continue
            users_.append(user)
            i += 1
            if i == int(Settings.get_recent_user_count()):
                return users_
        return users_

    @staticmethod
    def select_user():
        if not Settings.prompt("user"): return None
        question = {
            'type': 'list',
            'name': 'choice',
            'message': 'User:',
            'choices': ['All', 'Recent', 
                # 'Favorite', 
                'Enter Username', 'Select Username']
        }
        answers = PyInquirer.prompt(question)
        choice = answers["choice"]
        if not Settings.confirm(choice): return User.select_user()
        if str(choice) == "Enter Username":
            username = input("Username: ")
            return User.get_user_by_username(username)
        elif str(choice) == "Select Username":
            return User.select_username()
        return choice

    @staticmethod
    def select_users():
        if not Settings.prompt("users"): return []
        users = []
        while True:
            user = User.select_user()
            if not user: break
            users.append(user)
            if str(choice).lower() == "all" or str(choice).lower() == "recent": break
        if not Settings.confirm(users): return User.select_users()
        return users

    @staticmethod
    def select_username():
        # returns the list of usernames to select
        if not Settings.prompt("username"): return None
        users = User.get_all_users()
        for user in users:
            user["name"] = user["username"]
            user["value"] = user
            user["short"] = user["id"]
        question = {
            'type': 'list',
            'name': 'user',
            'message': 'Username:',
            'choices': users
        }
        answers = PyInquirer.prompt(question)
        user = answers["user"]
        if not Settings.confirm(user.username): return User.select_username()
        return user

    # gets a list of all subscribed user_ids from local txt
    @staticmethod
    def read_users_local():
        Settings.maybe_print("Getting Local Users")
        users = []
        users_ = []
        try:
            with open(str(Settings.get_users_path())) as json_file:  
                users = json.load(json_file)['users']
            Settings.maybe_print("Loaded:")
            for user in users:
                try:
                    users_.append(User(json.loads(user)))
                except Exception as e:
                    Settings.maybe_print(e)
            return users_
        except Exception as e:
            Settings.maybe_print(e)
        return users_

    @staticmethod
    def skipUserCheck(user):
        if str(user.id).lower() in Settings.get_skipped_users() or str(user.username).lower() in Settings.get_skipped_users():
            Settings.maybe_print("skipping: {}".format(user.username))
            return None
        return user

    # writes user list to local txt
    @staticmethod
    def write_users_local(users=None):
        if users is None:
            users = User.get_all_users()
        if len(users) == 0:
            Settings.maybe_print("Skipping: Local Users Save - No Users")
            return
        print("Saving Users Locally")
        Settings.maybe_print("local users path: "+str(Settings.get_users_path()))
        data = {}
        data['users'] = []
        for user in users:
            if Settings.is_debug():
                Settings.maybe_print("Saving: "+str(user.username))
            data['users'].append(user.toJSON())
        try:
            with open(str(Settings.get_users_path()), 'w') as outfile:  
                json.dump(data, outfile, indent=4, sort_keys=True)
        except FileNotFoundError:
            print("Error: Missing Local Users")
        except OSError:
            print("Error: Missing Local Path")

#######################################################################################

def delayForThirty():
    Settings.maybe_print("30...")
    time.sleep(10)
    Settings.maybe_print("20...")
    time.sleep(10)
    Settings.maybe_print("10...")
    time.sleep(7)
    Settings.maybe_print("3...")
    time.sleep(1)
    Settings.maybe_print("2...")
    time.sleep(1)
    Settings.maybe_print("1...")
    time.sleep(1)
