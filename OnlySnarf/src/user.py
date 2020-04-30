#!/usr/bin/python3
# 3/25/2019: Skeetzo
# User Class

import json
import time
import os
import threading
from datetime import datetime, timedelta
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
        self.id = data.get('id') or None
        self.messages_from = data.get('messages_from') or []
        self.messages_to = data.get('messages_to') or []
        self.messages = data.get('messages') or []
        self.preferences = data.get('preferences') or []
        self.last_messaged_on = data.get('last_messaged_on')
        self.sent_files = data.get('sent_files') or []
        self.subscribed_on = data.get('subscribed_on')
        self.isFavorite = data.get('isFavorite') or False
        self.statement_history = data.get('statement_history') or []
        self.started = data.get('started')
        ###### fucking json #####
        self.messages_from = ",".join(self.messages_from).split(",")
        self.messages_to = ",".join(self.messages_from).split(",")
        self.messages = ",".join(self.messages_from).split(",")
        self.preferences = ",".join(self.messages_from).split(",")
        self.sent_files = ",".join(self.messages_from).split(",")
        self.statement_history = ",".join(self.messages_from).split(",")
        #########################
        self.discount = None
        self.promotion = None
        # try:
            # Settings.dev_print("User: {} - {} - {}".format(self.name, self.username, self.id))
        # except Exception as e:
            # Settings.dev_print(e)
            # Settings.dev_print("User: {}".format(self.id))

    def discount(self, discount=None):
        if not discount: discount = Settings.get_discount()
        return Driver.discount_user(discount)

    def get_id(self):
        if self.id: return self.id
        id_ = Driver.user_get_id(self.get_username())
        self.id = id_
        return self.id

    def get_username(self):
        return self.username.replace("@", "")

    def message(self, message=None):
        if str(self.username) == "": return print("User Error: Missing Message Username")
        print("Messaging: {} - {}".format(self.username, self.id))
        successful = Driver.message(username=self.get_username(), user_id=self.id)
        if not successful: return False
        successful = User.enter_message(message)
        if not successful: return False
        print("Messaged: {}".format(self.username))

    @staticmethod
    def message_user(username="", message=None):
        user = User({"username":username})
        # setattr(user, "username", username)
        user.message(message=message)    

    @staticmethod
    def enter_message(message=None):
        try:
            print("Entering Message: {} - ${}".format(message.text, message.get_price() or 0))
            def enter_text(text):
                success = Driver.message_text(text)
                if not success: return False
                return True
            def enter_price(price):
                if price == "": return False
                if price != None and Decimal(sub(r'[^\d.]', '', price)) < Settings.get_price_minimum():
                    print("Warning: Price Too Low, Free Image")
                    print("Price Minimum: ${}".format(Settings.get_price_minimum()))
                else:
                    success = Driver.message_price(price)
                    if not success: return False
                Settings.debug_delay_check()
                return True
            def enter_files(files):
                # file_name = os.path.basename(path)
                # if str(file_name) in self.sent_files:
                    # print("Error: File Already Sent: {} -> {}".format(file_name, self.username))
                    # return False
                success = Driver.message_files(files)
                if not success: return False
                # if not Settings.is_debug():
                    # self.sent_files.append(str(file_name))
                Settings.debug_delay_check()
                return True
            def confirm():
                success = Driver.message_confirm()
                if not success: return False
                return True
            if not enter_text(message.get_text()): return False # not allowed to fail
            enter_price(message.get_price()) # allowed to fail
            enter_files(message.get_files()) # allowed to fail
            if not confirm(): return False # not allowed to fail
            print("Message Entered")
            return True
        except Exception as e:
            Settings.dev_print(e)
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
            "sent_files":str(self.sent_files),
            "subscribed_on":str(self.subscribed_on),
            "isFavorite":str(self.isFavorite)
        })

    # def get_username(self):
    #     return self["username"]

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
                Settings.dev_print(e)
        Settings.maybe_print("pruning memberlist")
        Settings.maybe_print("users: {}".format(len(active_users)))
        User.write_users_local(users=active_users)
        Settings.set_prefer_local(True)
        return active_users

    @staticmethod
    def get_following():
        # return following Users
        return []

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
        Settings.maybe_print("Getting Favorite Users")
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
            if not user.started: continue
            started = datetime.strptime(str(user.started),"%b %d, %Y")
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
        user = Settings.get_user() or None
        if user: return user
        # if not Settings.prompt("user"): return None
        choices = Settings.get_message_choices()
        choices.append("enter username")
        choices.append("select username")
        choices = [str(choice).title() for choice in choices]
        question = {
            'type': 'list',
            'name': 'user',
            'message': 'User:',
            'choices': choices,
            'filter': lambda val: str(val).lower()
        }
        answers = PyInquirer.prompt(question)
        user = answers["user"]
        if str(user) == "enter username":
            username = input("Username: ")
            return User.get_user_by_username(username)
        elif str(user) == "select username":
            return User.select_username()
        elif str(user) == "favorites":
            return User.get_favorite_users()
        if not Settings.confirm(user): return User.select_user()
        return user

    @staticmethod
    def select_users():
        # if not Settings.prompt("users"): return []
        users = []
        while True:
            user = User.select_user()
            if not user: break
            if str(user).lower() == "all" or str(user).lower() == "recent": return [user]
            users.append(user)
            if not Settings.prompt("another user"): break
        if not Settings.confirm([user.username for user in users]): return User.select_users()
        return users

    @staticmethod
    def select_username():
        # returns the list of usernames to select
        # if not Settings.prompt("select username"): return None
        users = User.get_all_users()
        users_ = []
        for user in users:
            user_ = {
                "name":user.username.replace("@",""),
                "value":user,
                "short":user.id
            }
            users_.append(user_)
        question = {
            'type': 'list',
            'name': 'user',
            'message': 'Username:',
            'choices': users_
        }
        user = PyInquirer.prompt(question)['user']
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
            Settings.maybe_print("Loaded Local Users")
            for user in users:
                try:
                    users_.append(User(json.loads(user)))
                except Exception as e:
                    Settings.dev_print(e)
            return users_
        except Exception as e:
            Settings.dev_print(e)
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
