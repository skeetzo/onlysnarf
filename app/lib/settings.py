import pkg_resources
import time
import PyInquirer
import os, json
##
from .colorize import colorize
from .libb.config import config
from .libb import defaults as DEFAULT
from .logger import logging
log = logging.getLogger('onlysnarf')

class Settings:
    
    LAST_UPDATED_KEY = False
    CATEGORY = None
    CONFIRM = True
    FILES = None
    PERFORMER_CATEGORY = None
    PROMPT = True

    def __init__():
        pass

    #####################
    ##### Functions #####
    #####################

    def debug_delay_check():
        if Settings.is_debug() and Settings.is_debug_delay():
            time.sleep(int(10))

    ##
    # Print
    ##

    def print(text):
        if int(config["verbose"]) >= 1:
            log.info(text)

    def print_same_line(text):
        sys.stdout.write('\r')
        sys.stdout.flush()
        sys.stdout.write(text)
        sys.stdout.flush()

    def maybe_print(text):
        if int(config["verbose"]) >= 2:
            log.verbose(text)

    # update for verbosity
    def dev_print(text):
        if int(config["verbose"]) >= 3:
            if "successful" in str(text).lower():
                log.successful(text)
            elif "failure" in str(text).lower():
                log.failure(text)
            else:
                log.debug(text)

    def err_print(error):
        log.error(error)

    def warn_print(error):
        log.warning(error)

    ##
    # Getters
    ##

    def get_action():
        return config["action"]

    def get_actions():
        return config["actions"]

    def get_amount():
        return config["amount"]

    def get_browser_type():
        return config["browser"]

    def get_months():
        return config["months"]

    def get_category():
        cat = config["category"]
        if str(cat) == "image": cat = "images"
        if str(cat) == "gallery": cat = "galleries"
        if str(cat) == "video": cat = "videos"
        if str(cat) == "performer": cat = "performers"
        return cat or None

    def get_category_performer():
        cat = config["performer_category"]
        if str(cat) == "image": cat = "images"
        if str(cat) == "gallery": cat = "galleries"
        if str(cat) == "video": cat = "videos"
        # if str(cat) == "performer": cat = "performers"
        return cat or None

    def get_categories():
        cats = []
        cats.extend(list(DEFAULT.CATEGORIES))
        cats.extend(list(config["categories"]))
        return cats

    def get_cookies_path():
        return os.path.join(Settings.get_mount_path(), Settings.get_username(), "cookies.pkl")

    def get_price():
        return config["price"] or ""

    def get_price_minimum():
        return DEFAULT.PRICE_MINIMUM or 0

    def get_date():
        return config["date"] or None

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
        return config["image_limit"] or DEFAULT.IMAGE_LIMIT
        
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
        return config["expiration"] or config["promotion_expiration"] or None
        
    def get_expiration_allowed():
        return DEFAULT.EXPIRATION_ALLOWED or []

    def get_input():
        return config["input"] or []

    def get_input_as_files():
        if Settings.FILES: return Settings.FILES
        from .file import File
        files = []
        for file_path in config["input"]:
            file = File()
            setattr(file, "path", file_path)
            files.append(file)
        Settings.FILES = files
        return files

    def get_keywords():
        keywords = config["keywords"] or []
        keywords = [n.strip() for n in keywords]
        return keywords

    def get_limit():
        return config["limit"] or None

    def get_message_choices():
        return DEFAULT.MESSAGE_CHOICES

    def get_mount_path():
        return config["mount_path"] or DEFAULT.MOUNT_PATH

    def get_sort_method():
        return config["sort"] or "random"

    def get_performers():
        performers = config["performers"] or []
        performers = [n.strip() for n in performers]
        return performers

    def get_profile_path():
        return config["profile_path"] or DEFAULT.PROFILE_PATH

    def get_recent_user_count():
        return config["recent_users_count"] or 0

    def get_promotion_method():
        return config["promotion_method"] or None

    def get_password():
        return config["password"] or ""

    def get_password_google():
        return config["password_google"] or ""

    def get_password_twitter():
        return config["password_twitter"] or ""

    def get_download_path():
        return config["download_path"] or ""

    def get_drive_path():
        return config["drive_path"] or "root"

    def get_drive_root():
        return config["drive_root"] or "OnlySnarf"

    def get_users_path():
        return config["users_path"] or DEFAULT.USERS_PATH

    def get_config_path():
        return config["config_path"] or ""    

    def get_local_path():
        localPath = os.path.join(Settings.get_mount_path(), Settings.get_username())
        from pathlib import Path
        Path(localPath).mkdir(parents=True, exist_ok=True)
        for cat in Settings.get_categories():
            Path(os.path.join(localPath, cat)).mkdir(parents=True, exist_ok=True)
        return localPath

    def get_google_path():
        return config["google_path"] or ""

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
        return config["remote_host"] or ""

    def get_remote_port():
        return config["remote_port"] or DEFAULT.REMOTE_PORT

    def get_remote_username():
        return config["remote_username"] or ""

    def get_remote_password():
        return config["remote_password"] or ""

    def get_remote_browser_host():
        return config["remote_host"] or ""

    def get_remote_browser_port():
        return config["remote_browser_port"] or DEFAULT.BROWSER_PORT

    def get_secret_path():
        return config["client_secret"] or ""

    def get_profile_method():
        return config["profile_method"] or None

    def get_schedule():
        if str(config["schedule"]) != "None": return config["schedule"]
        if Settings.get_date():
            if Settings.get_time():
                config["schedule"] = "{} {}".format(Settings.get_date(), Settings.get_time())
            else:
                config["schedule"] = "{}".format(Settings.get_date())
        return config["schedule"]

    def get_tags():
        tags = config["tags"] or []
        tags = [n.strip() for n in tags]
        return tags

    def get_text():
        return config["text"] or None

    def get_time():
        return config["time"] or None

    def get_title():
        return config["title"] or None
        
    def get_skipped_users():
        return config["skipped_users"] or []
        
    def get_questions():
        return config["questions"] or []
        
    def get_upload_max():
        return config["upload_max"] or DEFAULT.IMAGE_LIMIT
        
    # def get_upload_max_messages():
        # return config["upload_max_messages"] or UPLOAD_MAX_MESSAGES
    def get_login_method():
        return config["login"] or ""
        
    def get_upload_max_duration():
        return config["upload_max_duration"] or DEFAULT.UPLOAD_MAX_DURATION # 6 hours

    # comma separated string of usernames
    def get_users():
        users = config["users"] or []
        users = [n.strip() for n in users]
        from .user import User
        users_ = []
        for user in users:
            # user = User({})
            user = User({"username":config["user"]})
            # setattr(user, "username", config["user"])
            from .driver import Driver
            setattr(user, "driver", Driver.get_driver())
            users_.append(user)
        return users_

    def get_user():
        if not config["user"]: return None
        from .user import User
        user = User({"username":config["user"]})
        # setattr(user, "username", config["user"])
        return user

    def get_email():
        return config["email"] or ""

    def get_username():
        return config["username"] or ""

    def get_username_google():
        return config["username_google"] or ""

    def get_username_twitter():
        return config["username_twitter"] or ""

    # def get_users_favorite():
    #     return config["users_favorite"] or []
        
    def get_verbosity():
        return config["verbose"] or 0

    def get_version():
        return pkg_resources.get_distribution("onlysnarf").version

    def get_performer_category():
        return Settings.PERFORMER_CATEGORY

    def set_performer_category(category):
        Settings.PERFORMER_CATEGORY = category

    def get_user_num():
        return config["users_read"] or DEFAULT.USER_LIMIT

    # Bools

    def is_confirm():
        return Settings.CONFIRM or False

    def is_cookies():
        return config["cookies"] or False

    def is_delete_empty():
        return config["delete_empty"] or False

    def is_prompt():
        return Settings.PROMPT or False

    def is_create_missing():
        return config["create_missing"] or False

    def is_debug():
        return config["debug"] or False

    def is_debug_delay():
        return config["debug_delay"] or False

    def is_delete():
        return config["delete_google"] or False

    def is_force_backup():
        return config["force_backup"] or False

    def is_force_upload():
        return config["force_upload"] or False

    def is_keep():
        return config["keep"] or False

    def is_prefer_local():
        return config["prefer_local"] or False
        
    def is_prefer_local_following():
        return config["prefer_local_following"] or False

    def is_save_users():
        return config["save_users"] or False
        
    def is_reduce():
        return config["enable_reduce"] or False
    
    def is_show_window():
        return config["show"] or False

    def is_split():
        return config["enable_split"] or False
        
    def is_trim():
        return config["enable_trim"] or False
        
    def is_tweeting():
        return config["tweeting"] or False
        
    def is_backup():
        return config["backup"] or False
        
    def is_skip_download():
        return config["skip_download"] or False
        
    def is_skip_upload():
        return config["skip_upload"] or False

    ##
    # Menu
    ##

    def confirm(text):
        try:
            if text == None: return False
            if list(text) == []: return False
            if str(text) == "": return False
            if not Settings.CONFIRM: return True
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
        if Settings.LAST_UPDATED_KEY:
            print("Updated: {} = {}".format(Settings.LAST_UPDATED_KEY, config[Settings.LAST_UPDATED_KEY.replace(" ","_").upper()]))
            print('\r')
        Settings.LAST_UPDATED_KEY = None

    def menu():
        skipList = ["action", "amount", "category", "categories", "cron", "input", "messages", "posts", "date", "duration", "expiration", "keywords", "limit", "months", "bykeyword", "notkeyword", "price", "config_path", "google_path", "client_secret", "questions", "schedule", "skipped_users", "tags", "text", "time", "title", "user", "users", "username", "password", "users_favorite"]
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
        answer = answer.replace(" ", "_").upper()
        Settings.set_setting(answer)

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
        question = {
            'type': 'input',
            'message': 'Email:',
            'name': 'email'
        }
        email = PyInquirer.prompt(question)["email"]
        Settings.set_email(email)
        return email

    def prompt_username():
        question = {
            'type': 'input',
            'message': 'Username:',
            'name': 'username'
        }
        username = PyInquirer.prompt(question)["username"]
        Settings.set_username(username)
        return username

    def prompt_password():
        question = {
            'type': 'password',
            'message': 'Password:',
            'name': 'password'
        }
        pw = PyInquirer.prompt(question)["password"]
        Settings.set_password(pw)
        return pw

    def prompt_username_google():
        question = {
            'type': 'input',
            'message': 'Google username:',
            'name': 'username'
        }
        username = PyInquirer.prompt(question)["username"]
        Settings.set_username_google(username)
        return username

    def prompt_password_google():
        question = {
            'type': 'password',
            'message': 'Google password:',
            'name': 'password'
        }
        pw = PyInquirer.prompt(question)["password"]
        Settings.set_password_google(pw)
        return pw

    def prompt_username_twitter():
        question = {
            'type': 'input',
            'message': 'Twitter username:',
            'name': 'username'
        }
        username = PyInquirer.prompt(question)["username"]
        Settings.set_username_twitter(username)
        return username

    def prompt_password_twitter():
        question = {
            'type': 'password',
            'message': 'Twitter password:',
            'name': 'password'
        }
        pw = PyInquirer.prompt(question)["password"]
        Settings.set_password_twitter(pw)
        return pw

    def read_session_data():
        Settings.maybe_print("reading local session")
        path_ = os.path.join(Settings.get_mount_path(), "session.json")
        Settings.dev_print("local session path: "+str(path_))
        id_ = None
        url = None
        try:
            with open(str(path_)) as json_file:  
                data = json.load(json_file)
                id_ = data['id']
                url = data['url']
            Settings.maybe_print("loaded local users")
        except Exception as e:
            Settings.dev_print(e)
        return (id_, url)

    def write_session_data(id_, url):
        Settings.maybe_print("writing local session")
        Settings.dev_print("saving session id: {}".format(id_))        
        Settings.dev_print("saving session url: {}".format(url))
        path_ = os.path.join(Settings.get_mount_path(), "session.json")
        Settings.dev_print("local session path: "+str(path_))
        data = {}
        data['id'] = id_
        data['url'] = url
        try:
            with open(str(path_), 'w') as outfile:  
                json.dump(data, outfile, indent=4, sort_keys=True)
        except FileNotFoundError:
            Settings.err_print("Missing Session File")
        except OSError:
            Settings.err_print("Missing Session Path")

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

    def set_confirm(value):
        Settings.CONFIRM = bool(value)

    def set_email(email):
        config["email"] = str(email)

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
        config["prefer_local"] = bool(buul)
    
    def set_prefer_local_following(buul):
        config["prefer_local_following"] = bool(buul)

    def set_prompt(value):
        Settings.PROMPT = bool(value)

    def set_setting(key):
        value = config[key]
        key = key.replace("_"," ").title()
        print("Current: {}".format(value))
        if str(value) == "True" or str(value) == "False":
            question = {
                'type': 'confirm',
                'name': 'setting',
                'message': "Toggle value?",
                # 'default': int(value)
            }
            answer = PyInquirer.prompt(question)["setting"]
            if not answer: return Settings.menu()
            if value: config[key.upper()] = False
            else: config[key.upper()] = True
        else:
            question = {
                'type': 'input',
                'name': 'setting',
                'message': "New value:",
                # 'default': int(value)
            }
            answer = PyInquirer.prompt(question)["setting"]
            if not Settings.confirm(answer): return Settings.menu()
            config[key.upper()] = answer
        Settings.LAST_UPDATED_KEY = key
        # return Settings.menu()

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




