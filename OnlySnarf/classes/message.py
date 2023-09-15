
import logging
import re
from datetime import datetime
from decimal import Decimal
from re import sub

from .file import File, Folder
from .poll import Poll
from .schedule import Schedule
from .user import User
from ..lib.driver import message as WEBDRIVER_message, post as WEBDRIVER_post
from ..util.defaults import PRICE_MAXIMUM, PRICE_MINIMUM, SCHEDULE
from ..util.config import CONFIG

from marshmallow import Schema, fields, validate, post_load, EXCLUDE

class Message():
    """OnlyFans message (and post) class"""

    def __init__(self, files=[], keywords=[], performers=[], price=0, recipients=[], schedule={}, text="", includes=[], excludes=[]):
        """
        OnlyFans message and post object

        A post is just a message on a profile with different options made available.

        """

        # BUG: for whatever reason, prior formatting fucks over the isinstance reconizing the File object; maybe fix import in uploads?
        self.files = files
        # self.files = Message.format_files(files)
        self.keywords = list(set([k.strip() for k in keywords]))
        self.performers = list(set([p.strip() for p in performers]))
        self.price = Message.format_price(price)
        self.recipients = list(set([username.replace("@","") for username in recipients])) # usernames
        self.includes = list(set([username.replace("@","") for username in includes]))
        self.excludes = list(set([username.replace("@","") for username in excludes]))
        self.schedule = Message.format_schedule(schedule)        
        self.text = Message.format_text(text, self.keywords, self.performers, self.files)

    @staticmethod
    def create_message(message_data):
        # TODO: possibly update these formatting / validation steps?
        new_recipients = []
        for recipient in message_data["recipients"]:
            if recipient.lower().strip() == "random":
                new_recipients.append(User.get_random_user().username)
            else:
                new_recipients.append(recipient)
        message_data["recipients"] = new_recipients
        if message_data["input"]:
            message_data["files"] = message_data["input"]
        schema = MessageSchema(unknown=EXCLUDE)
        return schema.load(message_data)

    def dump(self):
        schema = MessageSchema()
        return schema.dump(self)

    @staticmethod
    def format_keywords(keywords):
        """
        Formats the list provided into a combined string with a # in front of each value.

        Parameters
        ----------
        keywords : list
            List of keywords as strings

        Returns
        -------
        str
            The generated keywords into a string
        """

        return f"#{' #'.join(keywords)}" if len(keywords) > 0 else ""

    @staticmethod
    def format_performers(performers):
        """
        Formats the list provided into a combined string with an @ in front of each value.
            A space is added before @ to close performer search modal (???).

        Parameters
        ----------
        performers : list
            List of performers usernames as strings

        Returns
        -------
        str
            The generated performers into a string
        """

        return f"@{' @'.join(performers)} " if len(performers) > 0 else ""

    @staticmethod
    def format_text(text, keywords, performers, files):
        """Formats self.text with the provided keywords and performers

        
        Returns
        -------
        str
            The generated text into a string. Example:
            "This is the text. @name, @name, and @name #keyword0 #keyword1"

        """

        if "@" in text  or "#" in text: return text # BUG: return if text has already been formatted
        if not text and len(keywords) == 0 and len(performers) == 0 and len(files) == 0:
            logging.warning("formatting empty message!")
            return ""
        if not text and len(files) > 0:
            text = Message.get_text_from_filename(files[0])
        return f"{text} {Message.format_performers(performers)} {Message.format_keywords(keywords)}".strip()

    @staticmethod
    def format_schedule(scheduleArgs):
        return Schedule.create_schedule(scheduleArgs).dump()

    # TODO: reintegrate upload max
    @staticmethod
    def format_files(file_paths):
        files = []
        if len(file_paths) > 0:
            # for file in files[:int(CONFIG["upload_max"])]:
            for file in file_paths:
                if not isinstance(file, File):
                    files.append(File(file))
                else:
                    files.append(file)
        # files = files[:int(CONFIG["upload_max"])] # reduce by max
        return files

    @staticmethod
    def format_price(price):
        if not price or str(price) == "0": return 0
        if str(price) == "max": return Decimal(PRICE_MAXIMUM)
        elif str(price) == "min": return Decimal(PRICE_MINIMUM)
        elif Decimal(sub(r'[^\d.]', '', str(price))) < Decimal(PRICE_MINIMUM):
            logging.warning(f"price too low: {price} < {PRICE_MINIMUM}")
            logging.debug("adjusting price to minimum...")
            return Decimal(PRICE_MINIMUM)
        elif Decimal(sub(r'[^\d.]', '', str(price))) > Decimal(PRICE_MAXIMUM):
            logging.warning(f"price too high: {price} < {PRICE_MAXIMUM}")
            logging.debug("adjusting price to maximum...")
            return Decimal(PRICE_MAXIMUM)    
        return Decimal(price)

    # TODO: format filename better, possibly grab text from parent folder instead
    @staticmethod
    def get_text_from_filename(file_object):
        """Gets text from this object's file's title"""

        # if not self.get_files(): return ""
        text = file_object.get_title()

        return text.replace("_", " ")

    # TODO: add updates to user object upon successful message?
    def on_success(self):

        # TODO: if was sent to 'all' or 'recent' then recipients might be empty

        # add files to list of files sent to help prevent duplicates
        # add message text to list of messages (cause why not, though it gets scraped anyways eventually)

        users = []
        for username in self.recipients:
            user = User.get_user_by_username(username)
            user.messages["sent"].append(self.text)
            user.files["sent"].extend([file.get_title() if isinstance(file, File) else file for file in self.files])
            user.files["sent"].extend(self.files)
            user.files["sent"] = list(set(user.files["sent"])) # prevent duplicates
            users.append(user)
        User.save_users(users)

    def send(self):
        """
        Sends this message.


        Returns
        -------
        bool
            Whether or not sending the message was successful.

        """

        if WEBDRIVER_message(self.dump()):
            self.on_success()        
            return True
        return False
            
