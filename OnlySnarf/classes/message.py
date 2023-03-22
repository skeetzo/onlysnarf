import re
from datetime import datetime
from decimal import Decimal
from re import sub
##
from ..lib.driver import Driver
from .file import File, Folder
from .poll import Poll
from .user import User
from ..util.settings import Settings
from .schedule import Schedule

class Message():
    """OnlyFans message (and post) class"""

    def __init__(self, users=[]):
        """
        OnlyFans message and post object

        A post is just a message on a profile with different options made available. So all posts are messages, as all messages are messages.
            Squares and rectangles.

        """

        # universal message variables
        self.text = ""
        self.files = []
        self.performers = []
        self.price = 0 # $3 - $100
        self.tags = []
        self.__initialized__ = False

    def init(self):
        """Initialize."""

        if self.__initialized__: return
        self.get_text()
        self.get_tags()
        self.get_price()
        self.get_files()
        self.get_performers()
        self.__initialized__ = True

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

        # ternary: a if condition else b
        return "#{}".format(" #".join(keywords)) if len(keywords) > 0 else ""

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

        # ternary: a if condition else b
        return " @{} ".format(" @".join(performers)) if len(performers) > 0 else ""


    def format_text(self):
        """Formats self.text with the provided keywords and performers

        
        Returns
        -------
        str
            The generated text into a string. Example:
            "This is the text. @name, @name, and @name #keyword0 #keyword1"

        """

        return "{}{}{}".format(self.get_text(), Message.format_performers(self.get_performers()), Message.format_keywords(self.get_tags())).strip()

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
            Settings.maybe_print("message contains (tip): {}".format(amount))
            return True, int(amount)
        elif re.search(r"I\'ve contributed \$[0-9]*\.00 to your Campaign", text):
            amount = re.match(r'I\'ve contributed \$([0-9]*)\.00 to your Campaign', text).group(1)
            Settings.maybe_print("message contains (campaign): {}".format(amount))
            return True, int(amount)
        return False, 0

    def get_files(self):
        """
        Gets files from args specified source or prompts as necessary.

        Uses appropriate file select method as specified by runtime args:
        - remote (server, ipfs)
        - local

        Parameters
        ----------
        again : bool
            Whether or not it is the script user's first time around.

        Returns
        -------
        list
            Files in a list

        """

        if len(self.files) > 0: return self.files[:int(Settings.get_upload_max())]
        files = Settings.get_input_as_files()
        if len(files) > 0:
            Settings.dev_print("fetched input files for upload")
            self.files = files[:int(Settings.get_upload_max())] # reduce by max
            # self.files = files
            # return files
        return self.files
        # files = Folder.get_files()
        # if files is empty this all basically just skips to the end and returns blank 
        # filed = []
        # for file in files:
            # turn all folders into their files
            # if isinstance(file, Folder): filed.extend(file.get_files())
            # else:
                # filed.append(file)
                # TODO
                # this goes elsewhere
                # flag that the files include a performer
                # if hasattr(file, "performer"):
                    # self.performers.append(getattr("performer", file))

    def get_message(self):
        """
        Gets the message as a serialized JSON object.


        Returns
        -------
        Object
            The message as an object.

        """

        return dict({
            "text": self.format_text(),
            "files": self.get_files(),
            "performers": self.get_performers(),
            "price": self.get_price(),
            "tags": self.get_tags()
        })

    def get_performers(self):
        """
        Gets the performers for the text.

        Returns
        -------
        list
            The performers

        """

        if len(self.performers) > 0: return self.performers
        self.performers = Settings.get_performers()
        return self.performers

    def get_price(self):
        """
        Gets the price value if not none else sets it from args or prompts.


        Returns
        -------
        int
            The price

        """

        if self.price: return self.price
        price = Settings.get_price()
        if str(price) == "0": return 0
        priceMin = Settings.get_price_minimum()
        priceMax = Settings.get_price_maximum()
        if str(price) == "max": price = priceMax
        elif str(price) == "min": price = priceMin
        elif Decimal(sub(r'[^\d.]', '', str(price))) < Decimal(priceMin):
            Settings.warn_print("price too low: {} < {}".format(price, priceMin))
            Settings.maybe_print("adjusting price to minimum...")
            price = priceMin
        elif Decimal(sub(r'[^\d.]', '', str(price))) > Decimal(priceMax):
            Settings.warn_print("price too high: {} < {}".format(price, priceMax))
            Settings.maybe_print("adjusting price to maximum...")
            price = priceMax    
        self.price = price
        return self.price

    def get_tags(self):
        """
        Gets the tags for the text.

        Returns
        -------
        list
            The tags

        """

        if len(self.tags) > 0: return self.tags
        self.tags = Settings.get_tags()
        return self.tags

    def get_text(self, again=True):
        """
        Gets the text value if not none else sets it from args or prompts.


        Parameters
        ----------
        again : bool
            Whether or not it is the script user's first time around.

        Returns
        -------
        str
            The text to enter.

        """

        if self.text != "": return self.text
        # retrieve from args and return if exists
        text = Settings.get_text()
        if text != "": 
            self.text = text
            return text
        text = self.get_text_from_filename()
        if text != "":
            self.text = text
            return text
        self.text = text
        return self.text

    def get_text_from_filename(self):
        """Gets text from this object's file's title"""

        if not self.get_files(): return ""
        text = self.files[0].get_title()
        # if "_" in str(self.text):
        if re.match("[0-9]_[0-9]", text) is not None:
            texttext = self.files[0].get_parent()["title"]
        else:
            try: 
                int(text)
                # is a simple int
                if int(text) > 20:
                    text = self.files[0].get_parent()["title"]
            except Exception as e:
                # not a simple int
                # do nothing cause probably set already
                pass
        text = text.replace("_", " ")
        # redo keyword parsing (unsure if necessary call)
        text = self.update_tags(text)
        return text

    def send(self, username, user_id=None):
        """
        Sends a message.


        Returns
        -------
        bool
            Whether or not sending the message was successful.

        """

        self.init()
        return User.message_user(self.get_message(), username, user_id=user_id)            

