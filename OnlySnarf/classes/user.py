import json
import os
import random
import logging
logger = logging.getLogger(__name__)
from datetime import datetime, timedelta
from marshmallow import Schema, fields, validate, ValidationError, post_load, EXCLUDE

from ..lib.driver import get_recent_chat_users, get_userid_by_username as WEBDRIVER_get_userid_by_username, message as WEBDRIVER_message, get_users as WEBDRIVER_get_users
from ..util.colorize import colorize
from ..util.data import add_to_randomized_users, reset_random_users, read_users_local, write_users_local
 # read_user_messages as WEBDRIVER_read_user_messages
from ..util.config import CONFIG

ALREADY_RANDOMIZED_USERS = []
USER_CACHE_BY_TYPE = {}

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

    isFriend = fields.Bool(dump_default=False)
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

USER_CACHE = []

class User:
    """OnlyFans users."""

    def __init__(self, username, name="", user_id="", files=[], messages=[], isFan=False, isFollower=False, isFavorite=False, isFriend=False, isRecent=False, isRenew=False, isTagged=False, isMuted=False, isRestricted=False, isBlocked=False):
        """User object"""

        self.username = User.format_username(username)
        self.name = name
        self.user_id = user_id
        self.messages = messages
        self.files = files
        # self.start_date = start_date
        #
        self.isFan = isFan
        self.isFollower = isFollower
        #
        self.isFriend = isFriend
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

        if isinstance(user, User) and str(self.username) == str(user.username):
            return True
        elif isinstance(user, dict) and str(self.username) == str(user["username"]):
            return True
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
        try:
            if isinstance(user, User):
                for key, value in user.dumps().items():
                    setattr(self, str(key), value)
            elif isinstance(user, dict):
                for key, value in user.items():
                    setattr(self, str(key), value)
        except Exception as e:
            logging.error(e)

    # necessary?
    # def delete(self):
        # pass
    # def save(self):
    #     User.write_users_local([self.dump()])

    #############
    ## Statics ##
    #############

    @staticmethod
    def format_username(username):
        if username == "random":
            username = User.get_random_user().username
        return str(username).replace("@","")

    @staticmethod
    def save_users(users):
        user_objects = []
        for user in users:
            if not isinstance(user, User):
                user = User.create_user(user)
            user_objects.append(user)
        write_users_local(user_objects)

    @staticmethod
    def get_all_users(refresh=False):
        """
        Get all users.

        Returns
        -------
        list
            The users

        """

        logger.debug("getting all users...")
        try:
            global USER_CACHE
            if len(USER_CACHE) > 0 and not refresh:
                logger.debug(f"cached users: {len(USER_CACHE)}")
                return USER_CACHE
            USER_CACHE = []
            if CONFIG["prefer_local"] and not refresh:
                user_objects, randomized_users = read_users_local()
                for user_object in user_objects:
                    USER_CACHE.append(User.create_user(user_object))
                logger.debug(f"local users: {len(USER_CACHE)}")
                return USER_CACHE
            for user in WEBDRIVER_get_users(isFan=True, isFollower=True):
                USER_CACHE.append(User.create_user(user))
            User.save_users(USER_CACHE)
            logger.debug(f"users: {len(USER_CACHE)}")
            return USER_CACHE
        except Exception as e:
            logger.error(e)
        return []

    # check each user in users
    # if user is not in random users, return user
    @staticmethod
    def get_random_user(isFollower=False, reattempt=False):
        """
        Get a random user.

        Returns
        -------
        classes.User
            A random user

        """

        logger.debug("getting random user...")
        users = User.get_all_users()
        local_users, random_users = read_users_local()
        randomUser = None
        i = 0
        while not randomUser and i < len(users):
            i+=1
            randomUser = random.choice(users)
            # print(f"random user: {randomUser.username}")
            # print(randomUser.dump())
            if randomUser.isFollower and isFollower:
                # print("IS FOLLOWER")
                # randomUser = None
                continue
            if not randomUser: continue
            # print("IS FAN")
            for user in random_users:
                if randomUser and randomUser.equals(user):
                    randomUser = None
        if not randomUser:
            if not reattempt:
                logger.warning("partially failed to find random user!")
                reset_random_users()
                return User.get_random_user(isFollower=isFollower, reattempt=reattempt)
            else:
                raise Exception("completely failed to find random user!")                
        logger.debug(f"random user: {randomUser.username}")
        add_to_randomized_users(randomUser)
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
    def get_users_by_type(typeOf="fan", refresh=False):
        logger.debug(f"getting users: {typeOf}")

        def return_type(typeOf, user_cache):
            foundUsers = []
            for user in user_cache:
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
            global USER_CACHE_BY_TYPE
            USER_CACHE_BY_TYPE[typeOf] = foundUsers
            logger.debug(f"found users of type {typeOf}: {len(foundUsers)}")
            return foundUsers

        # copied format from get_all_users
        global USER_CACHE_BY_TYPE
        if not USER_CACHE_BY_TYPE.get(typeOf): USER_CACHE_BY_TYPE[typeOf] = []
        if len(USER_CACHE_BY_TYPE[typeOf]) > 0 and not refresh:
            return return_type(typeOf, USER_CACHE_BY_TYPE[typeOf])
        USER_CACHE_BY_TYPE[typeOf] = []
        if CONFIG["prefer_local"] and not refresh:
            user_objects, randomized_users = read_users_local()
            for user_object in user_objects:
                USER_CACHE_BY_TYPE[typeOf].append(User.create_user(user_object))
            return return_type(typeOf, USER_CACHE_BY_TYPE[typeOf])

        # only return one or the other if they're specifically requested, otherwise all the other types could be either a fan or a follower
        isFan = True
        isFollower = True
        if typeOf == "fan":
            isFollower = False
        elif typeOf == "follower":
            isFan = False

        for user in WEBDRIVER_get_users(isFan=isFan, isFollower=isFollower):
            USER_CACHE_BY_TYPE[typeOf].append(User.create_user(user))

        return return_type(typeOf, USER_CACHE_BY_TYPE[typeOf])

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

    #     logger.debug("getting users that have never been messaged...")
    #     users = []
    #     for user in User.get_all_users():
    #         if len(user.messages_received) == 0:
    #             logger.debug("never messaged user: {}".format(user.username))
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

        logger.debug("getting new users...")
        newUsers = []
        date_ = datetime.today() - timedelta(days=10)
        for user in User.get_all_users():
            if not user.start_date: continue
            started = datetime.strptime(str(user.start_date),"%b %d, %Y")
            # logger.debug("date: "+str(date_)+" - "+str(started))
            if started < date_: continue
            logger.debug("new user: {}".format(user.username))
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
    #     logger.debug("getting users by list: {} - {}".format(number, name))
    #     listUsers = []
    #     for user in Driver.get_list(number=number, name=name):
    #         logger.debug("user: {}".format(user.username))
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
            logger.error("missing user id")
            return None
        for user in User.get_all_users():
            if str(user.user_id) == "@u"+str(userid) or str(user.user_id) == "@"+str(userid) or str(user.user_id) == str(userid):
                logger.debug("found user id: {}".format(userid))
                return user
        logger.error("missing user by user id - {}".format(userid))
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
            logger.error("missing username!")
            return None
        for user in User.get_all_users():
            if str(user.username) == "@u"+str(username) or str(user.username) == "@"+str(username) or str(user.username) == str(username):
                logger.debug("found username: {}".format(username))
                return user
        logger.error("missing user by username - {}".format(username))
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
        logger.debug("getting recent users from messages...")
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
        logger.info("updating chat logs: {}".format(len(users)))
        for user in users: user.messages_read()
        return users

















    