from OnlySnarf.settings import SETTINGS as settings
from OnlySnarf.user import User

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
        self.questions = None
        self.duration = None
        self.schedule = None

    def backup_files(self):
        for file in self.files:
            file.backup()

    def get_text(self):
        if str(self.text) != "": return self.text
        text = settings.TEXT or ""
        if str(text) != "": return text
        print("Text:")
        text_ = input("({})>> ".format(text))
        if text_ == None or str(text_) == "": return text
        self.text = text_
        return text_

    def get_keywords(self):
        if len(self.keywords) > 0: return self.keywords
        keywords = settings.get_keywords() or []
        print("Keywords: ")
        keywords = input("({})>> ".format(keywords))
        if keywords == "": return None
        if str(keywords) == "None":
            keywords = []
        elif str(keywords) == "[]":
            keywords = []
        elif str(keywords) == " ":
            keywords = []
        else:
            keywords = keywords.split(",")
            keywords = [n.strip() for n in keywords]
        self.keywords = keywords
        return keywords

    def get_performers(self):
        if len(self.performers) > 0: return self.performers
        performers = settings.get_tags() or []
        if len(performers) > 0: return performers
        print("Performers: ")
        performers = input("({})>> ".format(performers))
        if performers == "": return []
        if str(performers) == "None":
            performers = []
        elif str(performers) == "[]":
            performers = []
        elif str(performers) == " ":
            performers = []
        else:
            performers = performers.split(",")
            performers = [n.strip() for n in performers]
        self.performers = performers
        return performers

    def get_tags(self):
        if len(self.tags) > 0: return self.tags
        tags = settings.get_tags() or []
        if len(tags) > 0: return tags
        print("Tags: ")
        tags = input("({})>> ".format(tags))
        if tags == "": return []
        if str(tags) == "None":
            tags = []
        elif str(tags) == "[]":
            tags = []
        elif str(tags) == " ":
            tags = []
        else:
            tags = tags.split(",")
            tags = [n.strip() for n in tags]
        self.tags = tags
        return tags

    # ensures File references exist and are downloaded
    # files are File references
    # file references can be GoogleId references which need to download their source
    # files exist when checked for size
    # ?
    def get_files(self):
        for file in files:
            file.prepare() # if Google file, downloads. if file, check size
        return self.files

    def get_price(self):
        if self.price: return self.price
        price = settings.PRICE or ""
        if str(price) != "": return price
        print("Price (>{}):".format(settings.PRICE_MINIMUM))
        price_ = input("({})>> ".format(price))
        if price_ == None or str(price_) == "": return price
        self.price = price_
        return price_

    # ensures listed recipients are users
    # settings.USERS and self.recipients should be usernames
    # if includes [all, recent, favorite] & usernames it only uses the 1st found of [all,...]
    def get_recipients(self):
        if len(self.recipients) == 0 and len(settings.get_users()) > 0: self.recipients = settings.get_users()
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
        expires = settings.EXPIRES or ""
        if str(expires) != "": return expires
        print("Expiration [1, 3, 7, 99 or 'No limit']:")
        expires_ = input("({})>> ".format(expires_))
        if expires_ == None or str(expires_) == "": return expires
        if str(expires_).lower() not in settings.EXPIRATION_ALLOWED:
            print("Error: Incorrect Expiration")
            return expires
        self.expiration = expires_
        return expires_

    def get_poll(self):
        if self.poll and self.poll.questions and len(self.poll.questions) > 0: return self.poll
        poll = settings.get_poll()
        if poll: return poll
        confirm = self.prompt(confirm, "Poll (y/n): ")
        if not confirm: return None
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
        print("Questions:\n> {}".format("\n> ".join(questions)))
        while True:
            question = None
            question = self.prompt(question, "Question:")
            if not question: break
            questions.append(question)
        self.questions = questions
        return questions
    
    def get_duration(self):
        if self.duration: return self.duration
        duration = settings.DURATION or ""
        if str(duration) != "": return duration
        print("Duration [1, 3, 7, 99 or 'No limit']:")
        duration_ = input("({})>> ".format(duration))
        if duration_ == None or str(duration_) == "": return duration
        if str(duration_).lower() not in settings.DURATION_ALLOWED:
            print("Error: Incorrect Duration")
            return ""
        self.duration = duration_
        return duration_

    def get_schedule(self):
        if self.schedule: return self.schedule
        schedule = settings.get_schedule()
        if schedule: return schedule
        schedule_ = self.prompt(schedule_, "Schedule (y/n): ")
        if not schedule_: return schedule
        schedule_ = input( "({})>> ".format(schedule))
        date_ = settings.DATE or ""
        print("Date [mm/dd/YY]: ")
        date = input("({})>>".format(date_))
        time_ = settings.TIME or ""
        print("Time [HH:MM]: ")
        time = input("({})>>".format(time_))
        schedule = "{}:{}".format(date, time)
        self.schedule = schedule
        return schedule

    def get_post(self):
        self.get_text()
        self.get_keywords()
        self.get_tags()
        self.get_files()
        self.get_price()
        # self.get_recipients()
        self.get_poll()
        self.get_schedule()

    # sends to recipients
    # 'post' as recipient will post message instead
    def send(self):
        self.get_post()
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
            
    def prompt(self, var, text):
        if str(text) == "": return False
        var = input("{}\n[Enter]|[y|n]".format(text))
        if str(text) == "None" or str(text).lower() == "skip" or str(text).lower() == "s":
            print("Skipping")
            return False
        elif str(text) == "Cancel" or str(text).lower() == "cancel" or str(text).lower() == "c":
            print("Cancelling")
            return False
        elif str(text) == "No" or str(text).lower() == "n":
            return False
        return var