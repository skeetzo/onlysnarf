import json
import os
import random
import logging
from datetime import datetime, timedelta
from marshmallow import Schema, fields, validate, ValidationError, post_load, EXCLUDE

from ..util.colorize import colorize
from ..util.data import add_to_randomized_users, get_already_randomized_users, read_users_local, write_users_local
from .driver import get_recent_chat_users, get_userid_by_username as WEBDRIVER_get_userid_by_username, message as WEBDRIVER_message, get_users as WEBDRIVER_get_users
 # read_user_messages as WEBDRIVER_read_user_messages
from ..util.config import CONFIG

ALREADY_RANDOMIZED_USERS = []

class MessagesSchema(Schema):
    parsed = fields.List(fields.Str(), dump_default=[])
    sent = fields.List(fields.Str(), dump_default=[])
    received = fields.List(fields.Str(), dump_default=[])

class FilesSchema(Schema):
    sent = fields.List(fields.Str(), dump_default=[])
    received = fields.List(fields.Str(), dump_default=[])

# https://marshmallow.readthedocs.io/en/stable/
class UserSchema(Schema):
    username = fields.Str(required=True, error_messages={"required": "Username is required."}, validate=validate.Length(min=4))
    name = fields.Str()
    user_id = fields.Str()
    # start_date = fields.DateTime()
    messages = fields.Nested(MessagesSchema(unknown=EXCLUDE))
    files = fields.Nested(FilesSchema(unknown=EXCLUDE))

    isFan = fields.Bool(dump_default=False)
    isFollower = fields.Bool(dump_default=False)

    isRecent = fields.Bool(dump_default=False)
    isFavorite = fields.Bool(dump_default=False)
    isRenew = fields.Bool(dump_default=False)
    isRecent = fields.Bool(dump_default=False)
    isTagged = fields.Bool(dump_default=False)
    isMuted = fields.Bool(dump_default=False)
    isRestricted = fields.Bool(dump_default=False)
    isBlocked = fields.Bool(dump_default=False)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)

class User:
    """OnlyFans users."""

    def __init__(self, username, name="", user_id="", messages=[], isFan=False, isFollower=False, isFavorite=False, isRecent=False, isRenew=False, isTagged=False, isMuted=False, isRestricted=False, isBlocked=False):
        """User object"""

        self.username = str(username).replace("@","")
        self.name = name
        self.user_id = user_id
        self.messages = messages
        # self.start_date = start_date
        #
        self.isFan = isFan
        self.isFollower = isFollower
        #
        self.isRecent = isRecent
        self.isFavorite = isFavorite
        self.isRenew = isRenew
        self.isTagged = isTagged
        self.isMuted = isMuted
        self.isRestricted = isRestricted
        self.isBlocked = isBlocked

    @staticmethod
    def create_user(user_data):
        schema = UserSchema(unknown=EXCLUDE)
        if user_data["username"] == "random":
            user_data["username"] = User.get_random_user().username
        return schema.load(user_data)

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

    #     logging.info("reading user chat: {} ({})".format(self.username, self.user_id))
    #     # messages, messages_received, messages_sent = read_user_messages(self.username, user_id=self.user_id)
    #     # self.messages = messages
    #     # self.messages_received = messages_received
    #     # self.messages_sent = messages_sent
    #     self.messages, self.messages_received, self.messages_sent = WEBDRIVER_read_user_messages(self.username, user_id=self.user_id)
    #     # self.messages_and_timestamps = messages[1]
    #     logging.debug("chat read!")

    def update(self, user):
        for key, value in user.dump().items():
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

        logging.debug("getting all users...")
        users = []
        if CONFIG["prefer_local"]:
            users = read_users_local()
        if len(users) == 0:
            for user in WEBDRIVER_get_users(isFan=True, isFollower=True):
                users.append(User.create_user(user))
        logging.debug(f"users: {len(users)}")
        # write_users_local(users)
        CONFIG["prefer_local"] = True
        return users

    @staticmethod
    def get_random_user(isFollower=False):
        """
        Get a random user.

        Returns
        -------
        classes.User
            A random user

        """




        # TODO: fix the users only returning the last in the array for whatever reason



        logging.debug("getting random user...")
        users = User.get_all_users()
        randomizedUsers = get_already_randomized_users()
        # check each user in users
        # if user is not in random users, return user
        randomUser = random.choice(users)
        found = False
        i = 0
        while not found and i < len(users):
            randomUser = random.choice(users)
            if not isFollower and randomUser.isFollower:
                # randomUser = None
                continue
            i+=1
            # for each user in random users, if the user is equal to the current random user then mark user as found; exit when a user is not found
            for user in randomizedUsers:
                if randomUser.equal(user):
                    found = True
            # if not found:
                # randomUser = None
            # if not found: break
        add_to_randomized_users(randomUser)
        logging.debug(f"random user: {randomUser.username}")
        return randomUser

    # TODO: use this function at all?
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
        logging.debug(f"getting users: {typeOf}")
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
        logging.debug(f"found users: {len(foundUsers)}")
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

    #     logging.debug("getting users that have never been messaged...")
    #     users = []
    #     for user in User.get_all_users():
    #         if len(user.messages_received) == 0:
    #             logging.debug("never messaged user: {}".format(user.username))
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

        logging.debug("getting new users...")
        newUsers = []
        date_ = datetime.today() - timedelta(days=10)
        for user in User.get_all_users():
            if not user.start_date: continue
            started = datetime.strptime(str(user.start_date),"%b %d, %Y")
            # logging.debug("date: "+str(date_)+" - "+str(started))
            if started < date_: continue
            logging.debug("new user: {}".format(user.username))
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
    #     logging.debug("getting users by list: {} - {}".format(number, name))
    #     listUsers = []
    #     for user in Driver.get_list(number=number, name=name):
    #         logging.debug("user: {}".format(user.username))
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
            logging.error("missing user id")
            return None
        for user in User.get_all_users():
            if str(user.user_id) == "@u"+str(userid) or str(user.user_id) == "@"+str(userid) or str(user.user_id) == str(userid):
                logging.debug("found user id: {}".format(userid))
                return user
        logging.error("missing user by user id - {}".format(userid))
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
            logging.error("missing username!")
            return None
        for user in User.get_all_users():
            if str(user.username) == "@u"+str(username) or str(user.username) == "@"+str(username) or str(user.username) == str(username):
                logging.debug("found username: {}".format(username))
                return user
        logging.error("missing user by username - {}".format(username))
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
        logging.debug("getting recent users from messages...")
        users = []
        for user in get_recent_chat_users():
            users.append(User.create_user({"id":user}))
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
            return User.get_random_user().WEBDRIVER_message(message)
        else:
            return User.create_user(username, user_id=user_id).WEBDRIVER_message(message)
 

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
        logging.info("updating chat logs: {}".format(len(users)))
        for user in users: user.messages_read()
        # User.write_users_local(users=users)
        return users

















    