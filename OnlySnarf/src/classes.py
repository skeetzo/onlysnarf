import re
from datetime import datetime
from .driver import Driver
from .settings import Settings
from .user import User
from PyInquirer import prompt
from PyInquirer import Validator, ValidationError
from .validators import AmountValidator, MonthValidator, LimitValidator, NumberValidator, TimeValidator, DateValidator, DurationValidator, PromoDurationValidator, ExpirationValidator, ListValidator
from . import remote as Remote
from .file import File, Folder, Google_File, Google_Folder

DEBUGGING_DATE = False

class Discount:

    def __init__(self):
        self.amount = None
        self.months = None
        self.username = None
        self.gotten = False

    def apply(self):
        self.get()
        if not self.gotten: return
        if Settings.is_prompt():
            if not Settings.prompt("Discount"): return
        Settings.maybe_print("discounting: {}".format(self.get_username().username))
        username = self.get_username().username
        if username.lower() == "all":
            users = User.get_all_users()
        elif username.lower() == "recent":
            users = User.get_recent_users()
        elif username.lower() == "favorite":
            users = User.get_favorite_users()
        elif username.lower() == "new":
            users = User.get_new_users()
        else: users = [self]
        successful = False
        for user in users:
            self.username = user.username
            successful_ = Driver.discount_user(discount=self)
            if successful_: successful = successful_
        return successful

    @staticmethod
    def create():
        discount = Discount()
        discount.apply()

    def get(self):
        if self.gotten: return
        gotten = self.get_username()
        # if not gotten: return
        gotten = self.get_amount()
        # if not gotten: return
        gotten = self.get_months()
        # if not gotten: return
        self.gotten = True

    def get_amount(self):
        if self.amount: return self.amount
        amount = Settings.get_amount() or None
        if amount: 
            self.amount = amount
            return amount
        if not Settings.prompt("amount"): return None
        question = {
            'type': 'input',
            'name': 'amount',
            'message': 'Amount:',
            'validate': AmountValidator,
            'filter': lambda val: int(myround(int(val)))
        }
        answers = prompt(question)
        amount = answers["amount"]
        if not Settings.confirm(amount): return self.get_amount()
        self.amount = amount
        return self.amount

    def get_months(self):
        if self.months: return self.months
        months = Settings.get_months() or None
        if months: 
            self.months = months
            return months
        if not Settings.prompt("months"): return None
        question = {
            'type': 'input',
            'name': 'months',
            'message': 'Months:',
            'validate': MonthValidator,
            'filter': lambda val: int(val)
        }
        answers = prompt(question)
        months = answers["months"]
        if not Settings.confirm(months): return self.get_months()
        self.months = months
        return self.months

    def get_username(self):
        if self.username: return self.username
        username = User.select_user()
        self.username = username
        return self.username

########################################################################################

