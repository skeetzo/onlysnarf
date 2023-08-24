import json
import os
import random
from datetime import datetime, timedelta
from marshmallow import Schema, fields, validate, ValidationError, post_load

from ..util.colorize import colorize
from ..lib.driver import Driver
from ..util.settings import Settings
from ..webdriver import get_recent_chat_users, get_userid_by_username as WEBDRIVER_get_userid_by_username, message, read_user_messages as WEBDRIVER_read_user_messages

ALREADY_RANDOMIZED_USERS = []

# https://marshmallow.readthedocs.io/en/stable/
class UserSchema(Schema):
    username = fields.Str(required=True, error_messages={"required": "Username is required."}, validate=validate.Length(min=4))
    name = fields.Str()
    user_id = fields.Str()
    start_date = fields.DateTime()
    messages = fields.Nested(MessagesSchema(), dump_only=True)
    files = fields.Nested(FilesSchema(), dump_only=True)

    isRecent = fields.Bool(default=False)
    isFavorite = fields.Bool(default=False)
    isRenew = fields.Bool(default=False)
    isRecent = fields.Bool(default=False)
    isTagged = fields.Bool(default=False)
    isMuted = fields.Bool(default=False)
    isRestricted = fields.Bool(default=False)
    isBlocked = fields.Bool(default=False)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

class MessagesSchema(Schema):
    parsed = fields.List(fields.Str(), default=[])
    sent = fields.List(fields.Str(), default=[])
    received = fields.List(fields.Str(), default=[])

class FilesSchema(Schema):
    sent = fields.List(fields.Str(), default=[])
    received = fields.List(fields.Str(), default=[])

class User:
    """OnlyFans users."""

    def __init__(self, username, user_id, messages, start_date):
        """User object"""

        self.username = str(username).replace("@","")
        self.user_id = user_id
        self.messages = message
        self.start_date = start_date

        self.isFan = True
        self.isFollower = False

        self.isRecent = False
        self.isFavorite = False
        self.isRenew = False
        self.isRecent = False
        self.isTagged = False
        self.isMuted = False
        self.isRestricted = False
        self.isBlocked = False

    @staticmethod
    def create_user(user_data):
        schema = UserSchema()
        user = schema.load(user_data**)
        return user

    def dump(self):
        schema = UserSchema()
        result = schema.dump(self)
        # pprint(result, indent=2)
        return result

    def equals(self, user):
        """
        Equals comparison checks usernames and ids.

        Parameters
        ----------
        classes.User
            The user to compare another user object against
        """

        if (str(user.username) != "None" and str(user.username) == str(self.username)) or (str(user.user_id) != "None" and str(user.user_id) == str(self.user_id)): return True
        return False

    def get_id(self):
        """
        Get the provided ID of the User. Searches via username if necessary.

        Returns
        -------
        str
            The user id
        """

        if self.user_id: return self.user_id
        self.user_id = WEBDRIVER_get_userid_by_username(self.username)
        return self.user_id

    # TODO: possibly re-enable this
    # def messages_read(self):
    #     """
    #     Read the chat of the user.
    #     """

    #     Settings.print("reading user chat: {} ({})".format(self.username, self.user_id))
    #     # messages, messages_received, messages_sent = read_user_messages(self.username, user_id=self.user_id)
    #     # self.messages = messages
    #     # self.messages_received = messages_received
    #     # self.messages_sent = messages_sent
    #     self.messages, self.messages_received, self.messages_sent = WEBDRIVER_read_user_messages(self.username, user_id=self.user_id)
    #     # self.messages_and_timestamps = messages[1]
    #     Settings.maybe_print("chat read!")

    def update(self, user):
        for key, value in json.loads(user.dump()).items():
            setattr(self, str(key), value)

    # necessary?
    # def delete(self):
        # pass
    # def save(self):
    #     User.write_users_local([self.dump()])

    #############
    ## Statics ##
    #############

    @staticmethod
    def get_all_users_usernames():
        users = User.get_all_users()
        usernames = []
        for user in users:
            usernames.append(user.username)
        return usernames

    @staticmethod
    def get_all_users(prefer_local=True):
        """
        Get all users.

        Returns
        -------
        list
            The users

        """


        # TODO: update this to return following as well?

        Settings.dev_print("getting all users...")
        users = []
        if prefer_local:
            users = User.read_users_local()
        if len(users) == 0:
            for user in get_users_by_type(isFan=True):
                if user is None: continue
                users.append(User(user))
        Settings.maybe_print("users: {}".format(len(users)))
        User.write_users_local(users=users)
        Settings.set_prefer_local(True)
        return users



