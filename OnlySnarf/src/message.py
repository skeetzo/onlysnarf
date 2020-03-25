import datetime
from OnlySnarf.settings import SETTINGS as settings
from OnlySnarf.user import User
from PyInquirer

class Message():
    def __init__(self):
        self.text = None
        self.files = None
        ##
        self.keywords = None
        self.tags = None
        self.performers = None
        ## messages
        self.price = None
        self.recipients = None # users to send to
        ## posts
        self.expiration = None
        self.poll = None
        self.questions = None
        self.duration = None
        self.schedule = None

    ###########################################################################

    def backup_files(self):
        for file in self.files:
            file.backup()

    def get_text(self):
        if self.text: return self.text
        text = settings.TEXT or None
        if text: return text
        if not settings.prompt("text"): return None
        questions = [
            {
                'type': 'input',
                'name': 'text',
                'message': 'Text'
            }
        ]
        answers = PyInquirer.prompt(questions)
        self.text = answers["text"]
        if not settings.confirm(self.text): return None
        return self.text

    def get_keywords(self):
        if self.keywords: return self.keywords
        keywords = settings.get_keywords() or []
        if len(keywords) > 0: return keywords
        if not settings.prompt("keywords"): return None
        questions = [
            {
                'type': 'input',
                'name': 'keywords',
                'message': 'Tags'
            }
        ]
        answers = PyInquirer.prompt(questions)
        self.keywords = answers["keywords"]
        self.keywords = self.keywords.split(",")
        self.keywords = [n.strip() for n in self.keywords]
        if not settings.confirm(self.keywords): return None
        return self.keywords

    def get_performers(self):
        if self.performers: return self.performers
        performers = settings.get_tags() or []
        if len(performers) > 0: return performers
        if not settings.prompt("performers"): return None
        questions = [
            {
                'type': 'input',
                'name': 'performers',
                'message': 'Tags'
            }
        ]
        answers = PyInquirer.prompt(questions)
        self.performers = answers["performers"]
        self.performers = self.performers.split(",")
        self.performers = [n.strip() for n in self.performers]
        if not settings.confirm(self.performers): return None
        return self.performers

    def get_tags(self):
        if self.tags: return self.tags
        tags = settings.get_tags() or []
        if len(tags) > 0: return tags
        if not settings.prompt("tags"): return None
        questions = [
            {
                'type': 'input',
                'name': 'tags',
                'message': 'Tags'
            }
        ]
        answers = PyInquirer.prompt(questions)
        self.tags = answers["tags"]
        self.tags = self.tags.split(",")
        self.tags = [n.strip() for n in self.tags]
        if not settings.confirm(self.tags): return None
        return self.tags

    # ensures File references exist and are downloaded
    # files are File references
    # file references can be GoogleId references which need to download their source
    # files exist when checked for size
    # ?
    def get_files(self):
        for file in files:
            file.prepare() # if Google file, downloads. if file, check size
        return self.files

        if self.files: File.confirm(self.files)
        else: files = File.select_files()

    def get_price(self):
        if self.price: return self.price
        price = settings.PRICE or None
        if price: return price
        if not settings.prompt("price"): return None
        questions = [
            {
                'type': 'input',
                'name': 'price',
                'message': 'Price',
                'validate': NumberValidator,
                'filter': lambda val: int(val)
            }
        ]
        answers = PyInquirer.prompt(questions)
        self.price = answers["price"]
        if not settings.confirm(self.price): return None
        return self.price


    # ensures listed recipients are users
    # settings.USERS and self.recipients should be usernames
    # if includes [all, recent, favorite] & usernames it only uses the 1st found of [all,...]
    def get_recipients(self):
        if len(self.recipients) == 0 and len(settings.get_users()) > 0: 
            self.recipients = User.confirm(users=settings.get_users())
        elif len(self.recipients) == 0:
            self.recipients = User.select_users()
        users = []
        for user in self.recipients:
            if isinstance(user, str):
                if user in settings.MESSAGE_CHOICES:
                    return [user]
            user = User(user)
            users.append(user)
        return users

    def get_expiration(self):
        if self.expiration: return self.expiration
        expires = settings.EXPIRES or None
        if expires: return expires
        if not settings.prompt("expiration"): return None
        questions = [
            {
                'type': 'input',
                'name': 'expiration',
                'message': 'Expiration [1, 3, 7, 99 or \'No limit\']',
                'validate': ExpirationValidator
            }
        ]
        answers = PyInquirer.prompt(questions)
        self.expiration = answers["expiration"]
        if not settings.confirm(self.expiration): return None
        return self.expiration

    def get_poll(self):
        if self.poll and self.poll.questions and len(self.poll.questions) > 0: return self.poll
        poll = settings.get_poll() or None
        if poll: return poll
        if not settings.prompt("poll"): return None
        duration = self.get_duration()
        if not duration: return None
        questions = self.get_questions()
        if not questions or len(questions) == 0: return None
        poll = {"duration":duration,"questions":questions}
        self.poll = poll
        return poll

    def get_questions(self):
        if len(self.questions) > 0: return self.questions
        questions = settings.QUESTIONS or []
        if len(questions) > 0: return questions
        if not settings.prompt("questions"): return None
        while True:
            question = [
                {
                    'type': 'input',
                    'name': 'question',
                    'message': 'Question:',
                }
            ]
            answers = PyInquirer.prompt(question)
            question = answers["question"]
            if str(question) == "": break
            questions.append(question)
        if not settings.confirm(questions): return None
        self.questions = questions
        return self.questions
    
    def get_duration(self):
        if self.duration: return self.duration
        duration = settings.DURATION or None
        if duration: return duration
        if not settings.prompt("duration"): return None
        questions = [
            {
                'type': 'input',
                'name': 'duration',
                'message': 'Duration [1, 3, 7, 99 or \'No limit\']',
                'validate': DurationValidator
            }
        ]
        answers = PyInquirer.prompt(questions)
        self.duration = answers["duration"]
        if not settings.confirm(self.duration): return None
        return self.duration

    def get_schedule(self):
        if self.schedule: return self.schedule
        schedule = settings.get_schedule()
        if schedule: return schedule
        if not settings.prompt("schedule"): return None
        questions = [
            {
                'type': 'input',
                'name': 'date',
                'message': 'Date [mm/dd/YYYY]',
                'validate': DateValidator
            },
            {
                'type': 'input',
                'name': 'time',
                'message': 'Time [HH:MM]',
                'validate': TimeValidator
            }
        ]
        answers = PyInquirer.prompt(questions)
        self.schedule = "{}:{}".format(answers["date"], answers["time"])
        if not settings.confirm(self.schedule): return None
        return self.schedule

    def get_all(self):
        self.get_text()
        self.get_keywords()
        self.get_tags()
        self.get_files()
        self.get_price()
        self.get_recipients()
        self.get_poll()
        self.get_schedule()

    def get_post():
        self.get_text()
        self.get_keywords()
        self.get_tags()
        self.get_files()
        self.get_recipients()
        self.get_poll()
        self.get_schedule()

    def get_message():
        self.get_text()
        self.get_files()
        self.get_price()
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
                # if self.username in settings.MESSAGE_CHOICES: break
        except Exception as e:
            settings.devPrint(e)
            successful = False
        if successful: self.backup_files()

    def post(self):
        self.get_post()
        successful = False
        try: successful = Driver.post(self)
        except Exception as e:
            settings.devPrint(e)
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
            datetime.datetime.strptime(date_text, '%H-%M')
        except ValueError:
            raise ValidationError(
                message='Please enter a time (HH:mm)',
                cursor_position=len(document.text))  # Move cursor to end

class DateValidator(Validator):
    def validate(self, document):
        try:
            datetime.datetime.strptime(date_text, '%m-%d-%Y')
        except ValueError:
            raise ValidationError(
                message='Please enter a date (mm/dd/YYYY)',
                cursor_position=len(document.text))  # Move cursor to end

class DurationValidator(Validator):
    def validate(self, document):
        if str(document.text) not in str(settings.DURATION_ALLOWED):
            raise ValidationError(
                message='Please enter a duration ({})'.format(", ".join(settings.DURATION_ALLOWED)),
                cursor_position=len(document.text))  # Move cursor to end

class ExpirationValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter an expiration ({})'.format(", ".join(settings.EXPIRATION_ALLOWED)),
                cursor_position=len(document.text))  # Move cursor to end

