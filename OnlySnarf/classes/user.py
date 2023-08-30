import json
import os
import random
from datetime import datetime, timedelta
from marshmallow import Schema, fields, validate, ValidationError, post_load

from ..util.colorize import colorize
from ..util.data import add_to_randomized_users, get_already_randomized_users, read_users_local, write_users_local
from ..util.settings import Settings
from .driver import get_recent_chat_users, get_userid_by_username as WEBDRIVER_get_userid_by_username, message
 # read_user_messages as WEBDRIVER_read_user_messages

ALREADY_RANDOMIZED_USERS = []

class MessagesSchema(Schema):
    parsed = fields.List(fields.Str(), default=[])
    sent = fields.List(fields.Str(), default=[])
    received = fields.List(fields.Str(), default=[])

class FilesSchema(Schema):
    sent = fields.List(fields.Str(), default=[])
    received = fields.List(fields.Str(), default=[])

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
        user = schema.load(**user_data)
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
    def get_all_users():
        """
        Get all users.

        Returns
        -------
        list
            The users

        """

        Settings.dev_print("getting all users...")
        users = []
        if Settings.is_prefer_local():
            users = read_users_local()
        if len(users) == 0:
            for user in get_users_by_type(isFan=True, isFollower=True):
                users.append(User(user))
        Settings.maybe_print(f"users: {len(users)}")
        write_users_local(users)
        Settings.set_prefer_local(True)
        return users

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
        users = User.get_all_users()
        randomizedUsers = get_already_randomized_users()
        # check each user in users
        # if user is not in random users, return user
        randomUser = random.choice(users)
        while randomUser:
            found = False
            randomUser = random.choice(users)
            for user in randomizedUsers:
                if randomUser.equal(user):
                    found = True
            if not found: break
        add_to_randomized_users(randomUser)
        Settings.dev_print(f"random user: {randomUser.username}")
        return randomUser

    # TODO: change to enum?
    # active users (fans)
    # active subscriptions (followers)
    # friends
    # rebill on & off
    # recent
    # tagged
    # muted
    # restricted
    # blocked
    @staticmethod
    def get_users_by_type(typeOf="fan"):
        Settings.dev_print(f"getting users: {typeOf}")
        users = User.get_all_users()
        foundUsers = []
        for user in users:
            if typeOf == "fan" and user.isFan:
                foundUsers.append(user)
            elif typeOf == "follower" and user.isFollower:
                foundUsers.append(user)
            elif typeOf == "friend" and user.isFriend:
                foundUsers.append(user)
            elif typeOf == "renew_on" and user.isRenew:
                foundUsers.append(user)
            elif typeOf == "renew_off" and not user.isRenew:
                foundUsers.append(user)
            elif typeOf == "recent" and user.isRecent:
                foundUsers.append(user)
            elif typeOf == "tagged" and user.isTagged:
                foundUsers.append(user)
            elif typeOf == "muted" and user.isMuted:
                foundUsers.append(user)
            elif typeOf == "restricted" and user.isRestricted:
                foundUsers.append(user)
            elif typeOf == "blocked" and user.isBlocked:
                foundUsers.append(user)
        Settings.maybe_print(f"found users: {len(foundUsers)}")
        return foundUsers    

    # TODO: use this?
    # @staticmethod
    # def get_never_messaged_users():
    #     """
    #     Get all users that have never been messaged before.

    #     Returns
    #     -------
    #     list
    #         The users that have not been messaged

    #     """

    #     Settings.dev_print("getting users that have never been messaged...")
    #     users = []
    #     for user in User.get_all_users():
    #         if len(user.messages_received) == 0:
    #             Settings.maybe_print("never messaged user: {}".format(user.username))
    #             users.append(user)
    #     return users

    # TODO: test and actually use this
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

    # TODO: finish lists
    # @staticmethod
    # def get_users_by_list(number=None, name=None, ):
    #     """
    #     Get users by custom list.

    #     Returns
    #     -------
    #     list
    #         The users on the list

    #     """
    #     Settings.maybe_print("getting users by list: {} - {}".format(number, name))
    #     listUsers = []
    #     for user in Driver.get_list(number=number, name=name):
    #         Settings.maybe_print("user: {}".format(user.username))
    #         listUsers.append(user)
    #     return listUsers

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




































    














































    # i don't think i really want these to be here?


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

















    