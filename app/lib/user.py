import json
import time
import os
import threading
from datetime import datetime, timedelta
from re import sub
from decimal import Decimal
import PyInquirer
##
from .colorize import colorize
from .driver import Driver
from .settings import Settings

class User:

    def __init__(self, data):
        data = json.loads(json.dumps(data))
        # Settings.print(data)
        self.name = data.get('name') or ""
        self.username = str(data.get('username')).replace("@","") or ""
        self.id = data.get('id') or None
        self.messages_parsed = data.get('messages_parsed') or []
        self.messages_sent = data.get('messages_sent') or []
        self.messages_received = data.get('messages_received') or []
        self.messages = data.get('messages') or []
        self.preferences = data.get('preferences') or []
        self.last_messaged_on = data.get('last_messaged_on')
        self.sent_files = data.get('sent_files') or []
        self.subscribed_on = data.get('subscribed_on')
        self.isFavorite = data.get('isFavorite') or False
        self.lists = data.get('lists') or []
        self.statement_history = data.get('statement_history') or []
        self.started = data.get('started')
        ###### fucking json #####
        self.messages_sent = ",".join(self.messages_sent).split(",")
        self.messages_received = ",".join(self.messages_sent).split(",")
        self.messages = ",".join(self.messages_sent).split(",")
        self.messages_parsed = ",".join(self.messages_parsed).split(",")
        self.preferences = ",".join(self.messages_sent).split(",")
        self.sent_files = ",".join(self.messages_sent).split(",")
        self.statement_history = ",".join(self.messages_sent).split(",")
        #########################
        self.discount = None
        self.promotion = None
        #########################
        self.browser = None # Driver.get_browser()
        self.driver = None # Driver.get_driver()

        # try:
            # Settings.dev_print("user: {} - {} - {}".format(self.name, self.username, self.id))
        # except Exception as e:
            # Settings.dev_print(e)
            # Settings.dev_print("user: {}".format(self.id))

    def get_id(self):
        if self.id: return self.id
        id_ = self.driver.user_get_id(self.get_username())
        if not id_: return None
        self.id = id_
        return self.id

    def get_username(self):
        return self.username.replace("@", "")

    def message(self, message=None):
        if str(self.username) == "": return Settings.print("User Error: Missing Message Username")
        Settings.print("Messaging: {} - {}".format(self.username, self.id))
        successful = self.driver.message(username=self.get_username(), user_id=self.id)
        if not successful: return False
        successful = self.enter_message(message=message)
        if not successful: return False
        Settings.print("Messaged: {}".format(self.username))

    @staticmethod
    def message_user(username="", message=None):
        user = User({"username":username})
        # setattr(user, "username", username)
        setattr(user, "driver", Driver.get_driver())
        user.message(message=message)    

    def enter_message(self, message=None):
        try:
            Settings.print("Entering Message: {} - ${}".format(message.text, message.get_price() or 0))
            def enter_text(text):
                success = self.driver.message_text(text)
                if not success: return False
                return True
            def enter_price(price):
                if price == "": return False
                if price != None and Decimal(sub(r'[^\d.]', '', price)) < Settings.get_price_minimum():
                    Settings.warn_print("price too low, free image")
                    Settings.print("Price Minimum: ${}".format(Settings.get_price_minimum()))
                else:
                    success = self.driver.message_price(price)
                    if not success: return False
                Settings.debug_delay_check()
                return True
            def enter_files(files):
                # file_name = os.path.basename(path)
                # if str(file_name) in self.sent_files:
                    # Settings.err_print("file already sent: {} -> {}".format(file_name, self.username))
                    # return False
                success = self.driver.message_files(files)
                if not success: return False
                # if not Settings.is_debug():
                    # self.sent_files.append(str(file_name))
                Settings.debug_delay_check()
                return True
            def confirm():
                success = self.driver.message_confirm()
                if not success: return False
                return True
            if not enter_text(message.get_text()): return False # not allowed to fail
            enter_price(message.get_price()) # allowed to fail
            enter_files(message.get_files()) # allowed to fail
            if not confirm(): return False # not allowed to fail
            Settings.print("Message Entered")
            return True
        except Exception as e:
            Settings.dev_print(e)
            return False

    def equals(self, user):
        # Settings.print(str(user.username)+" == "+str(self.username))
        if str(user.username) == str(self.username) or str(user.id) == str(self.id):
            return True
        return False

    def toJSON(self):
        return json.dumps({
            "name":str(self.name),
            "username":str(self.username),
            "id":str(self.id),
            "messages_parsed":str(self.messages_parsed),
            "messages_sent":str(self.messages_sent),
            "messages_received":str(self.messages_received),
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
            return Settings.err_print("user not new")
        Settings.print("Sending User Greeting: {}".format(self.username))
        # self.send_message(message=Settings.DEFAULT_GREETING)
        User.enter_message(message=Settings.get_default_greeting())

    # send refresher message to user
    def refresh(self):
        if self.last_messaged_on == None:
            Settings.warn_print("never greeted, greeting instead")
            return self.greet()
        elif (timedelta(self.last_messaged_on)-timedelta(datetime())).days < 30:
            return Settings.err_print("refresher date too early - {}".format((timedelta(self.last_messaged_on)-timedelta(datetime())).days))
        Settings.print("Sending User Refresher: {}".format(self.username))
        # self.send_message(message=Settings.user_DEFAULT_REFRESHER)
        User.enter_message(message=Settings.get_default_refresher())

    # saves chat log to user
    def read_chat(self):
        Settings.print("Reading Chat: {} - {}".format(self.username, self.id))
        messages = self.driver.read_user_messages(username=self.username, user_id=self.id)
        self.messages = messages[0]
        # self.messages_and_timestamps = messages[1]
        self.messages_received = messages[2]
        self.messages_sent = messages[3]
        Settings.maybe_print("chat read: {} - {}".format(self.username, self.id))

    # saves statement / payment history
    def statementHistory(self, history):
        Settings.print("Reading Statement History: {} - {}".format(self.username, self.id))
        # self.driver.read_statements(user=self.id)

    # sets as favorite
    def favor(self):
        Settings.print("Favoring: {}".format(self.username))
        self.isFavorite = True

    # unsets as favorite
    def unfavor(self):
        Settings.print("Unfavoring: {}".format(self.username))
        self.isFavorite = False

    def update(self, user):
        return # todo fix this
        for key, value in json.loads(user.toJSON()).items():
            # Settings.print("updating: {} = {}".format(key, value))
            setattr(self, str(key), value)

    def update_chat_log(self):
        Settings.print("Updating Chat Log: {} - {}".format(self.username, self.id))
        user = self.read_chat()
        # todo: fix self.udpdate before this works
        # User.write_users_local(users=[self])

    @staticmethod
    def update_chat_logs(users=[], driver=None):
        if len(users) == 0:
            users = User.get_all_users(driver=driver)
        Settings.print("Updating Chat Logs: {}".format(len(users)))
        for user in users:
            user.read_chat()
        User.write_users_local(users=users)
        return users

    @staticmethod
    def get_all_users(driver=None):
        return User.get_active_users(driver=driver)

    # gets users from local or refreshes from onlyfans.com
    @staticmethod
    def get_active_users(driver=None):
        if Settings.is_prefer_local():
            users = User.read_users_local()
            if len(users) > 0: return users
        active_users = []
        if not driver: driver = Driver.get_driver()
        users = driver.users_get()
        for user in users:
            try:
                user = User(user)
                user = User.skipUserCheck(user)
                if user is None: continue
                setattr(user, "driver", driver)
                active_users.append(user)
            except Exception as e:
                Settings.dev_print(e)
        Settings.maybe_print("pruning memberlist")
        Settings.maybe_print("users: {}".format(len(active_users)))
        User.write_users_local(users=active_users)
        Settings.set_prefer_local(True)
        return active_users

    @staticmethod
    # return following Users
    def get_following(driver=None):
        if Settings.is_prefer_local_following(): return User.read_following_local()
        active_users = []
        users = driver.following_get()
        for user in users:
            try:
                user = User(user)
                user = User.skipUserCheck(user)
                if user is None: continue
                setattr(user, "driver", driver)
                active_users.append(user)
            except Exception as e:
                Settings.dev_print(e)
        Settings.maybe_print("following: {}".format(len(active_users)))
        User.write_following_local(users=active_users)
        Settings.set_prefer_local_following(True)
        return active_users

    def get_unparsed_messages(self):
        unparsed_messages = [m for m in self.messages if m not in self.messages_parsed]  
        Settings.dev_print("unparsed messages: {}\n{}".format(len(unparsed_messages),"\n".join(unparsed_messages)))
        return unparsed_messages

    @staticmethod
    def get_user_by_username(driver=None, username=None):
        if not username or username == None:
            Settings.err_print("missing username")
            return None

        if str(username) == "all":
            return User.get_all_users(driver=driver)
        elif str(username) == "recent":
            return User.get_recent_users(driver=driver)
        elif str(username) == "favorite":
            return User.get_favorite_users(driver=driver)

        users = User.read_users_local()
        for user in users:
            if str(user.username) == "@u"+str(username) or str(user.username) == "@"+str(username) or str(user.username) == str(username):
                Settings.maybe_print("found user: local")
                return user
        users = User.get_all_users(driver=driver)
        for user in users:
            if str(user.username) == "@u"+str(username) or str(user.username) == "@"+str(username) or str(user.username) == str(username):
                Settings.maybe_print("found user: members")
                return user
        Settings.err_print("missing user by username - {}".format(username))
        return None

    @staticmethod
    def get_favorite_users(driver=None):
        Settings.maybe_print("getting favorite users")
        users = User.get_all_users(driver=driver)
        favUsers = []
        # favorites = ",".join(str(Settings.get_users_favorite()))
        for user in users:
            if user.isFavorite:
                Settings.maybe_print("fav user: {}".format(user.username))
                user = User.skipUserCheck(user)
                if user is None: continue
                favUsers.append(user)
        return favUsers

    @staticmethod
    def get_users_by_list(number=None, name=None, driver=None):
        Settings.maybe_print("getting users by list: {} - {}".format(number, name))
        users = driver.get_list(number=number, name=name)
        listUsers = []
        for user in users:
            Settings.maybe_print("user: {}".format(user.username))
            user = User.skipUserCheck(user)
            if user is None: continue
            listUsers.append(user)
        return listUsers

    # returns users that have no messages sent to them
    @staticmethod
    def get_new_users(driver=None):
        Settings.maybe_print("getting new users")
        users = User.get_all_users(driver=driver)
        newUsers = []
        date_ = datetime.today() - timedelta(days=10)
        for user in users:
            if not user.started: continue
            started = datetime.strptime(str(user.started),"%b %d, %Y")
            # Settings.maybe_print("date: "+str(date_)+" - "+str(started))
            if started < date_: continue
            Settings.maybe_print("new user: {}".format(user.username))
            user = User.skipUserCheck(user)
            if user is None: continue
            newUsers.append(user)
        return newUsers

    @staticmethod
    def get_never_messaged_users(driver=None):
        Settings.maybe_print("getting new users")
        users = User.get_all_users(driver=driver)
        newUsers = []
        for user in users:
            if len(user.messages_received) == 0:
                Settings.maybe_print("never messaged user: {}".format(user.username))
                user = User.skipUserCheck(user)
                if user is None: continue
                newUsers.append(user)
        return newUsers

    @staticmethod
    def get_recent_users(driver=None):
        Settings.maybe_print("getting recent users")
        users = User.get_all_users(driver=driver)
        i = 0
        users_ = []
        for user in users:
            Settings.maybe_print("recent user: {}".format(user.username))
            user = User.skipUserCheck(user)
            if user is None: continue
            users_.append(user)
            i += 1
            if i == int(Settings.get_recent_user_count()):
                return users_
        return users_

    # probably not necessary
    def parse_message(self, message=None):
        self.messages.remove(str(message))
        self.messages_parsed.append(str(message))

    @staticmethod
    def get_recent_messagers(driver=None):
    # def get_recent_messagers(notusers=[], driver=None):
        Settings.maybe_print("getting recent users from messages")
        users = []
        try:
            users_ = driver.messages_scan()
            # users_ = driver.messages_scan(notusers=notusers)
            for user in users_:
                user_ = User({"id":user})
                setattr(user_, "driver", driver)
                users.append(user_)
        except Exception as e:
            Settings.dev_print(e)
        return users

    @staticmethod
    def select_user():
        Settings.print('a')
        user = Settings.get_user() or None
        if user: return user
        # if user: return User.get_user_by_username(user.username)
        # if not Settings.prompt("user"): return User.get_random_user()
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
        elif str(user) == "list":
            return User.list_menu()
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
    def list_menu():
        question = {
            'type': 'list',
            'name': 'answer',
            'message': 'User:',
            'choices': ["Back", "Enter", "Select"]
        }
        answer = PyInquirer.prompt(question)["answer"]
        if str(answer) == "Back":
            Settings.print(0)
            return User.select_user()
        elif str(answer) == "Enter":
            question = {
                'type': 'input',
                'message': 'Enter List (name or #):',
                'name': 'list'
            }
            list_ = PyInquirer.prompt(question)["list"]
            theList = None
            try:
                theList = int(list_)
                users = User.get_users_by_list(number=theList, driver=Driver.get_driver())
            except Exception as e:
                try:
                    theList = str(list_)
                    return User.get_users_by_list(name=theList, driver=Driver.get_driver())
                except Exception as e:
                    Settings.err_print("unable to find list number")
        elif str(answer) == "Select":
            lists_ = Driver.get_driver().get_lists()
            lists__ = [{"name":"Back", "value":"back"}]
            for list___ in lists_:
                lists__.append({
                    "name":list___[1],
                    "value":list___[0],
                })
            question = {
                'type': 'list',
                'name': 'answer',
                'message': 'Lists:',
                'choices': lists_
            }
            answer = PyInquirer.prompt(question)["answer"]
            if str(answer) == "back":
                return User.select_user()
            else:
                return Driver.get_driver().get_list_members(answer)
        return []

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

    def send_dick_pics(self, num):
        Settings.print("Sending Dick Pics: {}".format(num))
        # pass
        # downloads a dick pic from configured source and sends to user

        # search source for dick pics
        # send dick pics
        # Settings.get_drive_keyword()
        Settings.set_bycategory("dick")
        message = Message()
        setattr(message, "text", "8=======D~~") # todo: randomize this
        self.message(message=message)

    @staticmethod
    def skipUserCheck(user):
        if str(user.id).lower() in Settings.get_skipped_users() or str(user.username).lower() in Settings.get_skipped_users():
            Settings.maybe_print("skipping: {}".format(user.username))
            return None
        return user

    # gets a list of all subscribed user_ids from local txt
    @staticmethod
    def read_users_local(driver=None):
        Settings.maybe_print("getting local users")
        users = []
        users_ = []
        try:
            with open(str(Settings.get_users_path())) as json_file:  
                users = json.load(json_file)['users']
            Settings.maybe_print("loaded local users")
            for user in users:
                try:
                    user_ = User(json.loads(user))
                    setattr(user_, "driver", driver)
                    users_.append(user_)
                except Exception as e:
                    Settings.dev_print(e)
            return users_
        except Exception as e:
            Settings.dev_print(e)
        return users_

    # writes user list to local txt
    @staticmethod
    def write_users_local(users=None):
        if users is None:
            users = User.get_all_users()
        if len(users) == 0:
            Settings.maybe_print("skipping: local users save - no users")
            return
        Settings.print("Saving Users Locally")
        Settings.maybe_print("local users path: "+str(Settings.get_users_path()))
        ##
        # update from existing
        existingUsers = User.read_users_local()
        for user in users:
            for user_ in existingUsers:
                if user.equals(user_):
                    user.update(user_)
        ##
        data = {}
        data['users'] = []
        for user in users:
            data['users'].append(user.toJSON())
        try:
            with open(str(Settings.get_users_path()), 'w') as outfile:  
                json.dump(data, outfile, indent=4, sort_keys=True)
        except FileNotFoundError:
            Settings.err_print("missing local users")
        except OSError:
            Settings.err_print("missing local path")

    @staticmethod
    def read_following_local():
        Settings.maybe_print("getting local following")
        users = []
        users_ = []
        try:
            with open(str(Settings.get_users_path().replace("users.json", "following.json"))) as json_file:  
                users = json.load(json_file)['users']
            Settings.maybe_print("loaded local following")
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
    def write_following_local(users=None):
        if users is None:
            users = User.get_following()
        if len(users) == 0:
            Settings.maybe_print("skipping: local following save - no following")
            return
        Settings.print("Saving Following Users Locally")
        Settings.maybe_print("local users path: "+str(Settings.get_users_path().replace("users.json", "following.json")))
        data = {}
        data['users'] = []
        for user in users:
            data['users'].append(user.toJSON())
        try:
            with open(str(Settings.get_users_path().replace("users.json", "following.json")), 'w') as outfile:  
                json.dump(data, outfile, indent=4, sort_keys=True)
        except FileNotFoundError:
            Settings.err_print("missing local following")
        except OSError:
            Settings.err_print("missing local path")

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
