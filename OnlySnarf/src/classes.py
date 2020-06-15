from datetime import datetime
from .driver import Driver
from .settings import Settings
from .user import User
import PyInquirer
from .validators import AmountValidator, MonthValidator, LimitValidator, NumberValidator, TimeValidator, DateValidator, DurationValidator, ExpirationValidator, ListValidator

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
        if str(self.get_username()).lower() == "all":
            users = User.get_all_users()
        elif str(self.get_username()).lower() == "recent":
            users = User.get_new_users()
        elif str(self.get_username()).lower() == "favorite":
            users = User.get_favorite_users()
        else: users = [self]
        successful = False
        for user in users:
            self.username = user.username
            successful_ = Driver.discount_user(self)
            if successful_: successful = successful_
        return successful

    @staticmethod
    def create():
        discount = Discount()
        discount.apply()

    def get(self):
        if self.gotten: return
        gotten = self.get_username()
        if not gotten: return
        gotten = self.get_amount()
        if not gotten: return
        gotten = self.get_months()
        if not gotten: return
        self.gotten = True

    def get_amount(self):
        if self.amount: return self.amount
        amount = Settings.get_amount() or None
        print(amount)
        if amount: return amount
        if not Settings.prompt("amount"): return None
        question = {
            'type': 'input',
            'name': 'amount',
            'message': 'Amount:',
            'validate': AmountValidator,
            'filter': lambda val: int(myround(int(val)))
        }
        answers = PyInquirer.prompt(question)
        amount = answers["amount"]
        if not Settings.confirm(amount): return self.get_amount()
        self.amount = amount
        return self.amount

    def get_months(self):
        if self.months: return self.months
        months = Settings.get_months() or None
        if months: return months
        if not Settings.prompt("months"): return None
        question = {
            'type': 'input',
            'name': 'months',
            'message': 'Months:',
            'validate': MonthValidator,
            'filter': lambda val: int(val)
        }
        answers = PyInquirer.prompt(question)
        months = answers["months"]
        if not Settings.confirm(months): return self.get_months()
        self.months = months
        return self.months

    def get_username(self):
        if self.username: return self.username
        username = User.select_user()
        self.username = username
        return self.username

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

    def get_questions(self):
        if len(self.questions) > 0: return self.questions
        questions = Settings.get_questions() or []
        if len(questions) > 0: return questions
        if not Settings.prompt("questions"): return []
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
    
    def get_duration(self): # months
        if self.duration: return self.duration
        duration = Settings.get_duration() or None
        if duration: return duration
        if not Settings.prompt("duration"): return None
        question = {
            'type': 'input',
            'name': 'duration',
            'message': 'Duration [1, 3, 7, 99 (\'No Limit\')]',
            'validate': DurationValidator
        }
        answers = PyInquirer.prompt(question)
        duration = answers["duration"]
        if not Settings.confirm(duration): return self.get_duration()
        self.duration = duration
        return self.duration

class Promotion:

    def __init__(self):
        self.limit = None
        self.expiration = None
        self.duration = None
        self.user = None
        self.message = None
        self.gotten = False

    # requires the copy/paste and email steps
    def create_trial_link(self):
        print("Promotion - Creating Trial Link")
        self.get()
        if not self.gotten: return
        if not Settings.prompt("Promotion"): return
        # limit, expiration, months, user
        Driver.promotional_trial_link(self)
        # link = Driver.promotional_trial_link()
        # text = "Here's your free trial link!\n"+link
        # Settings.dev_print("Link: "+str(text))
        # Settings.send_email(email, text)

    # apply discount directly to user on user's profile page
    def apply_to_user():
        print("Promotion - Apply To User: {}".format(self.user.username))
        self.get()
        if not self.gotten: return
        if not Settings.prompt("Promotion"): return
        # user, expiration, months, message
        Driver.promotion_user_directly(self)

    def get(self):
        if self.gotten: return
        gotten = self.get_user()
        if not gotten: return
        gotten = self.get_expiration()
        if not gotten: return
        gotten = self.get_limit()
        if not gotten: return
        gotten = self.get_duration()
        if not gotten: return
        gotten = self.get_message()
        if not gotten: return
        self.gotten = True

    def get_expiration(self):
        if self.expiration: return self.expiration
        expiration = Settings.get_expiration() or None
        if expiration: return expiration
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

    def get_limit(self):
        if self.limit: return self.limit
        limit = Settings.get_limit() or None
        if limit: return limit
        if not limit.prompt("limit"): return None
        question = {
            'type': 'input',
            'name': 'limit',
            'message': 'Expiration [1, 3, 7, 99 (\'No Limit\')]',
            'validate': LimitValidator
        }
        answers = PyInquirer.prompt(question)
        limit = answers["limit"]
        if not Settings.confirm(limit): return self.get_limit()
        self.limit = limit
        return self.limit

    def get_message(self):
        if self.message != "": return self.message
        message = Settings.get_text() or None
        if message: return message
        if not Settings.prompt("message"): return ""
        question = {
            'type': 'input',
            'name': 'message',
            'message': 'Message:'
        }
        answers = PyInquirer.prompt(question)
        message = answers["message"]
        if not Settings.confirm(message): return self.get_text()
        self.message = message
        return self.message

    def get_duration(self): # months
        if self.duration: return self.duration
        duration = Settings.get_duration() or None
        if duration: return duration
        if not Settings.prompt("duration"): return None
        question = {
            'type': 'input',
            'name': 'duration',
            'message': 'Duration [1, 3, 7, 99 (\'No Limit\')]',
            'validate': DurationValidator
        }
        answers = PyInquirer.prompt(question)
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
            date = datetime.strptime(str(self.get_date()), "%Y-%m-%d %H:%M:%S")
            self.year = date.year
            self.month = date.strftime("%B")
            self.day = date.day
            if self.get_time():
                self.hour = date.hour
                self.minute = date.minute
        self.gotten = True

    def get_date(self):
        if self.date: return self.date
        date = Settings.get_date() or None
        if date: return date
        schedule = Settings.get_schedule() or None
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
        answers = PyInquirer.prompt(question)
        date = answers["date"]
        if not Settings.confirm(date): return self.get_date()
        self.date = date
        return self.date

    def get_time(self):
        if self.time: return self.time
        time = Settings.get_time() or None
        if time: return time
        schedule = Settings.get_schedule() or None
        if schedule:
            time = datetime.strptime(str(schedule), "%Y-%m-%d %H:%M:%S")
            self.time = time.time()
            return self.time
        if not Settings.prompt("time"): return None
        question = {
            'type': 'input',
            'name': 'time',
            'message': 'Enter a time (HH:MM):',
            'validate': TimeValidator
        }
        answers = PyInquirer.prompt(question)
        time = answers["time"]
        if not Settings.confirm(time): return self.get_time()
        self.time = time
        return self.time

# round to 5
def myround(x, base=5):
    return base * round(x/base)