def get_users_by_type(type="fan")
    active users (fans)
    active subscriptions (followers)
    friends
    rebill on & off
    recent
    tagged
    muted
    restricted
    blocked

    # TODO: route user fetches through single fx to save calls to save user json files?





    # TODO: update with more accurate "active"ness
    # gets users from local or refreshes from onlyfans.com
    @staticmethod
    def get_active_users(prefer_local=True):
        """
        Get active users.

        Returns
        -------
        list
            The active users

        """

        Settings.dev_print("getting active users...")
        users = []
        active_users = []
        if prefer_local:
            users = User.read_users_local()
        if len(users) == 0:
            for user in WEBDRIVER_get_active_users():
                users.append(User(user, isFan=True))
        for user in users:
            if user.isFan:
                active_users.append(user)
        Settings.maybe_print("active users: {}".format(len(active_users)))
        return active_users

    @staticmethod
    def get_active_subscriptions(prefer_local=True):
        """
        Get active users.

        Returns
        -------
        list
            The active users

        """

        Settings.dev_print("getting active followers...")
        users = []
        active_users = []
        if prefer_local:
            users = User.read_following_local() # TODO: update these references to match 'subscriptions'
        if len(users) == 0:
            for user in WEBDRIVER_get_active_subscriptions():
                users.append(User(user, isFollower=True))
        for user in users:
            if user.isFollower:
                active_users.append(user)
        Settings.maybe_print("active followers: {}".format(len(active_users)))



        User.write_following_local(users=users)



        return active_users
    

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
        for user in get_users_by_type(isFollowing=True):
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
        # TODO: finish lists
        for user in Driver.get_list(number=number, name=name):
            Settings.maybe_print("user: {}".format(user.username))
            listUsers.append(user)
        return listUsers















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
            if str(user.user_id) == "@u"+str(userid) or str(user.user_id) == "@"+str(userid) or str(user.user_id) == str(userid):
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
    def get_random_user():
        """
        Get a random user.

        Returns
        -------
        classes.User
            A random user

        """

        Settings.dev_print("getting random user...")

        users = User.get_all_users_usernames()

        randomUser = None
        randomizedUsers = User.get_already_randomized_users()

        while randomUser not in randomizedUsers:
            randomUser = random.choice(users)
            if randomUser not in randomizedUsers:
                User.add_to_randomized_users(randomUser, users=randomizedUsers)
                randomizedUsers.append(randomUser)

        Settings.dev_print("random user: {}".format(randomUser))

        users = User.get_all_users()
        for user in users:
            if str(user.username) == str(randomUser):
                return user
        return User({"username":randomUser})

    # return from json file 
    @staticmethod
    def get_already_randomized_users():
        Settings.dev_print("getting already randomized users...")
        users = []
        try:
            with open(str(Settings.get_users_path().replace("users.json","random_users.json"))) as json_file:  
                for user in json.load(json_file)['randomized_users']:
                    users.append(user)
            Settings.maybe_print("loaded randomized users")
        except Exception as e:
            Settings.dev_print(e)
        return users

    # add to json file
    @staticmethod
    def add_to_randomized_users(newUser, users=[]):
        data = {}
        data['randomized_users'] = []
        for user in users:
            data['randomized_users'].append(user)
        data['randomized_users'].append(newUser)
        try:
            with open(str(Settings.get_users_path().replace("users.json","random_users.json")), 'w') as outfile:  
                json.dump(data, outfile, indent=4, sort_keys=True)
        except FileNotFoundError:
            Settings.err_print("missing random users!")
        except OSError:
            Settings.err_print("missing random users path!")









































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
        for user in get_recent_chat_users():
            users.append(User({"id":user}))
        return users

    @staticmethod
    def message_user(message, username, user_id=None):

        """
        Message the user by their available username or id with the provided message data.

        Parameters
        ----------
        message : Object
            The message to send as a serialized Message object from get_message.
        """

        if str(username).lower() == "random":
            return User.get_random_user().message(message)
        else:
            return User(username, user_id=user_id).message(message)
 

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
    def write_users_local(users=[]):
        """
        Write to local users file.

        """
        if len(users) == 0:
            users = User.get_all_users()
        if len(users) == 0:
            Settings.maybe_print("skipping: local users save - empty")
            return
        Settings.maybe_print("saving users...")
        Settings.dev_print("local users path: "+str(Settings.get_users_path()))
        # merge with existing user data
        data = {}
        data['users'] = []
        existingUsers = User.read_users_local()
        for user in users:
            for u in existingUsers:
                if user.equals(u):
                    user.update(u)
            data['users'].append(user.dump())
        try:
            with open(str(Settings.get_users_path()), 'w') as outfile:  
                json.dump(data, outfile, indent=4, sort_keys=True)
        except FileNotFoundError:
            Settings.err_print("missing local users!")
        except OSError:
            Settings.err_print("missing local path!")
        Settings.dev_print("saved users!")

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
            data['users'].append(user.dump())
        try:
            with open(str(Settings.get_users_path().replace("users.json", "following.json")), 'w') as outfile:  
                json.dump(data, outfile, indent=4, sort_keys=True)
        except FileNotFoundError:
            Settings.err_print("missing local following")
        except OSError:
            Settings.err_print("missing local path")