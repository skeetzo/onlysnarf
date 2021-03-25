import re
from datetime import datetime
from .driver import Driver
from .settings import Settings
from .user import User
from PyInquirer import prompt
from PyInquirer import Validator, ValidationError
##
from .validators import AmountValidator, MonthValidator, LimitValidator, PriceValidator, NumberValidator, TimeValidator, DateValidator, DurationValidator, PromoDurationValidator, ExpirationValidator, ListValidator
from . import remote as Remote
from .file import File, Folder, Google_File, Google_Folder

class Discount:
    """OnlyFans discount class"""

    def __init__(self):
        """OnlyFans discount object"""

        # amount in percent
        self.amount = None
        # number of months (1-12)
        self.months = None
        # the recipient username
        self.username = None
        # prevents double prompts
        self.gotten = False

    def apply(self):
        """
        Applies the discounted amount to the recipient username via Driver.discount_user

        If the targeted username is one of the matching keywords then all of the 
        matching recipients will be discounted. Values are determined by runtime args or prompted
        for.

        """

        # ensure the discount has non default values
        self.get()
        if not self.gotten:
            Settings.err_print("Unable to apply discount")
            return
        # skip prompt if disabled
        if Settings.is_prompt():
            if not Settings.prompt("Discount"): return
        Settings.maybe_print("discounting: {}".format(self.username))
        # create new or find default browser
        driver = Driver.get_driver()
        if self.username.lower() == "all":
            users = User.get_all_users(driver=driver)
        elif self.username.lower() == "recent":
            users = User.get_recent_users(driver=driver)
        elif self.username.lower() == "favorite":
            users = User.get_favorite_users(driver=driver)
        elif self.username.lower() == "new":
            users = User.get_new_users(driver=driver)
        else: users = [self]
        for user in users:
            self.username = user.username
            driver.discount_user(discount=self)

    @staticmethod
    def create():
        """Create and apply a discount from args or prompts"""

        discount = Discount()
        discount.apply()

    def get(self):
        """Update the discount object's default values"""

        if self.gotten: return
        gotten = self.get_username()
        gotten = self.get_amount()
        gotten = self.get_months()
        self.gotten = True

    def get_amount(self):
        """
        Populate and get the amount value

        If not found in args and prompt is enabled, ask for value.

        Returns
        -------
        int
            the discounted amount to apply

        """

        if self.amount: return self.amount
        # retrieve from args and return if exists
        amount = Settings.get_amount() or None
        if amount: 
            self.amount = amount
            return amount
        # prompt skip
        if not Settings.prompt("amount"): return None
        question = {
            'type': 'input',
            'name': 'amount',
            'message': 'Amount:',
            'validate': AmountValidator,
            'filter': lambda val: int(myround(int(val)))
        }
        amount = prompt(question)["amount"]
        if not Settings.confirm(amount): return self.get_amount()
        self.amount = amount
        return self.amount

    def get_months(self):
        """
        Populate and get the months value

        If not found in args and prompt is enabled, ask for value.

        Returns
        -------
        int
            the number of months to discount for

        """

        if self.months: return self.months
        # retrieve from args and return if exists
        months = Settings.get_months() or None
        if months: 
            self.months = months
            return months
        # prompt skip
        if not Settings.prompt("months"): return None
        question = {
            'type': 'input',
            'name': 'months',
            'message': 'Months:',
            'validate': MonthValidator,
            'filter': lambda val: int(val)
        }
        months = prompt(question)["months"]
        if not Settings.confirm(months): return self.get_months()
        self.months = months
        return self.months

    def get_username(self):
        """
        Populate and get the username value

        If not found in args and prompt is enabled, ask for value.

        Returns
        -------
        str
            the username to discount

        """

        if self.username: return self.username
        self.username = User.select_user()
        return self.username

    def grandfatherer(self, users=[]):
        """
        Executes the 'Grandfather' discount model

        If users is empty it is populated with users from the 'Grandfather' OnlyFans list in 
        the account. All 'Grandfather'ed users are provided with the max discount for the max months.

        Parameters
        ----------
        users : list
            list of users to 'Grandfather'

        """

        from .driver import Driver
        if len(users) == 0:
            users = User.get_users_by_list(name="grandfathered", driver=Driver.get_driver())
        print("Discount - Grandfathering: {} users".format(len(users)))
        from .validators import DISCOUNT_MAX_MONTHS, DISCOUNT_MAX_AMOUNT
        self.months = DISCOUNT_MAX_MONTHS
        self.amount = DISCOUNT_MAX_AMOUNT
        # apply discount to all users
        for user in users:
            self.username = user.username
            print("Grandfathering: {}".format(self.username))
            try:
                Driver.get_driver().discount_user(discount=self)
            except Exception as e:
                print(e)