class Post(Message):
    """OnlyFans message (and post) class"""

    def __init__(self):
        """
        OnlyFans post object

        A post is just a message on a profile with different options made available. So all posts are messages, as all messages are messages.
            Squares and rectangles.

        """

        super().__init__()
        self.expiration = 0
        self.poll = None
        self.schedule = None

    # def __str__(self):
    #     return "fooPost"

    def init(self):
        """Initialize."""

        super().init()
        self.__initialized__ = False
        self.get_poll()
        self.get_schedule()
        self.get_expiration()
        self.__initialized__ = True

    def get_expiration(self, again=True):
        """
        Gets the expiration value if not none else sets it from args or prompts.
        
        Parameters
        ----------
        again : bool
            Whether or not it is the script user's first time around.


        Returns
        -------
        int
            The expiration as an int.

        """

        if self.expiration: return self.expiration
        # retrieve from args and return if exists
        expiration = Settings.get_expiration() or 0
        if expiration: 
            self.expiration = expiration
            return expiration
        self.expiration = expiration
        return self.expiration

    def get_poll(self, again=True):
        """
        Gets the poll value if not none else sets it from args or prompts.
        
        Parameters
        ----------
        again : bool
            Whether or not it is the script user's first time around.


        Returns
        -------
        Poll
            Poll object with proper values

        """

        # check if poll is ready
        if self.poll: return self.poll
        self.poll = Poll()
        return self.poll

    def get_post(self):
        """
        Gets the message as a serialized JSON object.


        Returns
        -------
        Object
            The message as an object.

        """

        return dict({
            "text": self.format_text(),
            "files": self.get_files(),
            "performers": self.get_performers(),
            "price": self.get_price(),
            "expiration": self.get_expiration(),
            "schedule": self.get_schedule(),
            "poll": self.get_poll(),
            "tags": self.get_tags()
        })

    def get_schedule(self):
        """
        Gets the schedule value if not none else sets it from args or prompts.

        Returns
        -------
        Schedule
            Schedule object with proper values.

        """

        if self.schedule: return self.schedule
        self.schedule = Schedule()
        return self.schedule

    def send(self):
        """
        Sends a post.


        Returns
        -------
        bool
            Whether or not sending the post was successful.

        """
        
        self.init()
        Settings.print("post > {}".format(self.get_text()))
        if not self.get_files() and self.get_text() == "":
            Settings.err_print("Missing files and text!")
            return False
        return Driver.post(self.get_post())
            