########################################################################################################################            
########################################################################################################################
########################################################################################################################

    # TODO: probably move this to webdriver equivalent
    @staticmethod
    def is_tip(text):
        """
        Checks if the text contains a tip amount.

        Parameters
        ----------
        text : str
            The text to parse

        Returns
        -------
        bool
            Whether the text contains a tip or not
        int
            The tip amount contained, default 0

        """

        if re.search(r'I sent you a \$[0-9]*\.00 tip ♥', text):
            amount = re.match(r'I sent you a \$([0-9]*)\.00 tip ♥', text).group(1)
            logging.debug("message contains (tip): {}".format(amount))
            return True, int(amount)
        elif re.search(r"I\'ve contributed \$[0-9]*\.00 to your Campaign", text):
            amount = re.match(r'I\'ve contributed \$([0-9]*)\.00 to your Campaign', text).group(1)
            logging.debug("message contains (campaign): {}".format(amount))
            return True, int(amount)
        return False, 0

########################################################################################################################            
########################################################################################################################
########################################################################################################################

class Post(Message):
    """OnlyFans message (and post) class"""

    def __init__(self, expiration=0, poll={}, **kwargs):
        """
        OnlyFans post object

        A post is just a message on a profile with different options made available. So all posts are messages, as all messages are messages.
            Squares and rectangles.

        """

        super().__init__(**kwargs)
        self.expiration = expiration
        self.poll = Post.format_poll(poll)

    @staticmethod
    def create_post(post_data):
        schema = PostSchema(unknown=EXCLUDE)
        return schema.load(post_data)

    def dump(self):
        schema = PostSchema()
        result = schema.dump(self)
        return result

    @staticmethod
    def format_poll(pollArgs):
        print("poll")
        print(pollArgs)
        return Poll(**pollArgs).dump()

    def send(self):
        """
        Sends this post.


        Returns
        -------
        bool
            Whether or not sending the post was successful.

        """

        logging.info("Posting...")
        if not self.files and not self.text:
            logging.error("Missing files and text!")
            return False
        return WEBDRIVER_post(self.dump())
            

# https://marshmallow.readthedocs.io/en/stable/
class MessageSchema(Schema):
    __model__ = Message

    text = fields.Str(default="")
    files = fields.List(fields.Str(), default=[])
    keywords = fields.List(fields.Str(), default=[])
    performers = fields.List(fields.Str(), default=[])
    price = fields.Float(validate=validate.Range(min=0, max=PRICE_MAXIMUM))
    schedule = fields.Dict()
    recipients = fields.List(fields.Str(), default=[])
    includes = fields.List(fields.Str(), default=[])
    excludes = fields.List(fields.Str(), default=[])

    @post_load
    def make_message(self, data, **kwargs):
        return type(self).__model__(**data)


class PostSchema(MessageSchema):
    __model__ = Post

    expiration = fields.Int(default=0)
    poll = fields.Dict()

    @post_load
    def make_post(self, data, **kwargs):
        return type(self).__model__(**data.dump())