########################################################################################

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
        - google
        - remote
        - local

        Returns
        -------
        list
            Files in a list

        """

        if str(self.files) == "unset": return []
        if len(self.files) > 0: return self.files[:int(Settings.get_upload_max())]
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
        if Settings.get_source() == "google":
            googleFiles = Google_File.get_files()
            if len(files) == 0 and len(googleFiles) > 0:
                files = Google_File.select_files()
            elif len(files) == 0 and len(googleFiles) == 0:
                self.files = "unset"
                return []
        elif Settings.get_source() == "remote":
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
            if isinstance(file, Folder) or isinstance(file, Google_Folder): filed.extend(file.get_files())
            else:
                # flag that the files include a performer
                if hasattr(file, "performer"):
                    self.hasPerformers = True
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
        if len(self.recipients) == 0 and len(Settings.get_users()) > 0: 
            self.users = Settings.get_users()
        elif len(self.recipients) == 0 and Settings.get_user(): 
            self.users = [Settings.get_user()]
        # select users
        elif len(self.recipients) == 0:
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
        if Settings.get_performer_category() or self.hasPerformers:
            self.get_performers()
        else: # might as well skip asking if not pulling from performer category
            self.performers = "unset"
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
        if Settings.get_performer_category() or self.hasPerformers:
            self.get_performers()
        else:
            self.performers = "unset"
        self.gotten = True

    def get_message(self):
        """Gets values to populate as a message"""

        if self.gotten: return
        self.get_recipients()
        self.get_text()
        self.get_price()
        self.get_files()
        self.set_text()
        if Settings.get_performer_category() or self.hasPerformers:
            self.get_performers()
        else:
            self.performers = "unset"
        self.gotten = True

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

########################################################################################
########################################################################################
########################################################################################

class Poll:
    """OnlyFans Poll class"""

    def __init__(self):
        """OnlyFans Poll object"""

        # duration of poll
        self.duration = None
        # list of strings
        self.questions = []
        # prevents double prompts
        self.gotten = False

    def check(self):
        """Check if poll is ready with valid values

        Returns
        -------
        bool
            Whether the poll is ready to be posted or not

        """

        if len(self.get_questions()) > 0: return True
        if self.get_duration(): return True
        return False

    def get(self):
        if self.gotten: return
        gotten = self.get_duration()
        # return early if skipped
        if not gotten: return
        gotten = self.get_questions()
        # return early if skipped
        if not gotten: return
        self.gotten = True

    def get_duration(self):
        """
        Gets the duration value if not none else sets it from args or prompts.

        Returns
        -------
        int
            The duration as an int

        """

        if self.duration: return self.duration
        # retrieve from args and return if exists
        duration = Settings.get_duration()
        if duration: 
            self.duration = duration
            return duration
        # prompt skip
        if not Settings.prompt("duration"): return None
        question = {
            'type': 'input',
            'name': 'duration',
            'message': 'Duration [1, 3, 7, 99 (\'No Limit\')]',
            'validate': DurationValidator
        }
        duration = prompt(question)["duration"]
        # confirm duration
        if not Settings.confirm(duration): return self.get_duration()
        self.duration = duration
        return self.duration

    def get_questions(self):
        """
        Gets the questions value if not none else sets it from args or prompts.

        Returns
        -------
        list
            The questions as strings in a list

        """

        if len(self.questions) > 0: return self.questions
        # retrieve from args and return if exists
        questions = Settings.get_questions()
        if len(questions) > 0: 
            self.questions = questions
            return questions
        # prompt skip
        if not Settings.prompt("questions"): return []
        print("Enter Questions")
        while True:
            question = {
                'type': 'input',
                'name': 'question',
                'message': 'Question:',
            }
            answers = prompt(question)["question"]
            if str(question) == "": break
            questions.append(question)
        # confirm questions
        if not Settings.confirm(questions): return self.get_questions()
        self.questions = questions
        return self.questions

########################################################################################
########################################################################################
########################################################################################

class Promotion:
    """Promotion class"""

    def __init__(self):
        """Promotion object"""

        # the amount to discount
        self.amount = None
        # the number of trials to allow
        self.limit = None
        # the expiration of the trial
        self.expiration = None
        # the duration of the discount
        self.duration = None
        # the user to apply the promotion to
        self.user = None
        # the message to provide with the promotion
        self.message = None
        # prevents double prompts
        self.gotten = False

    @staticmethod
    def apply_to_user():
        """Applies promotion directly to user via their profile page
        
           Applying a discount to a user requires:
           - amount
           - duration
           - expiration
           - message
           - user

        """

        print("Promotion - Apply To User")
        p = Promotion()
        # ensure the promotion has non default values, return early if missing
        # p.get()
        gotten = p.get_amount()
        if not gotten: return
        gotten = p.get_duration()
        if not gotten: return
        gotten = p.get_expiration()
        if not gotten: return
        gotten = p.get_message()
        if not gotten: return
        gotten = p.get_user()
        if not gotten: return
        # prompt skip
        if Settings.is_prompt():
            if not Settings.prompt("Promotion"): return
        from .driver import Driver
        # get default driver and apply the promotion directly
        Driver.get_driver().promotion_user_directly(promotion=p)

    @staticmethod
    def create_campaign():
        """Creates a Promotional Campaign

           A campaign consists of:
           - amount
           - duration
           - expiration
           - limit
           - user
           - text

        """

        print("Promotion - Creating Campaign")
        p = Promotion()
        # ensure the promotion has non default values, return early if missing
        # p.get()
        gotten = p.get_amount()
        if not gotten: return
        gotten = p.get_user()
        if not gotten: return
        gotten = p.get_expiration()
        if not gotten: return
        gotten = p.get_limit()
        if not gotten: return
        gotten = p.get_duration()
        if not gotten: return
        gotten = p.get_message()
        if not gotten: return
        # prompt skip
        if Settings.is_prompt():
            if not Settings.prompt("Promotion"): return
        from .driver import Driver
        # get the default driver and enter the promotion campaign
        Driver.get_driver().promotional_campaign(promotion=p)

    # requires the copy/paste and email steps
    @staticmethod
    def create_trial_link():
        """Creates a Promotional Trial Link

           A trial link consists of:
           - duration
           - expiration
           - limit
           - message
           - user
            
           Note: this creates a free trial link but does NOT send it to the user
           because it is incomplete. The copy/paste step to message to a user is nonfunctioning.           

        """

        print("Promotion - Creating Trial Link")
        p = Promotion()
        # ensure the promotion has non default values, return early if missing
        # p.get()
        gotten = p.get_duration()
        if not gotten: return
        gotten = p.get_expiration()
        if not gotten: return
        gotten = p.get_limit()
        if not gotten: return
        gotten = p.get_message()
        if not gotten: return
        gotten = p.get_user()
        if not gotten: return
        # if not self.gotten: return
        if Settings.is_prompt():
            if not Settings.prompt("Promotion"): return
        # limit, expiration, months, user
        from .driver import Driver
        link = Driver.get_driver().promotional_trial_link(promotion=p)
        # text = "Here's your free trial link!\n"+link
        # Settings.dev_print("Link: "+str(text))
        # Settings.send_email(email, text)

    def get(self):
        """Update the promotion object's default values"""

        if self.gotten: return
        gotten = self.get_user()
        gotten = self.get_amount()
        gotten = self.get_expiration()
        gotten = self.get_limit()
        gotten = self.get_duration()
        gotten = self.get_message()
        self.gotten = True

    def get_amount(self):
        """
        Gets the amount value if not none else sets it from args or prompts.

        Returns
        -------
        int
            The amount as an int

        """

        if self.amount: return self.amount
        # retrieve from args and return if exists
        amount = Settings.get_amount() or None
        if amount: 
            self.amount = amount
            return amount
        # prompt skip
        if not Settings.prompt("amount"): return None
        question = {
            'type': 'input',
            'name': 'amount',
            'message': 'Amount:',
            'validate': AmountValidator,
            'filter': lambda val: int(myround(int(val)))
        }
        amount = prompt(question)["amount"]
        # confirm amount
        if not Settings.confirm(amount): return self.get_amount()
        self.amount = amount
        return self.amount

    def get_expiration(self):
        """
        Gets the expiration value if not none else sets it from args or prompts.

        Returns
        -------
        int
            The expiration as an int

        """

        if self.expiration: return self.expiration
        # retrieve from args and return if exists
        expiration = Settings.get_expiration() or None
        if expiration: 
            self.expiration = expiration
            return expiration
        # prompt skip
        if not Settings.prompt("expiration"): return None
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

    def get_limit(self):
        """
        Gets the expiration value if not none else sets it from args or prompts.

        Returns
        -------
        int
            The expiration as an int

        """

        if self.limit: return self.limit
        # retrieve from args and return if exists
        limit = Settings.get_limit() or None
        if limit: 
            self.limit = limit
            return limit
        # prompt skip
        if not Settings.prompt("limit"): return None
        question = {
            'type': 'input',
            'name': 'limit',
            'message': 'Limit (in days or months)',
            'validate': LimitValidator
        }
        limit = prompt(question)["limit"]
        # confirm limit
        if not Settings.confirm(limit): return self.get_limit()
        self.limit = limit
        return self.limit

    def get_message(self):
        """
        Gets the message value if not none else sets it from args or prompts.

        Returns
        -------
        str
            The message as a str

        """

        if self.message != None: return self.message
        # retrieve from args and return if exists
        message = Settings.get_text() or None
        if message: 
            self.message = message
            return message
        # prompt skip
        if not Settings.prompt("message"): return ""
        question = {
            'type': 'input',
            'name': 'message',
            'message': 'Message:'
        }
        message = prompt(question)["message"]
        # confirm message
        if not Settings.confirm(message): return self.get_text()
        self.message = message
        return self.message

    def get_duration(self):
        """
        Gets the duration value if not none else sets it from args or prompts.

        Returns
        -------
        int
            The duration as an int

        """

        if self.duration: return self.duration
        # retrieve from args and return if exists
        duration = Settings.get_promo_duration() or None
        if duration: 
            self.duration = duration
            return duration
        # duration skip
        if not Settings.prompt("duration"): return None
        question = {
            'type': 'input',
            'name': 'duration',
            'message': 'Duration [1 day, 3 days, 7 days, ...]',
            'validate': PromoDurationValidator
        }
        duration = prompt(question)["duration"]
        # confirm duration
        if not Settings.confirm(duration): return self.get_duration()
        self.duration = duration
        return self.duration

    def get_user(self):
        """
        Populate and get the username value

        If not found in args and prompt is enabled, ask for value.

        Returns
        -------
        User
            the user to apply the promotion to

        """

        if self.user: return self.user
        user = User.select_user()
        self.user = user.username
        return self.user

    @staticmethod
    def grandfathered():
        """
        Executes the 'Grandfather' promotion model

        In groups of 5, existing users will be added to the 'Grandfathered' OnlyFans list and
        then provided with the max discount for the max months. If the process interrupts, 
        running again will continue to discount users not yet added to the list.

        """

        print("Promotion - Grandfather")
        # prompt skip
        if Settings.is_prompt():
            if not Settings.prompt("Grandfather"): return
        Settings.maybe_print("getting users to grandfather")
        # get all users
        users = User.get_all_users()
        from .driver import Driver
        # get all users from logged in user's 'grandfathered' list
        users_, name, number = Driver.get_driver().get_list(name="grandfathered")
        # remove all users that have already been grandfathered from the list of all users
        # users = [user for user in users if user not in users_] # i guess doesn't work?
        for i, user in enumerate(users[:]):
            for user_ in users_:
                for key, value in user_.items():
                    if str(key) == "username" and str(user.username) == str(value):
                        users.remove(user)

        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

        # get users in groups of 5 to allow performance over interrupts
        userChunks = chunks(users, 5)
        num = 1
        for userChunk in userChunks:
            print("Chunk: {}/{}".format(num, len(users)/5))
            num += 1
            # add users to 'grandfathered' list prior to discounting
            Settings.maybe_print("grandfathering: {}".format(len(userChunk)))
            try:
                successful = Driver.get_driver().add_users_to_list(users=userChunk, number=number, name="grandfathered")
                # if successful then discount
                if not successful: return
                d = Discount() # discount will fill defaults with promotion values
                d.grandfatherer(users=userChunk)
            except Exception as e:
                Settings.dev_print(e)

    @staticmethod
    def menu():
        """Promotion menu interface"""

        if not Settings.is_debug():
            print("### Not Available ###")
            return
        action = Promotion.ask_action()
        if (action == 'Back'): pass
        elif (action == 'trial'): Promotion.create_trial_link()
        elif (action == 'campaign'): Promotion.create_campaign()
        elif (action == 'user'): Promotion.apply_to_user()
        elif (action == 'grandfather'): Promotion.grandfathered()

    @staticmethod
    def ask_action():
        """Promotion menu selection

        Returns
        -------
        str
            The menu action to take

        """

        # arg - promotion_method: campaign, trial, user, grandfather
        options = ["back", 
            "campaign", # 
            "grandfather" # this mostly completely works
            "trial", # this isn't even finished but it does mostly work
            "user", # should this be here?
        ]
        menu_prompt = {
            'type': 'list',
            'name': 'action',
            'message': 'Please select a promotion action:',
            'choices': [str(option).title() for option in options],
            'filter': lambda val: str(val).lower()
        }
        answers = prompt(menu_prompt)
        return answers['action']

