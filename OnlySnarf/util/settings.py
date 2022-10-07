import pkg_resources
import time
import PyInquirer
import os, json, sys
from datetime import datetime
from pathlib import Path
##
from .colorize import colorize
from .config import config
from . import defaults as DEFAULT
from .validators import valid_schedule, valid_time

class Settings:
    
    LAST_UPDATED_KEY = None
    CATEGORY = None
    CONFIRM = True
    FILES = None
    PERFORMER_CATEGORY = None
    PROMPT = True
    LOG = None

    # TODO: figure out what to do here better
    def init():
        import logging
        from .logger import get_logger
        loglevel = logging.INFO
        if config["debug"] loglevel = logging.DEBUG
        Settings.LOG = get_logger(loglevel)
        config()


    #####################
    ##### Functions #####
    #####################

    def debug_delay_check():
        if Settings.is_debug() == "True" and Settings.is_debug_delay() == "True":
            time.sleep(int(10))

    ##
    # Print
    ##

    def print(text):
        if int(config["verbose"]) >= 1:
            Settings.LOG.info(text)

    def print_same_line(text):
        sys.stdout.write('\r')
        sys.stdout.flush()
        sys.stdout.write(text)
        sys.stdout.flush()

    def maybe_print(text):
        if int(config["verbose"]) >= 2:
            Settings.LOG.debug(text)

    def dev_print(text):
        if int(config["verbose"]) >= 3:
            Settings.LOG.debug(text)

    def err_print(error):
        Settings.LOG.error(error)

    def warn_print(error):
        Settings.LOG.warning(error)

    def format_date(date):
        if isinstance(date, str):
            return datetime.strptime(date, DEFAULT.DATE_FORMAT).strftime(DEFAULT.DATE_FORMAT)
        else:
            return date.strftime(DEFAULT.DATE_FORMAT)

    def format_time(time):
        if isinstance(time, str):
            return datetime.strptime(time, DEFAULT.TIME_FORMAT).strftime(DEFAULT.TIME_FORMAT)
        else:
            return time.strftime(DEFAULT.TIME_FORMAT)

    ##
    # Getters
    ##

    def get_action():
        return config["action"]

    def get_actions():
        return DEFAULT.ACTIONS

    def get_amount():


        # # prompt skip
        # if not Settings.prompt("amount"): return None
        # question = {
        #     'type': 'input',
        #     'name': 'amount',
        #     'message': 'Amount:',
        #     'validate': AmountValidator,
        #     'filter': lambda val: int(myround(int(val)))
        # }
        # amount = prompt(question)["amount"]
        # if not Settings.confirm(amount): return self.get_amount()
        # self.amount = amount
        # return self.amount






        return config["amount"]

    def get_base_directory():
        USER = os.getenv('USER')
        if str(os.getenv('SUDO_USER')) != "root" and str(os.getenv('SUDO_USER')) != "None":
            USER = os.getenv('SUDO_USER')
        baseDir = "/home/{}/.onlysnarf".format(USER)
        # if os.environ.get('ENV') == "test":
          # baseDir = os.getcwd()
          # baseDir = os.path.dirname(__file__)
        return baseDir

    def get_browser_type():
        return config["browser"]

    def get_months():


        # # prompt skip
        # if not Settings.prompt("months"): return None
        # question = {
        #     'type': 'input',
        #     'name': 'months',
        #     'message': 'Months:',
        #     'validate': MonthValidator,
        #     'filter': lambda val: int(val)
        # }
        # months = prompt(question)["months"]
        # if not Settings.confirm(months): return self.get_months()
        # self.months = months
        # return self.months



        return config["months"]

    def get_category():
        cat = config["category"]
        if str(cat) == "image": cat = "images"
        if str(cat) == "gallery": cat = "galleries"
        if str(cat) == "video": cat = "videos"
        if str(cat) == "performer": cat = "performers"
        return cat or None

    def get_categories():
        cats = []
        cats.extend(list(DEFAULT.CATEGORIES))
        cats.extend(list(config["categories"]))
        return cats

    def get_cookies_path():
        # return os.path.join(Settings.get_base_directory(), Settings.get_username(), "cookies.pkl")
        return os.path.join(Settings.get_base_directory(), "cookies.pkl")

    def get_price():
        return config["price"]


        # if not Settings.prompt("price"): return 0
        # question = {
        #     'type': 'input',
        #     'name': 'price',
        #     'message': 'Price',
        #     'validate': PriceValidator,
        #     'filter': lambda val: int(val)
        # }
        # price = prompt(question)["price"]
        # # if not Settings.confirm(price): return self.get_price(again=again)
        # self.price = price
        # return price

    def get_price_minimum():
        return DEFAULT.PRICE_MINIMUM

    def get_price_maximum():
        return DEFAULT.PRICE_MAXIMUM

    def get_date():
        config["date"] = Settings.format_date(config["date"])
        if str(config["date"]) == DEFAULT.DATE and str(config["schedule"]) != DEFAULT.SCHEDULE:
            if isinstance(config["schedule"], str):
                config["date"] = datetime.strptime(config["schedule"], DEFAULT.SCHEDULE_FORMAT).date().strftime(DEFAULT.DATE_FORMAT)
            else:
                config["date"] = config["schedule"].date().strftime(DEFAULT.DATE_FORMAT)
            config["date"] = datetime.strptime(str(config["date"]), DEFAULT.DATE_FORMAT)
        else:
            config["date"] = datetime.strptime(str(config["date"]), DEFAULT.DATE_FORMAT)
        config["date"] = config["date"].strftime(DEFAULT.DATE_FORMAT)    
        Settings.maybe_print("date (settings): {}".format(config["date"]))
        return config["date"]

    def get_default_greeting():
        return DEFAULT.GREETING or ""

    def get_default_refresher():
        return DEFAULT.REFRESHER or ""
        
    def get_discount_max_amount():
        return DEFAULT.DISCOUNT_MAX_AMOUNT or 0
        
    def get_discount_min_amount():
        return DEFAULT.DISCOUNT_MIN_AMOUNT or 0
        
    def get_discount_max_months():
        return DEFAULT.DISCOUNT_MAX_MONTHS or 0
        
    def get_discount_min_months():
        return DEFAULT.DISCOUNT_MIN_MONTHS or 0

    def get_download_max():
        return config["download_limit"] or DEFAULT.IMAGE_LIMIT
        
    def get_drive_ignore():
        return config["notkeyword"] or None
        
    def get_drive_keyword():
        return config["bykeyword"] or None
        
    def get_duration():
        return config["duration"] or None

    def get_promo_duration():
        return config["duration_promo"] or None
        
    def get_duration_allowed():
        return DEFAULT.DURATION_ALLOWED or []
        
    def get_duration_promo_allowed():
        return DEFAULT.PROMOTION_DURATION_ALLOWED or []

    def get_expiration():
        return config["expiration"]

    def get_promo_expiration():
        return config["promotion_expiration"]

    def get_input():
        return config["input"] or []

    def get_input_as_files():
        if Settings.FILES: return Settings.FILES
        from ..classes.file import File
        files = []
        if isinstance(config["input"], list):
            for file_path in config["input"]:
                file = File()
                setattr(file, "path", file_path)
                files.append(file)
        else:
            file = File()
            setattr(file, "path", config["input"])
            files.append(file)
        Settings.FILES = files
        return files

    def get_keywords():
        keywords = config["keywords"] or []
        keywords = [n.strip() for n in keywords]
        return keywords

    def get_logs_path(process):
        if process == "firefox":
            path_ = os.path.join(Settings.get_base_directory(), "log")
            Path(path_).mkdir(parents=True, exist_ok=True)
            return os.path.join(path_, "geckodriver.log")
        elif process == "google":
            path_ = os.path.join(Settings.get_base_directory(), "log")
            Path(path_).mkdir(parents=True, exist_ok=True)
            return os.path.join(path_, "chromedriver.log")
        return ""

    def get_message_choices():
        return DEFAULT.MESSAGE_CHOICES

    def get_root_path():
        return config["root_path"] or DEFAULT.ROOT_PATH

    def get_sort_method():
        return config["sort"] or "random"

    def get_performers():
        performers = config["performers"] or []
        performers = [n.strip() for n in performers]
        return performers

    def get_profile_path():
        return config["path_profile"] or DEFAULT.PROFILE_PATH

    def get_recent_user_count():
        return config["recent_users_count"] or 0
    
    def get_promotion_limit():
        return config["promotion_limit"] or None

    def get_promotion_method():
        return config["promotion_method"] or None

    def get_password():
        try: return Settings.get_user_config(Settings.get_username())["onlyfans_password"]
        except Exception as e: Settings.err_print(e)
        return ""

    def get_password_google():
        try: return Settings.get_user_config(Settings.get_username())["google_password"]
        except Exception as e: Settings.err_print(e)
        return ""

    def get_password_twitter():
        try: return Settings.get_user_config(Settings.get_username())["twitter_password"]
        except Exception as e: Settings.err_print(e)
        return ""

    def get_download_path():
        return config["path_download"]

    def get_users_path():
        return config["path_users"]

    def get_config_path():
        return config["path_config"]   

    def get_local_path():
        localPath = os.path.join(Settings.get_root_path(), Settings.get_username())
        from pathlib import Path
        Path(localPath).mkdir(parents=True, exist_ok=True)
        for cat in Settings.get_categories():
            Path(os.path.join(localPath, cat)).mkdir(parents=True, exist_ok=True)
        return localPath

    def get_destination():
        return config["destination"] or ""

    def get_source():
        return config["source"] or ""

    def get_source_options():
        return DEFAULT.SOURCES

    def get_reconnect_id():
        return config["session_id"] or ""

    def get_reconnect_url():
        return config["session_url"] or ""

    def get_remote_host():
        return config["remote_host"] or DEFAULT.REMOTE_HOST

    def get_remote_port():
        return config["remote_port"] or DEFAULT.REMOTE_PORT

    def get_remote_path():
        return config["remote_path"] or DEFAULT.REMOTE_PATH

    def get_remote_username():
        return config["remote_username"] or ""

    def get_remote_password():
        return config["remote_password"] or ""

    def get_profile_method():
        return config["profile_method"] or None

    def get_schedule():
        if str(config["schedule"]) == DEFAULT.SCHEDULE:
            config["schedule"] = datetime.strptime("{} {}".format(Settings.get_date(), Settings.get_time()), DEFAULT.SCHEDULE_FORMAT).strftime(DEFAULT.SCHEDULE_FORMAT)
        elif not isinstance(config["schedule"], str):
            config["schedule"] = config["schedule"].strftime(DEFAULT.SCHEDULE_FORMAT)
        Settings.maybe_print("schedule (settings): {}".format(config["schedule"]))
        return config["schedule"]

    def get_tags():
        tags = config["tags"] or []
        tags = [n.strip() for n in tags]
        return tags

    def get_text():
        return config["text"] or ""

    def get_time():
        config["time"] = Settings.format_time(config["time"])        
        if (str(config["time"]) == DEFAULT.TIME or str(config["time"]) == DEFAULT.TIME_NONE) and str(config["schedule"]) != DEFAULT.SCHEDULE:
            Settings.dev_print("time from schedule")
            date = datetime.strptime(str(config["schedule"]), DEFAULT.SCHEDULE_FORMAT)
            config["time"] = datetime.strptime(str(date.time().strftime(DEFAULT.TIME_FORMAT)), DEFAULT.TIME_FORMAT)
        else:
            Settings.dev_print("time from config")
            config["time"] = datetime.strptime(str(config["time"]), DEFAULT.TIME_FORMAT)
        config["time"] = config["time"].strftime(DEFAULT.TIME_FORMAT)
        Settings.maybe_print("time (settings): {}".format(config["time"]))
        return config["time"]

    def get_title():
        return config["title"] or ""
        
    def get_skipped_users():
        return config["skipped_users"] or []
        
    def get_questions():
        return config["questions"] or []
        
    def get_upload_max():
        return config["upload_max"] or DEFAULT.IMAGE_LIMIT
        
    # def get_upload_max_messages():
        # return config["upload_max_messages"] or UPLOAD_MAX_MESSAGES

    def get_login_method():
        return config["login"]
        
    def get_upload_max_duration():
        return config["upload_max_duration"] or DEFAULT.UPLOAD_MAX_DURATION # 6 hours

    # comma separated string of usernames
    def get_users():
        from ..classes.user import User
        if str(config["user"]) != "None":
            if str(config["user"]) == "all":
                config["users"].extend([user.username for user in User.get_all_users()])
            elif str(config["user"]) == "recent":
                config["users"].extend([user.username for user in User.get_recent_users()])
            elif str(config["user"]) == "favorite":
                config["users"].extend([user.username for user in User.get_favorite_users()])
            elif str(config["user"]) == "random":
                config["users"].append(User.get_random_user().username)
            else: config["users"].append(config["user"])
        users = []
        for user in [n.strip() for n in config["users"]]:
            if isinstance(user, User): pass
            elif isinstance(user, str): user = User({"username":user})
            # BUG (potential): might bug out if the username is for whatever reason all numbers
            elif isinstance(user, int): user = User({"id":user})
            users.append(user)
        return users

    def get_user():
        return Settings.get_users()[0]

    def get_email():
        return config["email"]

    def get_user_configs():
        # load configs from .onlysnarf or baseDir
        pass

    def get_user_config(username="default"):
        import configparser
        config_file = configparser.ConfigParser()
        # strip email
        if "@" in username: username = username[0 : username.index("@")]
        Settings.dev_print("retreiving user config: {}".format(username))
        config_file.read(os.path.join(Settings.get_base_directory(), "users", username+".conf"))
        userConfig = {}
        for section in config_file.sections():
            # print(section)
            for key in config_file[section]:
                # print(section, key, config_file[section][key].strip("\""))
                userConfig[section.lower()+"_"+key.lower()] = config_file[section][key].strip("\"")
        return userConfig

    def get_username():
        return config["username"] or ""

    def get_username_onlyfans():
        try:
            return Settings.get_user_config(Settings.get_username())["onlyfans_username"]
        except Exception as e:
            Settings.err_print(e)
        return ""

    def get_username_google():
        try:
            return config["google_username"] or Settings.get_user_config(Settings.get_username())["google_username"]
        except Exception as e:
            Settings.err_print(e)
        return ""            

    def get_username_twitter():
        try:
            return config["twitter_username"] or Settings.get_user_config(Settings.get_username())["twitter_username"]
        except Exception as e:
            Settings.err_print(e)
        return ""

    ## TODO
    # add arg -profile
    # add method for reading config profiles from conf/users

    def get_profile():
        pass

    def select_profile():
        pass

    # def get_users_favorite():
    #     return config["users_favorite"] or []
        
    def get_verbosity():
        return config["verbose"] or 0

    def get_version():
        return pkg_resources.get_distribution("onlysnarf").version

    def get_user_num():
        return config["users_read"] or DEFAULT.USER_LIMIT

    # Bools

    def is_confirm():
        return Settings.CONFIRM or config["confirm"]

    def is_cookies():
        return config["cookies"]

    def is_delete():
        return config["delete"]

    def is_delete_empty():
        return config["delete_empty"]

    def is_debug(process=None):
        if process == "firefox": return config["debug_firefox"]
        elif process == "google": return config["debug_google"]
        elif process == "selenium": return config["debug_selenium"]
        elif process == "cookies": return config["debug_cookies"]
        # elif process == "tests": return 
        return config["debug"]

    def is_debug_delay():
        return config["debug_delay"]

    def is_force_backup():
        return config["force_backup"]

    def is_force_upload():
        return config["force_upload"]

    def is_keep():
        return config["keep"]

    def is_prefer_local():
        return config["prefer_local"]

    def is_prompt():
        return Settings.PROMPT

    def is_save_users():
        return config["save_users"]
        
    def is_reduce():
        return config["enable_reduce"]
    
    def is_show_window():
        return config["show"]

    def is_split():
        return config["enable_split"]
        
    def is_trim():
        return config["enable_trim"]
        
    def is_tweeting():
        return config["tweeting"]
        
    def is_backup():
        return config["backup"]
        
    def is_skip_download():
        return config["skip_download"]
        
    def is_skip_upload():
        return config["skip_upload"]

    ##
    # Menu
    ##

    def confirm(text):
        try:
            if text == None: return False
            if list(text) == []: return False
            if str(text) == "": return False
            # if config["confirm"] == "True": return True
            # if 
        except: pass
        questions = [
            {
                'type': 'confirm',
                'message': 'Is this correct? -> {}'.format(text),
                'name': 'confirm',
                'default': True,
            }
        ]
        return PyInquirer.prompt(questions)["confirm"]

    def header():
        if Settings.LAST_UPDATED_KEY is not None:
            print("Updated: {} = {}".format(Settings.LAST_UPDATED_KEY, config[str(Settings.LAST_UPDATED_KEY).replace(" ","_").lower()]))
            print('\r')
        Settings.LAST_UPDATED_KEY = None

    def menu():
        skipList = ["action", "amount", "category", "categories", "cron", "input", "messages", "posts", "date", "duration", "expiration", "keywords", "limit", "months", "bykeyword", "notkeyword", "price", "config_path", "questions", "schedule", "skipped_users", "tags", "text", "time", "title", "user", "users", "username", "password", "users_favorite"]
        print('Settings')
        keys = [key.replace("_"," ").title() for key in config.keys() if key.lower() not in skipList and "categories" not in str(key).lower() and "messages" not in str(key).lower()]
        keys.insert(0, "Back")
        question = {
            'type': 'list',
            'name': 'choice',
            'message': 'Set:',
            'choices': keys,
            'filter': lambda val: val.lower()
        }
        answer = PyInquirer.prompt(question)["choice"]
        if str(answer).lower() == "back": return
        Settings.set_setting(answer.replace(" ", "_"))

    def prompt(text):
        if list(text) == []: return False
        if str(text) == "": return False
        if not Settings.PROMPT: return False
        question = {
            'type': 'confirm',
            'message': '{}?'.format(str(text).capitalize()),
            'name': 'confirm',
            'default': True,
        }
        return PyInquirer.prompt(question)["confirm"]

    def prompt_email():
        if not Settings.PROMPT: return False
        question = {
            'type': 'input',
            'message': 'Email:',
            'name': 'email'
        }
        email = PyInquirer.prompt(question)["email"]
        Settings.set_email(email)
        return email

    def prompt_username():
        if not Settings.PROMPT: return False
        question = {
            'type': 'input',
            'message': 'Username:',
            'name': 'username'
        }
        username = PyInquirer.prompt(question)["username"]
        Settings.set_username(username)
        return username

    def prompt_password():
        if not Settings.PROMPT: return False
        question = {
            'type': 'password',
            'message': 'Password:',
            'name': 'password'
        }
        pw = PyInquirer.prompt(question)["password"]
        Settings.set_password(pw)
        return pw

    def prompt_username_google():
        if not Settings.PROMPT: return False
        question = {
            'type': 'input',
            'message': 'Google username:',
            'name': 'username'
        }
        username = PyInquirer.prompt(question)["username"]
        Settings.set_username_google(username)
        return username

    def prompt_password_google():
        if not Settings.PROMPT: return False
        question = {
            'type': 'password',
            'message': 'Google password:',
            'name': 'password'
        }
        pw = PyInquirer.prompt(question)["password"]
        Settings.set_password_google(pw)
        return pw

    def prompt_username_twitter():
        if not Settings.PROMPT: return False
        question = {
            'type': 'input',
            'message': 'Twitter username:',
            'name': 'username'
        }
        username = PyInquirer.prompt(question)["username"]
        Settings.set_username_twitter(username)
        return username

    def prompt_password_twitter():
        if not Settings.PROMPT: return False
        question = {
            'type': 'password',
            'message': 'Twitter password:',
            'name': 'password'
        }
        pw = PyInquirer.prompt(question)["password"]
        Settings.set_password_twitter(pw)
        return pw

    def select_category(categories=None):
        # if Settings.CATEGORY: return Settings.CATEGORY
        if not categories: categories = Settings.get_categories()
        print("Select a Category")
        categories.insert(0, "Back")
        question = {
            'type': 'list',
            'message': 'Category:',
            'name': 'category',
            'choices': categories,
            'filter': lambda cat: cat.lower()
        }
        cat = PyInquirer.prompt(question)["category"]
        if str(cat) == "back": return None
        if not Settings.confirm(cat): return Settings.select_category()
        # Settings.CATEGORY = cat
        config["category"] = cat
        return cat

    ##
    # Setters
    ##

    def set_bycategory(cat):
        config["bycategory"] = cat

    def set_category(cat):
        config["category"] = cat

    def set_cookies(value):
        config["cookies"] = value

    def set_confirm(value):
        config["confirm"] = value

    def set_email(email):
        config["email"] = str(email)

    def set_debug(newValue):
        if str(newValue) == "tests":
            # config["confirm"] = False
            # config["prompt"] = False
            Settings.CONFIRM = False
            Settings.PROMPT = False
        else:
            config["debug"] = newValue

    def set_username(username):
        config["username"] = str(username)

    def set_username_google(username):
        config["username_google"] = str(username)

    def set_username_twitter(username):
        config["username_twitter"] = str(username)

    def set_password(password):
        config["password"] = str(password)

    def set_password_google(password):
        config["password_google"] = str(password)

    def set_password_twitter(password):
        config["password_twitter"] = str(password)

    def set_prefer_local(buul):
        config["prefer_local"] = buul
    
    def set_prefer_local_following(buul):
        config["prefer_local_following"] = buul

    def set_prompt(value):
        Settings.PROMPT = value

    def set_setting(key):
        try:
            value = config[key]
            key = key.replace("_"," ").title()
            print("Current: {}".format(value))
            if str(value) == "True" or str(value) == "False":
                question = {
                    'type': 'confirm',
                    'name': 'setting',
                    'message': "Toggle value?"
                }
                answer = PyInquirer.prompt(question)["setting"]
                if not answer: return Settings.menu()
                if bool(value): config[key.lower()] = False
                else: config[key.lower()] = True
            else:
                question = {
                    'type': 'input',
                    'name': 'setting',
                    'message': "New value:",
                    # 'default': int(value)
                }
                answer = PyInquirer.prompt(question)["setting"]
                if not Settings.confirm(answer): return Settings.menu()
                config[key.lower().replace(" ","_")] = answer
            Settings.LAST_UPDATED_KEY = key.lower()
        except Exception as e:
            Settings.dev_print(e)

###########################################################################



#     def update_value(self, variable, newValue):
#         variable = str(variable).upper().replace(" ","_")
#         try:
#             # print("Updating: {} = {}".format(variable, newValue))
#             setattr(self, variable, newValue)
#             # print("Updated: {} = {}".format(variable, getattr(self, variable)))
#         except Exception as e:
#             maybePrint(e)

# # move this behavior to user
#     def update_profile_value(self, variable, newValue):
#         variable = str(variable).upper().replace(" ","_")
#         try:
#             # print("Updating: {} = {}".format(variable, newValue))
#             Settings.PROFILE.setattr(self, variable, newValue)
#             # print("Updated: {} = {}".format(variable, getattr(self, variable)))
#         except Exception as e:
#             maybePrint(e)














































#######################################################################################

def delayForThirty():
    Settings.maybe_print("30...")
    time.sleep(10)
    Settings.maybe_print("20...")
    time.sleep(10)
    Settings.maybe_print("10...")
    time.sleep(7)
    Settings.maybe_print("3...")
    time.sleep(1)
    Settings.maybe_print("2...")
    time.sleep(1)
    Settings.maybe_print("1...")
    time.sleep(1)