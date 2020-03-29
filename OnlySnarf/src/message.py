from datetime import datetime
from .driver import Driver
from .file import File, Google_File
from .settings import Settings
from .user import User
from .validators import NumberValidator, TimeValidator, DateValidator, DurationValidator, ExpirationValidator, ListValidator
import PyInquirer
from PyInquirer import Validator, ValidationError

class Message():
    def __init__(self):
        self.text = ""
        self.files = []
        ##
        self.keywords = []
        self.tags = []
        self.performers = []
        ## messages
        self.price = None
        self.recipients = [] # users to send to
        ## posts
        self.expiration = None
        self.poll = None
        self.schedule = None

    ###########################################################################

    def backup_files(self):
        for file in self.files:
            file.backup()

    @staticmethod
    def format_keywords(keywords):
        if len(keywords) > 0: return "#{}".format(" #".join(self.get_performers()))

    @staticmethod
    def format_performers(performers):
        if len(performers) > 0: return "w/ @{}".format(" @".join(self.get_performers()))
            
    @staticmethod
    def format_tags(tags):
        if len(tags) > 0: return "@{}".format(" @".join(self.get_tags()))

    def format_text(self):
        "{} {} {} {}".format(self.get_text(), Message.format_performers(self.get_performers()), Message.format_tags(self.get_tags()),
            Message.format_keywords(self.get_keywords()))

    def get_keywords(self):
        # if self.keywords: return self.keywords
        if len(self.keywords) > 0: return self.keywords
        keywords = Settings.get_keywords() or []
        if len(keywords) > 0: return keywords
        if not Settings.prompt("keywords"): return []
        question = {
            'type': 'input',
            'name': 'keywords',
            'message': 'Keywords:',
            'validate': ListValidator
        }
        answers = PyInquirer.prompt(question)
        keywords = answers["keywords"]
        keywords = keywords.split(",")
        keywords = [n.strip() for n in keywords]
        if not Settings.confirm(keywords): return self.get_keywords()
        self.keywords = keywords
        return self.keywords

    def get_performers(self):
        # if self.performers: return self.performers
        if len(self.performers) > 0: return self.performers
        performers = Settings.get_tags() or []
        if len(performers) > 0: return performers
        if not Settings.prompt("performers"): return []
        question = {
            'type': 'input',
            'name': 'performers',
            'message': 'Performers:',
            'validate': ListValidator
        }
        answers = PyInquirer.prompt(question)
        performers = answers["performers"]
        performers = performers.split(",")
        performers = [n.strip() for n in performers]
        if not Settings.confirm(performers): return self.get_performers()
        self.performers = performers
        return self.performers

    def get_tags(self):
        # if self.tags: return self.tags
        if len(self.tags) > 0: return self.tags
        tags = Settings.get_tags() or []
        if len(tags) > 0: return tags
        if not Settings.prompt("tags"): return []
        question = {
            'type': 'input',
            'name': 'tags',
            'message': 'Tags:',
            'validate': ListValidator
        }
        answers = PyInquirer.prompt(question)
        tags = answers["tags"]
        tags = tags.split(",")
        tags = [n.strip() for n in tags]
        if not Settings.confirm(tags): return self.get_tags()
        self.tags = tags
        return self.tags

    # ensures File references exist and are downloaded
    # files are File references
    # file references can be GoogleId references which need to download their source
    # files exist when checked for size
    # ?
    def get_files(self):
        if len(self.files) == 0 and Settings.get_input():
            files = Settings.get_input()
            for file in files:
                file_ = File()
                setattr(file_, "path", file)
                self.files.append(file_)
        elif len(self.files) == 0 and len(Google_File.get_files()) > 0:
            self.files = Google_File.select_files()
        elif len(self.files) == 0:
            self.files = File.select_files()
        files = []
        for file in self.files:
            if Settings.confirm(file.get_path()):
                file.prepare() # if Google file, downloads. if file, check size
                files.append(file)
        return files

    def get_price(self):
        if self.price: return self.price
        price = Settings.get_price() or None
        if price: return price
        if not Settings.prompt("price"): return ""
        question = {
            'type': 'input',
            'name': 'price',
            'message': 'Price',
            'validate': NumberValidator,
            'filter': lambda val: int(val)
        }
        answers = PyInquirer.prompt(question)
        price = answers["price"]
        if not Settings.confirm(price): return self.get_price()
        self.price = price
        return self.price

    def get_expiration(self):
        if self.expiration: return self.expiration
        expires = Settings.get_expiration() or None
        if expires: return expires
        if not Settings.prompt("expiration"): return None
        question = {
            'type': 'input',
            'name': 'expiration',
            'message': 'Expiration [1, 3, 7, 99 (\'No Limit\')]',
            'validate': ExpirationValidator
        }
        answers = PyInquirer.prompt(question)
        expiration = answers["expiration"]
        if not Settings.confirm(expiration): return self.get_expiration()
        self.expiration = expiration
        return self.expiration

    def get_poll(self):
        if self.poll and self.poll.check(): return self.poll
        poll = Settings.get_poll() or None
        if poll: return poll
        if not Settings.prompt("poll"): return None
        poll = Poll()
        poll.get()
        self.poll = poll
        return poll

    # ensures listed recipients are users
    # Settings.USERS and self.recipients should be usernames
    # if includes [all, recent, favorite] & usernames it only uses the 1st found of [all,...]
    def get_recipients(self):
        if len(self.recipients) == 0 and len(Settings.get_users()) > 0: 
            self.recipients = User.confirm(users=Settings.get_users())
        elif len(self.recipients) == 0:
            self.recipients = User.select_users()
        users = []
        for user in self.recipients:
            if isinstance(user, str):
                if user in Settings.get_message_choices():
                    return [user]
            user = User(user)
            users.append(user)
        return users

    def get_schedule(self):
        if self.schedule: return self.schedule
        schedule = Settings.get_schedule()
        if schedule: return schedule
        if not Settings.prompt("schedule"): return None
        questions = [
            {
                'type': 'input',
                'name': 'date',
                'message': 'Date (mm/dd/YYYY)',
                'validate': DateValidator
            },
            {
                'type': 'input',
                'name': 'time',
                'message': 'Time (HH:MM)',
                'validate': TimeValidator
            }
        ]
        answers = PyInquirer.prompt(questions)
        schedule = "{}:{}".format(answers["date"], answers["time"])
        if not Settings.confirm(schedule): return self.get_schedule()
        self.schedule = schedule
        return self.schedule

    def get_text(self):
        if self.text != "": return self.text
        text = Settings.get_text() or None
        if text: return text
        if not Settings.prompt("text"): return ""
        question = {
            'type': 'input',
            'name': 'text',
            'message': 'Text:'
        }
        answers = PyInquirer.prompt(question)
        text = answers["text"]
        if not Settings.confirm(text): return self.get_text()
        self.text = text
        return self.text

    def get_all(self):
        self.get_text()
        self.get_keywords()
        self.get_tags()
        self.get_price()
        self.get_poll()
        self.get_schedule()
        self.get_files()
        self.get_recipients()

    def get_post(self):
        self.get_text()
        self.get_keywords()
        self.get_tags()
        self.get_poll()
        self.get_schedule()
        self.get_files()
        self.get_recipients()

    def get_message(self):
        self.get_text()
        self.get_price()
        self.get_files()
        self.get_recipients()

    # sends to recipients
    # 'post' as recipient will post message instead
    def send(self):
        self.get_message()
        successful = False
        try: 
            # for user in self.get_recipients():
            for user in self.get_recipients():
                # if isinstance(user, str): 
                if str(user) == "post": successful_ = Driver.post(self)
                else: successful_ = User.message_user(username=user, message=self)
                if successful_: successful = successful_
                # if self.username in Settings.get_message_choices(): break
        except Exception as e:
            Settings.dev_print(e)
            successful = False
        if successful: self.backup_files()

    def post(self):
        self.get_post()
        successful = False
        try: successful = Driver.post(self)
        except Exception as e:
            Settings.dev_print(e)
            successful = False
        if successful: self.backup_files()