########################################################################################
########################################################################################
########################################################################################

class Schedule:

    def __init__(self):
        self.date = None
        self.time = None
        ##
        self.hour = "00"
        self.minute = "00"
        self.year = "0"
        self.month = "0"
        self.day = "0"
        self.suffix = "am"
        ##
        self.gotten = False

    def apply(self):
        self.get()
        if not self.gotten: return
        if not Settings.prompt("Schedule"): return

    def check(self):
        if self.get_date() and self.get_time(): return True
        return False

    def get(self):
        if self.gotten: return
        if self.get_date():
            date = self.get_date()
            maybe_print(0)
            maybe_print(date)
            if self.get_time():
                maybe_print(11)
                maybe_print(self.get_time())
                if "00:00:00" in str(date):
                    date = str(date).replace("00:00:00", self.get_time())
                else:
                    date = "{} {}".format(date, self.get_time())
            if "am" in self.get_time().lower(): self.suffix = "am"
            elif "pm" in self.get_time().lower(): self.suffix = "pm"
            maybe_print(1)
            maybe_print(date)
            date = datetime.strptime(str(date), "%Y-%m-%d %H:%M %p")
            maybe_print(2)
            maybe_print(date)
            self.year = date.year
            self.month = date.strftime("%B")
            self.day = date.day
            self.hour = date.hour
            self.minute = date.minute
            maybe_print("year: {}".format(self.year))
            maybe_print("month: {}".format(self.month))
            maybe_print("day: {}".format(self.day))
            maybe_print("hour: {}".format(self.hour))
            maybe_print("minutes: {}".format(self.minute))
        self.gotten = True

    def get_date(self):
        """
        Gets the date value if not none else sets it from args or prompts.

        Returns
        -------
        str
            The date as a valid date string

        """

        if self.date: return self.date
        date = Settings.get_date() or None
        if date: 
            self.date = date
            return date
        # retrieve from args and return if exists
        schedule = Settings.get_schedule() or None
        if schedule:
            date = datetime.strptime(str(schedule), "%Y-%m-%d %H:%M:%S")
            self.date = date.date()
            return self.date
        # prompt skip
        if not Settings.prompt("date"): return None
        question = {
            'type': 'input',
            'name': 'date',
            'message': 'Enter a date (MM-DD-YYYY):',
            'validate': DateValidator
        }
        date = prompt(question)["date"]
        # confirm date
        if not Settings.confirm(date): return self.get_date()
        self.date = date
        return self.date

    def get_time(self):
        """
        Gets the time value if not none else sets it from args or prompts.

        Returns
        -------
        str
            The time as a valid time string

        """

        if self.time: return self.time
        # retrieve from args and return if exists
        time = Settings.get_time() or None
        if time: 
            time = datetime.strptime(str(time), "%Y-%m-%d %H:%M:%S")
            # Settings.dev_print(time)
            time = time.strftime("%I:%M %p")
            # Settings.dev_print(time)
            self.time = time
            return self.time
        # retrieve time from schedule args and return if exists
        schedule = Settings.get_schedule() or None
        if schedule:
            time = datetime.strptime(str(schedule), "%Y-%m-%d %H:%M:%S")
            # Settings.dev_print(time)
            time = time.strftime("%I:%M %p")
            # Settings.dev_print(time)
            self.time = time
            return self.time
        # prompt skip
        if not Settings.prompt("time"): return None
        question = {
            'type': 'input',
            'name': 'time',
            'message': 'Enter a time (HH:MM):',
            'validate': TimeValidator
        }
        time = prompt(question)["time"]
        # confirm time
        if not Settings.confirm(time): return self.get_time()
        self.time = time
        return self.time

# round to 5
def myround(x, base=5):
    return base * round(x/base)