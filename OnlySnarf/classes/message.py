import re
from datetime import datetime
from ..lib.driver import Driver
from ..util.settings import Settings
from .user import User
from PyInquirer import prompt
##
from ..util.validators import PriceValidator, ExpirationValidator, ListValidator
from ..lib import remote as Remote
from .file import File, Folder
from .poll import Poll
from .schedule import Schedule

class Message():
    """OnlyFans message (and post) class"""

    def __init__(self):
        """
        OnlyFans message and post object

        A post is just a message on a profile with different options made available.

        """

        # universal message variables
        self.text = None
        self.files = []
        self.keywords = []
        self.performers = []
        self.hasPerformers = False # used to flag files from performer folders
        ## message only variables
        self.price = None # $3 - $100
        self.users = [] # users to send to
        ## post only variables
        self.expiration = None
        self.poll = None
        self.schedule = None
        ##
        self.gotten = False

    def backup_files(self):
        """Backs up files"""

        for file in self.get_files():
            file.backup()

    def delete_files(self):
        """Deletes files"""

        for file in self.get_files():
            file.delete()

    def cleanup_files(self):
        """Processes files after a successful message or post by backing them up then deleting them"""

        self.backup_files()
        self.delete_files()

    @staticmethod
    def format_keywords(keywords):
        """
        Formats the list provided into a combined string with a # in front of each value

        Parameters
        ----------
        keywords : list
            List of keywords as strings

        Returns
        -------
        str
            The generated keywords into a string
        """

        if len(keywords) > 0: return " #{}".format(" #".join(keywords))
        return ""

    @staticmethod
    def format_performers(performers): # spaced added after @ to close performer search modal
        """
        Formats the list provided into a combined string with an @ in front of each value

        Parameters
        ----------
        performers : list
            List of performers usernames as strings

        Returns
        -------
        str
            The generated performers into a string
        """

        if len(performers) > 0: return " w/ @{} ".format(" @".join(performers))
        return ""
            

    def format_text(self):
        """Formats self.text with the provided keywords and performers"""

        return "{}{}{}".format(self.get_text(),
            Message.format_performers(self.get_performers()),
            Message.format_keywords(self.get_keywords())).strip()

    def get_keywords(self):
        """
        Gets the keywords value if not none else sets it from args or prompts.

        Returns
        -------
        list
            The keyword strings in a list

        """

        if str(self.keywords) == "unset": return []
        # if self.keywords: return self.keywords
        if len(self.keywords) > 0: return self.keywords
        # retrieve from args and return if exists
        keywords = Settings.get_keywords() or []
        if len(keywords) > 0: return keywords
        if not Settings.prompt("keywords"):
            self.keywords = "unset" # used to skip prompting for value in future
            return []
        question = {
            'type': 'input',
            'name': 'keywords',
            'message': 'Keywords:',
            'validate': ListValidator
        }
        keywords = prompt(question)["keywords"]
        keywords = [n.strip() for n in keywords.split(",")]
        # confirm keywords
        if not Settings.confirm(keywords): return self.get_keywords()
        self.keywords = keywords
        return self.keywords

    def get_performers(self):
        """
        Gets the performers value if not none else sets it from args or prompts.

        Returns
        -------
        list
            The performer usernames as strings in a list

        """

        if str(self.performers) == "unset": return []
        if len(self.performers) > 0: return self.performers
        # retrieve from args and return if exists
        performers = Settings.get_performers() or []
        # ensures all performers from files are included
        if len(self.files) > 0:
            for file in self.files:
                if hasattr(file, "performer"):
                    performer = getattr(file, "performer")
                    if performer not in performers:
                        performers.append(performer)
        if len(performers) > 0: 
            self.performers = performers
            return performers
        # prompt skip
        if not Settings.prompt("performers"):
            self.performers = "unset"
            return []
        question = {
            'type': 'input',
            'name': 'performers',
            'message': 'Performers:',
            'validate': ListValidator
        }
        performers = prompt(question)["performers"]
        performers = [n.strip() for n in performers.split(",")]
        # confirm performers
        if not Settings.confirm(performers): return self.get_performers()
        self.performers = performers
        return self.performers

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

        amount = 0
        if re.search(r'I sent you a \$[0-9]*\.00 tip ♥', text):
            amount = re.match(r'I sent you a \$([0-9]*)\.00 tip ♥', text).group(1)
            Settings.maybe_print("successfully found tip")
            Settings.dev_print("amount: {}".format(amount))
            return True, int(amount)
        elif re.search(r"I\'ve contributed \$[0-9]*\.00 to your Campaign", text):
            amount = re.match(r'I\'ve contributed \$([0-9]*)\.00 to your Campaign', text).group(1)
            Settings.maybe_print("successfully found campaign donation")
            Settings.dev_print("amount: {}".format(amount))
            return True, int(amount)
        return False, int(amount)

    def get_files(self):
        """
        Gets files from args specified source or prompts as necessary.

        Uses appropriate file select method as specified by runtime args:
        - remote
        - local

        Returns
        -------
        list
            Files in a list

        """

        # if str(self.files) == "unset": return []
        if isinstance(self.files, list) and len(self.files) > 0: return self.files[:int(Settings.get_upload_max())]
        if len(Settings.get_input_as_files()) > 0:
            self.files = Settings.get_input_as_files()
            return self.files
        # prompt skip
        if not Settings.is_prompt() and Settings.get_category() == None:
            self.files = "unset"
            return []
        files = []
        if len(self.files) == 0:
            files = File.select_file_upload_method()
            if str(files[0]) == "unset" or str(files) == "unset":
                self.files = "unset"
                files = []
                if Settings.is_prompt(): return []
        if files == None: files = []
        # get files from appropriate source's menu selection
        if Settings.get_source() == "remote":
            remoteFiles = Remote.get_files()
            if len(remoteFiles) > 0:
                files = Remote.select_files()
            elif len(files) == 0 and len(remoteFiles) == 0:
                self.files = "unset"
                return []
        elif Settings.get_source() == "local":
            localFiles = File.get_files()
            if len(files) == 0 and len(localFiles) > 0:
                files = File.select_files()
            elif len(files) == 0 and len(localFiles) == 0:
                self.files = "unset"
                return []
        filed = []
        for file in files:
            # turn all folders into their files
            if isinstance(file, Folder): filed.extend(file.get_files())
            else:
                # flag that the files include a performer
                if hasattr(file, "performer"):
                    self.performers.append(getattr("performer", file))
                filed.append(file)
        self.files = filed[:int(Settings.get_upload_max())]
        return self.files

    def get_expiration(self):
        """
        Gets the expiration value if not none else sets it from args or prompts.

        Returns
        -------
        int
            The expiration as an int

        """

        if str(self.expiration) == "unset": return None
        if self.expiration: return self.expiration
        # retrieve from args and return if exists
        expires = Settings.get_expiration() or None
        if expires: 
            self.expiration = expires
            return expires
        # prompt skip
        if not Settings.prompt("expiration"):
            self.expiration = "unset"
            return None
        question = {
            'type': 'input',
            'name': 'expiration',
            'message': 'Expiration [1, 3, 7, 99 (\'No Limit\')]',
            'validate': ExpirationValidator
        }
        expiration = prompt(question)["expiration"]
        # confirm expiration
        if not Settings.confirm(expiration): return self.get_expiration()
        self.expiration = expiration
        return self.expiration

    def get_poll(self):
        """
        Gets the poll value if not none else sets it from args or prompts.

        Returns
        -------
        Poll
            Poll object with proper values

        """

        if str(self.poll) == "unset": return None
        # check if poll is ready
        if self.poll and self.poll.check(): return self.poll
        # prompt skip
        if Settings.is_prompt() and not Settings.prompt("poll"):
            self.poll = "unset"
            return None
        poll = Poll()
        # ensure the poll has non default values
        poll.get()
        # check if valid poll
        if not poll.check(): return None
        self.poll = poll
        return poll

    def get_price(self):
        """
        Gets the price value if not none else sets it from args or prompts.

        Returns
        -------
        int
            The price as an int

        """

        if self.price: return self.price
        # retrieve from args and return if exists
        price = Settings.get_price() or None
        if price: 
            self.price = price
            return price
        if not Settings.prompt("price"): return ""
        question = {
            'type': 'input',
            'name': 'price',
            'message': 'Price',
            'validate': PriceValidator,
            'filter': lambda val: int(val)
        }
        price = prompt(question)["price"]
        if not Settings.confirm(price): return self.get_price()
        self.price = price
        return self.price

    def get_recipients(self):
        """
        Gets the recipients value if not none else sets it from args or prompts.

        Returns
        -------
        list
            Usernames in a list

        """

        if len(self.users) > 0: return self.users
        # if no recipients, prompt for them
        if len(self.users) == 0 and len(Settings.get_users()) > 0: 
            self.users = Settings.get_users()
        elif len(self.users) == 0 and Settings.get_user(): 
            self.users = [Settings.get_user()]
        # select users
        elif len(self.users) == 0:
            self.users = User.select_users()
        return self.users

    def get_schedule(self):
        """
        Gets the schedule value if not none else sets it from args or prompts.

        Returns
        -------
        Schedule
            Schedule object with proper values

        """

        if str(self.schedule) == "unset": return None
        if self.schedule: return self.schedule
        # prompt skip
        if Settings.is_prompt() and not Settings.prompt("schedule"):
            self.schedule = "unset"
            return None
        schedule = Schedule()
        schedule.get()
        # checks if schedule is valid
        if not schedule.check(): return None
        self.schedule = schedule
        return schedule
        
    def get_text(self):
        """
        Gets the text value if not none else sets it from args or prompts.

        Returns
        -------
        str
            The text to enter

        """

        if self.text: return self.text
        # retrieve from args and return if exists
        text = Settings.get_text() or None
        if text: 
            self.text = text
            return text
        # prompt skip
        if not Settings.prompt("text"): return None
        question = {
            'type': 'input',
            'name': 'text',
            'message': 'Text:'
        }
        text = prompt(question)["text"]
        # confirm text
        if not Settings.confirm(text): return self.get_text()
        self.text = text
        return self.text

    def get(self):
        """Gets all values"""

        if self.gotten: return
        self.get_text()
        self.get_keywords()
        self.get_price()
        self.get_poll()
        self.get_schedule()
        self.get_expiration()
        self.get_files()
        self.get_recipients()
        self.set_text()

        self.get_performers()

        self.gotten = True

    def get_post(self):
        """Gets values to populate as a post"""

        if self.gotten: return
        self.get_text()
        self.get_keywords()
        self.get_poll()
        self.get_schedule()
        self.get_expiration()
        self.get_files()
        self.set_text()

        self.get_performers()

        self.gotten = True

    def get_message(self):
        """Gets values to populate as a message"""

        if self.gotten: return
        self.get_recipients()
        self.get_text()
        self.get_price()
        self.get_files()
        self.set_text()

        self.get_performers()

        self.gotten = True

    def send_message(self):
        try:
            self.get_message()
            if Settings.is_prompt():
                if not Settings.prompt("Send"): return
            if self.get_files() != "unset" and len(self.get_files()) == 0 and not self.get_text():
                Settings.err_print("Missing Files and Text")
                return False
            successes = 0
            failures = 0
            try: 
                for user in self.users:
                    successful = False
                    if isinstance(user, User):
                        successful = User.message_user(username=user.username, message=self)
                    else:
                        successful = User.message_user(username=user, message=self)
                    if successful: successes+=1
                    else: failures+=1
            except Exception as e:
                Settings.dev_print(e)
                failures+=1
            if failures >= successes:
                Settings.print("Successful | Failed: {} | {}".format(successes, failures))
                return False
            self.cleanup_files()
            return True
        except Exception as e:
            Settings.dev_print(e)
        return False

    def send_post(self):
        try:
            self.get_post()
            if Settings.is_prompt():
                if not Settings.prompt("Post"): return False
            if self.get_files() != "unset" and len(self.get_files()) == 0 and not self.get_text():
                Settings.err_print("Missing Files and Text")
                return False
            successes = 0
            failures = 0
            try:
                successful = Driver.get_driver().post(message=self)
                if successful: successes+=1
                else: failures+=1
            except Exception as e:
                Settings.dev_print(e)
                failures+=1
            if failures >= successes:
                Settings.print("Successful | Failed: {} | {}".format(successes, failures))
                return False
            self.cleanup_files()
            return True
        except Exception as e:
            Settings.dev_print(e)
        return False

    def set_keywords(self):
        """Sets keywords from this object's file's title"""

        if len(self.get_keywords()) == 0 and len(self.get_files()) > 0:
            self.keywords = self.files[0].get_parent()["title"].split(" ")
            for keyword in self.keywords:
                if str(keyword) in str(self.text):
                    self.keywords = []
            
    def set_text(self):
        """Sets text from this object's file's title"""

        if not self.text and len(self.get_files()) > 0:
            self.text = self.files[0].get_title()
            # if "_" in str(self.text):
            if re.match("[0-9]_[0-9]", self.text) is not None:
                self.text = self.files[0].get_parent()["title"]
            else:
                try: 
                    int(self.text)
                    # is a simple int
                    if int(self.text) > 20:
                        self.text = self.files[0].get_parent()["title"]
                except Exception as e:
                    # not a simple int
                    # do nothing cause probably set already
                    pass
            self.text = self.text.replace("_", " ")
            self.set_keywords()
