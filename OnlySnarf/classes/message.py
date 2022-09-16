import re
from datetime import datetime
from ..lib.driver import Driver
from ..util.settings import Settings
from .user import User
from PyInquirer import prompt
##
from ..util.validators import PriceValidator, ListValidator
from ..lib import remote as Remote
from .file import File, Folder
from .poll import Poll
from .schedule import Schedule

class Message():
    """OnlyFans message (and post) class"""

    def __init__(self):
        """
        OnlyFans message and post object

        A post is just a message on a profile with different options made available. So all posts are messages, as all messages are messages.
            Squares and rectangles.

        """

        # universal message variables
        self.text = ""
        self.files = []
        self.keywords = []
        self.performers = []
        self.price = 0 # $3 - $100
        
        # TODO: check if this is necessary
        self.hasPerformers = False # used to flag files from performer folders

        # typically related to messages only
        self.users = [] # users to send to as username or user id
        self.user_id = 0 # user to send's to known user id

        self.__initialized__ = False

    # def __str__(self):
    #     return "foo"


    def init(self):
        """Initialize."""

        if self.__initialized__: return
        self.get_text()
        # self.get_tags()
        self.get_price()
        self.get_files()
        self.get_recipients()
        # self.get_performers()
        self.__initialized__ = True

    def backup_files(self):
        """Backs up files"""

        for file in self.get_files(): file.backup()

    def delete_files(self):
        """Deletes files"""

        for file in self.get_files(): file.delete()

    def cleanup(self):
        """Processes files after a successful message or post by backing them up then deleting them"""

        self.backup_files()
        self.delete_files()

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
        return " #{}".format(" #".join(keywords)) if len(keywords) > 0 else ""

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
        return " w/ @{} ".format(" @".join(performers)) if len(performers) > 0 else ""


    def format_text(self):
        """Formats self.text with the provided keywords and performers

        
        Returns
        -------
        str
            The generated text into a string. Example:
            "This is the text. w/ @name, @name, and @name #keyword0 #keyword1"

        """

        return self.get_text().strip()
        # return "{}{}{}".format(self.get_text(),Message.format_performers(self.get_performers()),Message.format_keywords(self.get_tags())).strip()

    def get_tags(self, performers=True, again=True):
        """
        Gets the keywords (or performers) value if not none else sets it from args or prompts from script runner.
            If "performers" is equal to true then the prompt knows to fetch performers instead of keywords.
            If "again" is equal to true then the prompt knows that the user might be unsure. 
        
        Parameters
        ----------
        performers : bool
            Signal to get performers instead of keywords.

        again : bool
            Whether or not it is the script user's first time around.


        Returns
        -------
        list
            The keyword strings in a list

        """

        variable = "keywords"
        if performers: variable = "performers"
        # retrieve if set already
        if len(dict(self)[variable]) > 0: return dict(self)[variable]
        # else retrieve from args and return if exists
        variables = []
        if variable == "keywords": variables = Settings.get_tags()
        elif variable == "performers": variables = Settings.get_performers()
        if len(variables) > 0: 
            dict(self)[variable] = variables
            return variables
        # skip prompt
        if not Settings.prompt(variable): return []
        question = {
            'type': 'input',
            'name': 'keywords',
            'message': '{}:'.format(variable.camelCase()),
            'validate': ListValidator
        }
        if again: Settings.print("are you sure you've done this before, {}? ;)".format(Settings.get_username()))
        variables = prompt(question)[variable]
        variables = [n.strip() for n in variables.split(",")]
        # confirm variables or go in a circle
        # if not Settings.confirm(variables): return self.get_tags(performers=performers, again=True)
        dict(self)[variable] = variables
        return variables

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
            self.files = files
            return files
        # prompt skip
        if not Settings.is_prompt(): return []
        files = File.get_files()
        # if files is empty this all basically just skips to the end and returns blank 
        filed = []
        for file in files:
            # turn all folders into their files
            if isinstance(file, Folder): filed.extend(file.get_files())
            else:
                filed.append(file)
                # TODO
                # this goes elsewhere
                # flag that the files include a performer
                # if hasattr(file, "performer"):
                    # self.performers.append(getattr("performer", file))
        self.files = filed[:int(Settings.get_upload_max())] # reduce by max
        return self.files

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
            "price": self.get_price()
        })


    def get_price(self, again=True):
        """
        Gets the price value if not none else sets it from args or prompts.


        Parameters
        ----------
        again : bool
            Whether or not it is the script user's first time around.

        Returns
        -------
        int
            The price as an int.

        """

        if self.price: return int(self.price)
        # retrieve from args and return if exists
        price = Settings.get_price() or 0
        if price: 
            self.price = price
            return int(price)
        if not Settings.prompt("price"): return 0
        question = {
            'type': 'input',
            'name': 'price',
            'message': 'Price',
            'validate': PriceValidator,
            'filter': lambda val: int(val)
        }
        price = prompt(question)["price"]
        # if not Settings.confirm(price): return self.get_price(again=again)
        self.price = int(price)
        return int(price)

    def get_recipients(self, again=True):
        """
        Gets the recipients value if not none else sets it from args or prompts. Users 'user' from config if provided as base for list otherwise 'users'.

        Returns
        -------
        list
            Usernames in a list

        """

        if len(self.users) > 0: return self.users
        self.users = Settings.get_users()
        return self.users

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
        # prompt skip
        if not Settings.prompt("text"): return ""
        question = {
            'type': 'input',
            'name': 'text',
            'message': 'Text:'
        }
        text = prompt(question)["text"]
        # confirm text
        # if not Settings.confirm(text): return self.get_text(again=again)
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

    def send(self):
        """
        Sends a message.


        Returns
        -------
        bool
            Whether or not sending the message was successful.

        """
        try:
            self.init()
            # if not Settings.confirm("Send message?"): return False
            # if not self.get_files() and self.get_text() == "":
            #     Settings.err_print("Missing files and text!")
            #     return False
            try: 
                successes = 0
                failures = 0
                recipients = self.get_recipients()
                Settings.maybe_print("messaging users: {}".format(len(recipients)))
                for user in recipients:
                    successful = User.message_user(self.get_message(), user.username, user_id=user.id)
                    if successful: successes+=1
                    else: failures+=1
            except Exception as e:
                Settings.dev_print(e)
                failures+=1
            Settings.maybe_print("successful: {}".format(successes))
            Settings.maybe_print("failed: {}".format(failures))
            self.cleanup()
            if successes > failures: return True
        except Exception as e:
            Settings.dev_print(e)
        Settings.print("something went wrong! shnarrnf!")
        return False

    def update_keywords(self, text):
        """Sets keywords from this object's file's title"""

        return
        if len(self.get_tags()) == 0 and len(self.get_files()) > 0:
            self.keywords = self.files[0].get_parent()["title"].split(" ")
            for keyword in self.keywords:
                if str(keyword) in str(self.text):
                    self.keywords = []
            

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
        expires = Settings.get_expiration() or 0
        if expires: 
            self.expiration = expires
            return expires
        # prompt skip
        if not Settings.prompt("expiration"): return 0
        question = {
            'type': 'input',
            'name': 'expiration',
            'message': 'Expiration [any number, 999 for \'No Limit\']',
            # 'validate': 
        }
        expiration = prompt(question)["expiration"]
        # confirm expiration
        # if not Settings.confirm(expiration): return self.get_expiration(again=again)
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
        self.poll = self.poll.get()
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
            "price": self.get_price(),
            "expiration": self.get_expiration(),
            "schedule": self.get_schedule(),
            "poll": self.get_poll()
        })

    def get_schedule(self, again=True):
        """
        Gets the schedule value if not none else sets it from args or prompts.
        
        Parameters
        ----------
        again : bool
            Whether or not it is the script user's first time around.


        Returns
        -------
        Schedule
            Schedule object with proper values.

        """

        if self.schedule: return self.schedule.get()
        self.schedule = Schedule()
        return self.schedule.get()

    def send(self):
        """
        Sends a post.


        Returns
        -------
        bool
            Whether or not sending the post was successful.

        """
        try:
            self.init()
            Settings.print("post > {}".format(self.get_text()))
            # if not Settings.confirm("Send post?"): return False
            if not self.get_files() and self.get_text() == "":
                Settings.err_print("Missing files and text!")
                return False
            try:
                successes = 0
                failures = 0
                successful = Driver.post(self.get_post())
                if successful: successes+=1
                else: failures+=1
            except Exception as e:
                Settings.dev_print(e)
                failures+=1
            Settings.maybe_print("successful: {}".format(successes))
            Settings.maybe_print("failed: {}".format(failures))
            self.cleanup()
            if successes > failures: return True
        except Exception as e:
            Settings.dev_print(e)
        Settings.print("something went wrong! shnarrnf!")
        return False