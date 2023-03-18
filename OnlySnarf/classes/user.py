import json
import time
import os
import threading
from datetime import datetime, timedelta
##
from ..util.colorize import colorize
from ..lib.driver import Driver
from ..util.settings import Settings

class User:
    """OnlyFans users."""

    def __init__(self, data):
        """User object"""

        data = json.loads(json.dumps(data))
        self.name               =   data.get('name')                            or None
        self.username           =   str(data.get('username')).replace("@","")   or None
        self.id                 =   data.get('id')                              or None

        self.messages_parsed    =   data.get('messages_parsed')                 or []
        self.messages_sent      =   data.get('messages_sent')                   or []
        self.messages_received  =   data.get('messages_received')               or []
        self.messages           =   data.get('messages')                        or []

        self.sent_files         =   data.get('sent_files')                      or []
        self.isFavorite         =   data.get('isFavorite')                      or False
        # self.lists              =   data.get('lists')                           or []
        self.start_date         =   data.get('started')                         or None

        # BUG: fix empty array
        if len(self.sent_files) > 0 and self.sent_files[0] == "":
            self.sent_files = []

    def toJSON(self):
        """
        Dumps relevant user data to JSON.
        """

        return json.dumps({
            "name":str(self.name),
            "username":str(self.username),
            "id":str(self.id),
            "messages_parsed":str(self.messages_parsed),
            "messages_sent":str(self.messages_sent),
            "messages_received":str(self.messages_received),
            "messages":str(self.messages),
            "sent_files":str(self.sent_files),
            "isFavorite":str(self.isFavorite)
        })

    def equals(self, user):
        """
        Equals comparison checks usernames and ids.

        Parameters
        ----------
        classes.User
            The user to compare another user object against
        """

        if str(user.username) == str(self.username) or str(user.id) == str(self.id): return True
        return False

    def get_id(self):
        """
        Get the provided ID of the User. Searches via username if necessary.

        Returns
        -------
        str
            The user id
        """

        if self.id: return self.id
        self.id = Driver.user_get_id(self.get_username())
        return self.id

    def get_username(self):
        """
        Get the username of the User.

        Returns
        -------
        str
            The username
        """

        if self.username: return self.username
        self.username = Driver.get_username(self.get_id())
        return self.username

    def message(self, message):
        """
        Message the user by their available username or id with the provided message.

        Parameters
        ----------
        message : Object
            The message to send as a serialized Message object from get_message.

        Returns
        -------
        bool
            Whether or not the message was successful
        """

        if not self.get_username() and not self.get_id(): return Settings.err_print("missing user identifiers!")
        if self.id:
            Settings.print("messaging user (id): {} ({}) - \"{}\"".format(self.username, self.id, message["text"]))
        else:
            Settings.print("messaging user: {} - \"{}\"".format(self.username, message["text"]))
        if not Driver.message(self.username, user_id=self.id): return False
        return self.message_send(message)

    def messages_read(self):
        """
        Read the chat of the user.
        """

        Settings.print("reading user chat: {} ({})".format(self.username, self.id))
        # messages, messages_received, messages_sent = Driver.read_user_messages(self.username, user_id=self.id)
        # self.messages = messages
        # self.messages_received = messages_received
        # self.messages_sent = messages_sent
        self.messages, self.messages_received, self.messages_sent = Driver.read_user_messages(self.username, user_id=self.id)
        # self.messages_and_timestamps = messages[1]
        Settings.maybe_print("chat read!")

    def message_send(self, message):
        """
        Complete the various components of sending a message to a user.
        
        Parameters
        ----------
        message : Object
            The message to send as a serialized Message object from get_message.

        Returns
        -------
        bool
            Whether or not the message was successful
        """

        Settings.print("entering message: (${}) {}".format(message["price"], message["text"]))
        try:
            driver = Driver.get_driver()
            def confirm_message(): return driver.message_confirm()
            # enter the text of the message
            def enter_text(text): return driver.message_text(text)
            # enter the price to send the message to the user
            def enter_price(price):
                if not price: return True
                return driver.message_price(price)
            def enter_files(files):
                for file in files:
                    # enter files by filepath while checking for already sent files
                    file_name = file.get_title()
                    if str(file_name) in self.sent_files:
                        Settings.warn_print("file already sent to user: {} <-- {}".format(self.username, file_name))
                        Settings.maybe_print("skipping...")
                        continue
                    self.sent_files.append(file_name)
                return driver.upload_files(files)
            if all([enter_text(message["text"]), enter_price(message["price"]), enter_files(message["files"])]): return confirm_message()
        except Exception as e:
            Settings.err_print("message failed!")
            Settings.dev_print(e)
        return False

    def update(self, user):
        for key, value in json.loads(user.toJSON()).items():
            # Settings.print("updating: {} = {}".format(key, value))
            setattr(self, str(key), value)

    #############
    ## Statics ##
    #############

    # TODO: update with more accurate "active"ness
    # gets users from local or refreshes from onlyfans.com
    @staticmethod
    def get_active_users():
        """
        Get active users.

        Returns
        -------
        list
            The active users

        """

        Settings.dev_print("getting active users...")
        active_users = []
        for user in User.get_all_users():
            if not User.skipUserCheck(user): continue
            active_users.append(user)
        Settings.maybe_print("active users: {}".format(len(active_users)))
        return active_users
    
    @staticmethod
    def get_all_users():
        """
        Get all users.

        Returns
        -------
        list
            The users

        """

        Settings.dev_print("getting all users...")
        if Settings.is_prefer_local():
            users = User.read_users_local()
            if len(users) > 0: return users
        users = []
        for user in Driver.users_get():
            if user is None: continue
            users.append(User(user))
        Settings.maybe_print("users: {}".format(len(users)))
        User.write_users_local(users=users)
        Settings.set_prefer_local(True)
        return users

    ## TODO
    # make this actually do something
    @staticmethod
    def get_favorite_users():
        """
        Get all favorite users.

        Returns
        -------
        list
            The favorite users

        """

        Settings.dev_print("getting favorite users...")
        users = []
        for user in User.get_all_users():
            if user.isFavorite:
                Settings.maybe_print("fav user: {}".format(user.username))
                users.append(user)
        return users

    @staticmethod
    def get_following():
        """
        Get all following.

        Returns
        -------
        list
            The users being followed

        """

        Settings.dev_print("getting following...")
        if Settings.is_prefer_local():
            users = User.read_following_local()
            if len(users) > 0: return users
        users = []
        for user in Driver.following_get():
            user = User(user)
            users.append(user)
        Settings.maybe_print("following: {}".format(len(users)))
        User.write_following_local(users=users)
        Settings.set_prefer_local(True)
        return users

    @staticmethod
    def get_never_messaged_users():
        """
        Get all users that have never been messaged before.

        Returns
        -------
        list
            The users that have not been messaged

        """

        Settings.dev_print("getting users that have never been messaged...")
        users = []
        for user in User.get_all_users():
            if len(user.messages_received) == 0:
                Settings.maybe_print("never messaged user: {}".format(user.username))
                users.append(user)
        return users

    @staticmethod
    def get_new_users():
        """
        Get all new users.

        Returns
        -------
        list
            The users that are new

        """

        Settings.dev_print("getting new users...")
        newUsers = []
        date_ = datetime.today() - timedelta(days=10)
        for user in User.get_all_users():
            if not user.start_date: continue
            started = datetime.strptime(str(user.start_date),"%b %d, %Y")
            # Settings.maybe_print("date: "+str(date_)+" - "+str(started))
            if started < date_: continue
            Settings.maybe_print("new user: {}".format(user.username))
            newUsers.append(user)
        return newUsers

    @staticmethod
    def get_random_user():
        """
        Get a random user.

        Returns
        -------
        classes.User
            A random user

        """

        Settings.dev_print("getting random user...")
        import random
        return random.choice(User.get_all_users())

    @staticmethod
    def get_recent_messagers():
        """
        Get users that have recently sent messages.

        Returns
        -------
        list
            The users that have recently sent messages

        """
        Settings.dev_print("getting recent users from messages...")
        users = []
        for user in Driver.messages_scan():
            users.append(User({"id":user}))
        return users

    ## TODO: maybe update this so it actually works?
    @staticmethod
    def get_recent_users():
        """
        Get recent users.

        Returns
        -------
        list
            The recent users

        """
        Settings.dev_print("getting recent users...")
        i = 0
        users = []
        for user in User.get_all_users():
            Settings.maybe_print("recent user: {}".format(user.username))
            users.append(user)
            i += 1
            if i == int(Settings.get_recent_user_count()): break
        return users

    @staticmethod
    def get_user_by_id(userid):
        """
        Get user by id.

        Returns
        -------
        int
            The user id

        """
        if not userid or userid == None:
            Settings.err_print("missing user id")
            return None
        for user in User.get_all_users():
            if str(user.id) == "@u"+str(userid) or str(user.id) == "@"+str(userid) or str(user.id) == str(userid):
                Settings.maybe_print("found user id: {}".format(userid))
                return user
        Settings.err_print("missing user by user id - {}".format(userid))
        return None

    @staticmethod
    def get_user_by_username(username):
        """
        Get user by username.

        Returns
        -------
        classes.User
            The user with the provided username

        """
        if not username or str(username) == "None":
            Settings.err_print("missing username!")
            return None
        for user in User.get_all_users():
            if str(user.username) == "@u"+str(username) or str(user.username) == "@"+str(username) or str(user.username) == str(username):
                Settings.maybe_print("found username: {}".format(username))
                return user
        Settings.err_print("missing user by username - {}".format(username))
        return None

    @staticmethod
    def get_users_by_list(number=None, name=None, ):
        """
        Get users by custom list.

        Returns
        -------
        list
            The users on the list

        """
        Settings.maybe_print("getting users by list: {} - {}".format(number, name))
        listUsers = []
        for user in Driver.get_list(number=number, name=name):
            Settings.maybe_print("user: {}".format(user.username))
            listUsers.append(user)
        return listUsers

    @staticmethod
    def message_user(message, username, user_id=None):

        """
        Message the user by their available username or id with the provided message data.

        Parameters
        ----------
        message : Object
            The message to send as a serialized Message object from get_message.
        """

        user = User({"username":username,"id":user_id})
        return user.message(message) 

    @staticmethod
    def read_following_local():
        """
        Read the locally saved following file.

        Returns
        -------
        list
            The locally saved followers

        """
        Settings.dev_print("getting local following...")
        users = []
        try:
            with open(str(Settings.get_users_path().replace("users.json", "following.json"))) as json_file:  
                for user in json.load(json_file)['users']:
                    users.append(User(json.loads(user)))
            Settings.maybe_print("loaded local following")
        except Exception as e:
            Settings.dev_print(e)
        return users

    @staticmethod
    def read_users_local():
        """
        Read the locally saved users file.

        Returns
        -------
        list
            The locally saved users

        """
        Settings.dev_print("getting local users...")
        users = []
        try:
            with open(str(Settings.get_users_path())) as json_file:  
                for user in json.load(json_file)['users']:
                    users.append(User(json.loads(user)))
            Settings.maybe_print("loaded local users")
        except Exception as e:
            Settings.dev_print(e)
        return users

    @staticmethod
    def read_users_messages(users=[]):
        """
        Read all the users messages.

        Parameters
        ----------
        classes.User
            A list of users to read the messages of.

        """

        if len(users) == 0: users = User.get_all_users()
        Settings.print("updating chat logs: {}".format(len(users)))
        for user in users: user.messages_read()
        # User.write_users_local(users=users)
        return users
 
    @staticmethod
    def skipUserCheck(user):
        """
        Skip user if meets flags.

        Returns
        -------
        classes.User
            The same user provided (if not skipped)

        """
        if str(user.id).lower() in Settings.get_skipped_users() or str(user.username).lower() in Settings.get_skipped_users():
            Settings.maybe_print("skipping: {}".format(user.username))
            return None
        return user

    @staticmethod
    def write_users_local(users=None):
        """
        Write to local users file.

        """
        if users is None:
            users = User.get_all_users()
        if len(users) == 0:
            Settings.maybe_print("skipping: local users save - empty")
            return
        Settings.print("saving users...")
        Settings.dev_print("local users path: "+str(Settings.get_users_path()))
        # merge with existing user data
        existingUsers = User.read_users_local()
        for user in users:
            for u in existingUsers:
                if user.equals(u):
                    user.update(u)
        data = {}
        data['users'] = []
        for user in users:
            data['users'].append(user.toJSON())
        try:
            with open(str(Settings.get_users_path()), 'w') as outfile:  
                json.dump(data, outfile, indent=4, sort_keys=True)
        except FileNotFoundError:
            Settings.err_print("missing local users!")
        except OSError:
            Settings.err_print("missing local path!")

    @staticmethod
    def write_following_local(users=None):
        """
        Write to local followers file.

        """
        if users is None:
            users = User.get_following()
        if len(users) == 0:
            Settings.maybe_print("skipping: local following save - empty following")
            return
        Settings.print("saving following...")
        Settings.dev_print("local users path: "+str(Settings.get_users_path().replace("users.json", "following.json")))
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