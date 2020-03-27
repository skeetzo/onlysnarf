from datetime import datetime
from .file import File, Google_File
from .settings import Settings
from .user import User
import PyInquirer
from PyInquirer import Validator, ValidationError

class Message():
    def __init__(self):
        self.text = None
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
        self.questions = []
        self.duration = None
        self.schedule = None

    ###########################################################################

    def backup_files(self):
        for file in self.files:
            file.backup()

    def get_text(self):
        if self.text: return self.text
        text = Settings.get_text() or None
        if text: return text
        if not Settings.prompt("text"): return None
        questions = [
            {
                'type': 'input',
                'name': 'text',
                'message': 'Text:'
            }
        ]
        answers = PyInquirer.prompt(questions)
        text = answers["text"]
        if not Settings.confirm(text): return self.get_text()
        self.text = text
        return self.text

    def get_keywords(self):
        # if self.keywords: return self.keywords
        if len(self.keywords) > 0: return self.keywords
        keywords = Settings.get_keywords() or []
        if len(keywords) > 0: return keywords
        if not Settings.prompt("keywords"): return None
        questions = [
            {
                'type': 'input',
                'name': 'keywords',
                'message': 'Keywords:',
                'validate': ListValidator
            }
        ]
        answers = PyInquirer.prompt(questions)
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
        if not Settings.prompt("performers"): return None
        questions = [
            {
                'type': 'input',
                'name': 'performers',
                'message': 'Performers:',
                'validate': ListValidator
            }
        ]
        answers = PyInquirer.prompt(questions)
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
        if not Settings.prompt("tags"): return None
        questions = [
            {
                'type': 'input',
                'name': 'tags',
                'message': 'Tags:',
                'validate': ListValidator
            }
        ]
        answers = PyInquirer.prompt(questions)
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
        if not Settings.prompt("price"): return None
        questions = {
                'type': 'input',
                'name': 'price',
                'message': 'Price',
                'validate': NumberValidator,
                'filter': lambda val: int(val)
            }
        answers = PyInquirer.prompt(questions)
        price = answers["price"]
        if not Settings.confirm(price): return self.get_price()
        self.price = price
        return self.price

    def get_expiration(self):
        if self.expiration: return self.expiration
        expires = Settings.get_expires() or None
        if expires: return expires
        if not Settings.prompt("expiration"): return None
        questions = {
                'type': 'input',
                'name': 'expiration',
                'message': 'Expiration [1, 3, 7, 99 or \'No Limit\']',
                'validate': ExpirationValidator
            }
        answers = PyInquirer.prompt(questions)
        expiration = answers["expiration"]
        if not Settings.confirm(expiration): return self.get_expiration()
        self.expiration = expiration
        return self.expiration

    def get_poll(self):
        if self.poll and self.poll.questions and len(self.poll.questions) > 0: return self.poll
        poll = Settings.get_poll() or None
        if poll: return poll
        # if not Settings.prompt("poll"): return None
        duration = self.get_duration()
        if not duration: return None
        questions = self.get_questions()
        if not questions or len(questions) == 0: return None
        poll = {"duration":duration,"questions":questions}
        self.poll = poll
        return poll

    def get_questions(self):
        if len(self.questions) > 0: return self.questions
        questions = Settings.get_questions() or []
        if len(questions) > 0: return questions
        if not Settings.prompt("questions"): return None
        print("Enter Questions")
        while True:
            question = {
                    'type': 'input',
                    'name': 'question',
                    'message': 'Question:',
                }
            answers = PyInquirer.prompt(question)
            question = answers["question"]
            if str(question) == "": break
            questions.append(question)
        if not Settings.confirm(questions): return self.get_questions()
        self.questions = questions
        return self.questions
    
    def get_duration(self):
        if self.duration: return self.duration
        duration = Settings.get_duration() or None
        if duration: return duration
        if not Settings.prompt("duration"): return None
        question = {
                'type': 'input',
                'name': 'duration',
                'message': 'Duration [1, 3, 7, 99 or \'No Limit\']',
                'validate': DurationValidator
            }
        answers = PyInquirer.prompt(question)
        duration = answers["duration"]
        if not Settings.confirm(duration): return self.get_duration()
        self.duration = duration
        return self.duration

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

########################################################################################

class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end

class TimeValidator(Validator):
    def validate(self, document):
        try:
            datetime.strptime(document.text, '%H:%M')
        except ValueError:
            raise ValidationError(
                message='Please enter a time (HH:mm)',
                cursor_position=len(document.text))  # Move cursor to end

class DateValidator(Validator):
    def validate(self, document):
        try:
            datetime.strptime(document.text, '%m/%d/%Y')
        except ValueError:
            raise ValidationError(
                message='Please enter a date (mm/dd/YYYY)',
                cursor_position=len(document.text))  # Move cursor to end

class DurationValidator(Validator):
    def validate(self, document):
        if str(document.text).lower() not in str(Settings.get_duration_allowed()).lower():
            raise ValidationError(
                message='Please enter a duration ({})'.format(", ".join(Settings.get_duration_allowed())),
                cursor_position=len(document.text))  # Move cursor to end

class ExpirationValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter an expiration ({})'.format(", ".join(Settings.get_expiration_allowed())),
                cursor_position=len(document.text))  # Move cursor to end

class ListValidator(Validator):
    def validate(self, document):
        return True
        try:
            pass
            # import ast
            # ast.literal_eval(document.text)
        except Exception as e:
            raise ValidationError(
                message='Please enter a comma separated list of values',
                cursor_position=len(document.text))  # Move cursor to end