class Message():
    def __init__(self):
        self.text = None
        self.files = []
        ##
        self.keywords = []
        self.tags = []
        self.performers = []
        self.hasPerformers = False
        ## messages
        self.price = None
        self.recipients = [] # users to send to
        self.users = [] # prepared recipients
        ## posts
        self.expiration = None
        self.poll = None
        self.schedule = None
        ##
        self.gotten = False

    def backup_files(self):
        for file in self.get_files():
            file.backup()

    def delete_files(self):
        for file in self.get_files():
            file.delete()

    def cleanup_files(self):
        self.backup_files()
        self.delete_files()

    @staticmethod
    def format_keywords(keywords):
        if len(keywords) > 0: return " #{}".format(" #".join(keywords))
        return ""

    @staticmethod
    def format_performers(performers): # spaced added after @ to close performer search modal
        if len(performers) > 0: return " w/ @{} ".format(" @".join(performers))
        return ""
            
    @staticmethod
    def format_tags(tags):
        if len(tags) > 0: return " @{}".format(" @".join(tags))
        return ""

    def format_text(self):
        return "{}{}{}{}".format(self.get_text(), Message.format_performers(self.get_performers()), Message.format_tags(self.get_tags()),
            Message.format_keywords(self.get_keywords())).strip()

    def get_keywords(self):
        if str(self.keywords) == "unset": return []
        # if self.keywords: return self.keywords
        if len(self.keywords) > 0: return self.keywords
        keywords = Settings.get_keywords() or []
        if len(keywords) > 0: return keywords
        if not Settings.prompt("keywords"):
            self.keywords = "unset"
            return []
        question = {
            'type': 'input',
            'name': 'keywords',
            'message': 'Keywords:',
            'validate': ListValidator
        }
        answers = prompt(question)
        keywords = answers["keywords"]
        keywords = keywords.split(",")
        keywords = [n.strip() for n in keywords]
        if not Settings.confirm(keywords): return self.get_keywords()
        self.keywords = keywords
        return self.keywords

    def get_performers(self):
        if str(self.performers) == "unset": return []
        # if self.performers: return self.performers
        if len(self.performers) > 0: return self.performers
        performers = Settings.get_performers() or []
        if len(performers) > 0: return performers

        if len(self.files) > 0:
            for file in self.files:
                if hasattr(file, "performer"):
                    p = getattr(file, "performer")
                    if p not in performers:
                        performers.append(p)
            if len(performers) > 0:
                self.performers = performers
                return performers

        if not Settings.prompt("performers"):
            self.performers = "unset"
            return []
        question = {
            'type': 'input',
            'name': 'performers',
            'message': 'Performers:',
            'validate': ListValidator
        }
        answers = prompt(question)
        performers = answers["performers"]
        performers = performers.split(",")
        performers = [n.strip() for n in performers]
        if not Settings.confirm(performers): return self.get_performers()
        self.performers = performers
        return self.performers

    def get_tags(self):
        if str(self.tags) == "unset": return []
        # if self.tags: return self.tags
        if len(self.tags) > 0: return self.tags
        tags = Settings.get_tags() or []
        if len(tags) > 0: return tags
        if not Settings.prompt("tags"):
            self.tags = "unset"
            return []
        question = {
            'type': 'input',
            'name': 'tags',
            'message': 'Tags:',
            'validate': ListValidator
        }
        answers = prompt(question)
        tags = answers["tags"]
        tags = tags.split(",")
        tags = [n.strip() for n in tags]
        if not Settings.confirm(tags): return self.get_tags()
        self.tags = tags
        return self.tags

    @staticmethod
    # gets tip text from a message
    def isTip(text):
        amount = 0
        if re.search(r'I sent you a $[0-9]*.00 tip ♥'):
            amount = re.match(r'I sent you a $([0-9]*).00 tip ♥')
            print("amount: {}".format(amount))
            return True, amount
        return False, amount
        # check text for "I sent you a $5.00 tip ♥"
        # pass

    # ensures File references exist and are downloaded
    # files are File references
    # file references can be GoogleId references which need to download their source
    # files exist when checked for size
    # ?
    def get_files(self):
        if str(self.files) == "unset": return []
        if len(self.files) > 0: return self.files[:int(Settings.get_upload_max())]
        if not Settings.is_prompt() and Settings.get_category() == None:
            self.files = "unset"
            return []
        files = []
        if len(self.files) == 0 and len(Settings.get_input()) > 0:
            files.append(Settings.get_input_as_files())
        elif len(self.files) == 0:
            files = File.select_file_upload_method()
            if str(files[0]) == "unset" or str(files) == "unset":
                self.files = "unset"
                files = []
                if Settings.is_prompt(): return []
        if files == None: files = []
        if Settings.get_source() == "google":
            googleFiles = Google_File.get_files()
            if len(files) == 0 and len(googleFiles) > 0:
                files = Google_File.select_files()
            elif len(files) == 0 and len(googleFiles) == 0:
                self.files = "unset"
                return []
        if Settings.get_source() == "dropbox":
            dropboxFiles = Dropbox.get_files()
            if len(files) == 0 and len(dropboxFiles) > 0:
                files = Dropbox.select_files()
            elif len(files) == 0 and len(dropboxFiles) == 0:
                self.files = "unset"
                return []
        if Settings.get_source() == "remote":
            remoteFiles = Remote.get_files()
            if len(remoteFiles) > 0:
                files = Remote.select_files()
            elif len(files) == 0 and len(remoteFiles) == 0:
                self.files = "unset"
                return []
        if Settings.get_source() == "local":
            localFiles = File.get_files()
            if len(files) == 0 and len(localFiles) > 0:
                files = File.select_files()
            elif len(files) == 0 and len(localFiles) == 0:
                self.files = "unset"
                return []
        filed = []
        for file in files:
            if isinstance(file, Folder) or isinstance(file, Google_Folder): filed.extend(file.get_files())
            else:
                if hasattr(file, "performer"):
                    self.hasPerformers = True
                filed.append(file)
        self.files = filed[:int(Settings.get_upload_max())]
        return self.files

    def get_expiration(self):
        if str(self.expiration) == "unset": return None
        if self.expiration: return self.expiration
        expires = Settings.get_expiration() or None
        if expires: 
            self.expiration = expires
            return expires
        if not Settings.prompt("expiration"):
            self.expiration = "unset"
            return None
        question = {
            'type': 'input',
            'name': 'expiration',
            'message': 'Expiration [1, 3, 7, 99 (\'No Limit\')]',
            'validate': ExpirationValidator
        }
        answers = prompt(question)
        expiration = answers["expiration"]
        if not Settings.confirm(expiration): return self.get_expiration()
        self.expiration = expiration
        return self.expiration

    def get_poll(self):
        if str(self.poll) == "unset": return None
        if self.poll and self.poll.check(): return self.poll
        if Settings.is_prompt() and not Settings.prompt("poll"):
            self.poll = "unset"
            return None
        poll = Poll()
        poll.get()
        if not poll.check(): return None
        self.poll = poll
        return poll

    def get_price(self):
        if self.price: return self.price
        price = Settings.get_price() or None
        if price: 
            self.price = price
            return price
        if not Settings.prompt("price"): return ""
        question = {
            'type': 'input',
            'name': 'price',
            'message': 'Price',
            'validate': NumberValidator,
            'filter': lambda val: int(val)
        }
        answers = prompt(question)
        price = answers["price"]
        if not Settings.confirm(price): return self.get_price()
        self.price = price
        return self.price

    # ensures listed recipients are users
    # Settings.USERS and self.recipients should be usernames
    # if includes [all, recent, favorite] & usernames it only uses the 1st found of [all,...]
    def get_recipients(self):
        if len(self.users) > 0: return self.users
        users = []
        if len(self.recipients) == 0 and len(Settings.get_users()) > 0: 
            users = Settings.get_users()
        elif len(self.recipients) == 0 and Settings.get_user(): 
            users = [Settings.get_user()]
        elif len(self.recipients) == 0:
            users = User.select_users()
        # users = []
        # for user in recipients:
        #     if str(user.username).lower() == "all":
        #         users = User.get_all_users()
        #         break
        #     elif str(user.username).lower() == "recent":
        #         users = User.get_recent_users()
        #         break
        #     elif str(user.username).lower() == "favorite":
        #         users = User.get_favorite_users()
        #         break
        #     else: users.append(user)
        self.users = users
        return self.users

    def get_schedule(self):
        if str(self.schedule) == "unset": return None
        if self.schedule: return self.schedule
        if Settings.is_prompt() and not Settings.prompt("schedule"):
            self.schedule = "unset"
            return None
        schedule = Schedule()
        schedule.get()
        if not schedule.check(): return None
        self.schedule = schedule
        return schedule
        
    def get_text(self):
        if self.text: return self.text
        text = Settings.get_text() or None
        if text: 
            self.text = text
            return text
        if not Settings.prompt("text"): return None
        question = {
            'type': 'input',
            'name': 'text',
            'message': 'Text:'
        }
        answers = prompt(question)
        text = answers["text"]
        if not Settings.confirm(text): return self.get_text()
        self.text = text
        return self.text

    def get(self):
        if self.gotten: return
        self.get_text()
        self.get_keywords()
        self.get_tags()
        self.get_price()
        self.get_poll()
        self.get_schedule()
        self.get_expiration()
        self.get_files()
        self.get_recipients()
        if not self.text and str(self.files) != "unset":
            if len(self.files) > 0:
                self.text = self.files[0].get_title()
        if Settings.get_performer_category() or self.hasPerformers:
            self.get_performers()
        else: # might as well skip asking if not pulling from performer category
            self.performers = "unset"
        self.gotten = True

    def get_post(self):
        if self.gotten: return
        self.get_text()
        self.get_keywords()
        self.get_tags()
        self.get_poll()
        self.get_schedule()
        self.get_expiration()
        self.get_files()
        if not self.text and str(self.files) != "unset":
            if len(self.files) > 0:
                self.text = self.files[0].get_title()
        if Settings.get_performer_category() or self.hasPerformers:
            self.get_performers()
        else:
            self.performers = "unset"
        self.gotten = True

    def get_message(self):
        if self.gotten: return
        self.get_recipients()
        self.get_text()
        self.get_price()
        self.get_files()
        if not self.text and str(self.files) != "unset":
            if len(self.files) > 0:
                self.text = self.files[0].get_title()
        if Settings.get_performer_category() or self.hasPerformers:
            self.get_performers()
        else:
            self.performers = "unset"
        self.gotten = True

    @staticmethod
    def is_tip(message):
        return False
        # pass
        # check if message is tip
        # returns false
        # or returns true and tip amount

########################################################################################

class Poll:

    def __init__(self):
        self.duration = None
        self.questions = []
        self.gotten = False

    def apply(self):
        self.get()
        if not self.gotten: return
        if not Settings.prompt("Poll"): return
        return True

    def check(self):
        if len(self.get_questions()) > 0: return True
        if self.get_duration(): return True
        return False

    def get(self):
        if self.gotten: return
        gotten = self.get_duration()
        if not gotten: return
        gotten = self.get_questions()
        if not gotten: return
        self.gotten = True

    def get_duration(self): # months
        if self.duration: return self.duration
        duration = Settings.get_duration()
        if duration: 
            self.duration = duration
            return duration
        if not Settings.prompt("duration"): return None
        question = {
            'type': 'input',
            'name': 'duration',
            'message': 'Duration [1, 3, 7, 99 (\'No Limit\')]',
            'validate': DurationValidator
        }
        answers = prompt(question)
        duration = answers["duration"]
        if not Settings.confirm(duration): return self.get_duration()
        self.duration = duration
        return self.duration

    def get_questions(self):
        if len(self.questions) > 0: return self.questions
        questions = Settings.get_questions()
        if len(questions) > 0: 
            self.questions = questions
            return questions
        if not Settings.prompt("questions"): return []
        print("Enter Questions")
        while True:
            question = {
                'type': 'input',
                'name': 'question',
                'message': 'Question:',
            }
            answers = prompt(question)
            question = answers["question"]
            if str(question) == "": break
            questions.append(question)
        if not Settings.confirm(questions): return self.get_questions()
        self.questions = questions
        return self.questions

########################################################################################

class Promotion:

    def __init__(self):
        self.amount = None
        self.limit = None
        self.expiration = None
        self.duration = None
        self.user = None
        self.message = None
        self.gotten = False

    # apply discount directly to user on user's profile page
    def apply_to_user(self):
        print("Promotion - Apply To User: {}".format(self.user.username))
        self.get()
        if Settings.is_prompt():
            if not Settings.prompt("Promotion"): return
        # user, expiration, months, message
        Driver.promotion_user_directly(promotion=self)

    def create_campaign(self):
        print("Promotion - Creating Campaign")
        self.get()
        if Settings.is_prompt():
            if not Settings.prompt("Promotion"): return
        Driver.promotional_campaign(promotion=self)

    # requires the copy/paste and email steps
    def create_trial_link(self):
        print("Promotion - Creating Trial Link")
        self.get()
        # if not self.gotten: return
        if Settings.is_prompt():
            if not Settings.prompt("Promotion"): return
        # limit, expiration, months, user
        Driver.promotional_trial_link(promotion=self)
        # link = Driver.promotional_trial_link()
        # text = "Here's your free trial link!\n"+link
        # Settings.dev_print("Link: "+str(text))
        # Settings.send_email(email, text)

    def get(self):
        if self.gotten: return
        gotten = self.get_user()
        gotten = self.get_amount()
        gotten = self.get_expiration()
        gotten = self.get_limit()
        gotten = self.get_duration()
        gotten = self.get_message()
        self.gotten = True

    def get_amount(self):
        if self.amount: return self.amount
        amount = Settings.get_amount() or None
        if amount: 
            self.amount = amount
            return amount
        if not Settings.prompt("amount"): return None
        question = {
            'type': 'input',
            'name': 'amount',
            'message': 'Amount:',
            'validate': AmountValidator,
            'filter': lambda val: int(myround(int(val)))
        }
        answers = prompt(question)
        amount = answers["amount"]
        if not Settings.confirm(amount): return self.get_amount()
        self.amount = amount
        return self.amount

    def get_expiration(self):
        if self.expiration: return self.expiration
        expiration = Settings.get_expiration() or None
        if expiration: 
            self.expiration = expiration
            return expiration
        if not Settings.prompt("expiration"): return None
        question = {
            'type': 'input',
            'name': 'expiration',
            'message': 'Expiration [1, 3, 7, 99 (\'No Limit\')]',
            'validate': ExpirationValidator
        }
        answers = prompt(question)
        expiration = answers["expiration"]
        if not Settings.confirm(expiration): return self.get_expiration()
        self.expiration = expiration
        return self.expiration

    def get_limit(self):
        if self.limit: return self.limit
        limit = Settings.get_limit() or None
        if limit: 
            self.limit = limit
            return limit
        if not Settings.prompt("limit"): return None
        question = {
            'type': 'input',
            'name': 'limit',
            'message': 'Limit (in days or months)',
            'validate': LimitValidator
        }
        answers = prompt(question)
        limit = answers["limit"]
        if not Settings.confirm(limit): return self.get_limit()
        self.limit = limit
        return self.limit

    def get_message(self):
        if self.message != None: return self.message
        message = Settings.get_text() or None
        if message: 
            self.message = message
            return message
        if not Settings.prompt("message"): return ""
        question = {
            'type': 'input',
            'name': 'message',
            'message': 'Message:'
        }
        answers = prompt(question)
        message = answers["message"]
        if not Settings.confirm(message): return self.get_text()
        self.message = message
        return self.message

    def get_duration(self): # months
        if self.duration: return self.duration
        duration = Settings.get_promo_duration() or None
        if duration: 
            self.duration = duration
            return duration
        if not Settings.prompt("duration"): return None
        question = {
            'type': 'input',
            'name': 'duration',
            'message': 'Duration [1 day, 3 days, 7 days, ...]',
            'validate': PromoDurationValidator
        }
        answers = prompt(question)
        duration = answers["duration"]
        if not Settings.confirm(duration): return self.get_duration()
        self.duration = duration
        return self.duration

    def get_user(self):
        if self.user: return self.user
        user = User.select_user()
        self.user = user
        return self.user

    @staticmethod
    def menu():
        if not Settings.is_debug():
            print("### Not Available ###")
            return
        action = Promotion.ask_action()
        if (action == 'Back'): pass
        elif (action == 'apply to user'): promotion.create_trial_link()
        elif (action == 'create trial link'): promotion.apply_to_user()

    @staticmethod
    def ask_action():
        options = ["back", "apply to user", "create trial link"]
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
        if self.date: return self.date
        date = Settings.get_date() or None
        if date: 
            self.date = date
            return date
        schedule = Settings.get_schedule() or None

        # if not Settings.is_prompt():
        #     self.date = None
        #     return None

        if schedule:
            date = datetime.strptime(str(schedule), "%Y-%m-%d %H:%M:%S")
            self.date = date.date()
            return self.date
        if not Settings.prompt("date"): return None
        question = {
            'type': 'input',
            'name': 'date',
            'message': 'Enter a date (MM-DD-YYYY):',
            'validate': DateValidator
        }
        answers = prompt(question)
        date = answers["date"]
        if not Settings.confirm(date): return self.get_date()
        self.date = date
        return self.date

    def get_time(self):
        if self.time: return self.time
        time = Settings.get_time() or None
        if time: 
            time = datetime.strptime(str(time), "%Y-%m-%d %H:%M:%S")
            maybe_print('a')
            maybe_print(time)
            time = time.strftime("%I:%M %p")
            maybe_print('b')
            maybe_print(time)
            self.time = time
            maybe_print('c')
            return self.time
            # return time
        schedule = Settings.get_schedule() or None

        # if not Settings.is_prompt():
        #     self.time = None
        #     return None

        if schedule:
            time = datetime.strptime(str(schedule), "%Y-%m-%d %H:%M:%S")
            maybe_print('e')
            maybe_print(time)
            time = time.strftime("%I:%M %p")
            maybe_print('f')
            maybe_print(time)
            self.time = time
            maybe_print('g')
            return self.time
        if not Settings.prompt("time"): return None
        question = {
            'type': 'input',
            'name': 'time',
            'message': 'Enter a time (HH:MM):',
            'validate': TimeValidator
        }
        answers = prompt(question)
        time = answers["time"]
        if not Settings.confirm(time): return self.get_time()
        self.time = time
        return self.time

# round to 5
def myround(x, base=5):
    return base * round(x/base)

def maybe_print(s):
    global DEBUGGING_DATE
    if DEBUGGING_DATE: print(s)