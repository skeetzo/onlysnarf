import pkg_resources
import time
import os, json, sys
from datetime import datetime
from pathlib import Path
##
from .colorize import colorize
from .config import config
from . import defaults as DEFAULT
from .validators import valid_schedule, valid_time
from .logger import logging
log = logging.getLogger('onlysnarf')

class Settings:
    
    LAST_UPDATED_KEY = None
    CATEGORY = None
    FILES = None
    PERFORMER_CATEGORY = None

    #####################
    ##### Functions #####
    #####################

    def debug_delay_check():
        if str(Settings.is_debug()) == "True" and str(Settings.is_debug_delay()) == "True":
            Settings.dev_print("napping...")
            time.sleep(10)

    ##
    # Print
    ##

    def print(text):
        if int(config["verbose"]) >= 0:
            log.info(text)

    def print_same_line(text):
        sys.stdout.write('\r')
        sys.stdout.flush()
        sys.stdout.write(text)
        sys.stdout.flush()

    def maybe_print(text):
        if int(config["verbose"]) >= 1 or str(os.environ.get("ENV")) == "test":
            log.debug(text)

    def dev_print(text):
        if int(config["verbose"]) >= 2 or str(os.environ.get("ENV")) == "test":
            log.debug(text)

    def err_print(error):
        log.error(error)

    def warn_print(error):
        log.warning(error)

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

    def header():
        Settings.print("### SETTINGS ###")
        Settings.print("...")
        Settings.print("...")
        Settings.print("...")

    def menu():
        Settings.print("### SETTINGS MENU ###")
        Settings.print("...")
        Settings.print("...")
        Settings.print("...")

    ##
    # Getters
    ##

    def get_action():
        return config["action"]

    def get_actions():
        return DEFAULT.ACTIONS

    def get_amount():
        return config["amount"]

    def get_base_directory():
        return DEFAULT.ROOT_PATH

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

    def get_categories():
        cats = []
        cats.extend(list(DEFAULT.CATEGORIES))
        cats.extend(list(config["categories"]))
        return cats

    def get_cookies_path():
        # return os.path.join(Settings.get_base_directory(), Settings.get_username(), "cookies.pkl")
        return os.path.join(Settings.get_base_directory(), "cookies.pkl")

    def get_price():
        try: return config["price"]
        except Exception as e: pass
        return 0

    def get_price_minimum():
        return DEFAULT.PRICE_MINIMUM

    def get_price_maximum():
        return DEFAULT.PRICE_MAXIMUM

    def get_date():
        try:
            config["date"] = Settings.format_date(config["date"])
            if str(config["date"]) == DEFAULT.DATE and str(config["schedule"]) != DEFAULT.SCHEDULE and str(config["schedule"] != "None"):
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
        except Exception as e:
            pass
        return datetime.strptime(DEFAULT.DATE, DEFAULT.DATE_FORMAT)

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

    def get_duration():
        try: return config["duration"]
        except Exception as e: pass
        return None

    def get_promo_duration():
        try: return config["duration_promo"]
        except Exception as e: pass
        return None
        
    def get_duration_allowed():
        return DEFAULT.DURATION_ALLOWED or []
        
    def get_duration_promo_allowed():
        return DEFAULT.PROMOTION_DURATION_ALLOWED or []

    def get_expiration():
        try: return config["expiration"]
        except Exception as e: pass
        return DEFAULT.EXPIRATION_NONE

    def get_promo_expiration():
        return config["promotion_expiration"]

    def get_input():
        # fix pytest bug from 4.4.9
        files = []
        for file_path in config["input"]:
            if ".py" not in str(file_path):
                files.append[file_path]
        return set(files)

    def get_input_as_files():
        if Settings.FILES: return Settings.FILES
        from ..classes.file import File
        files = []
        try:
            _input = config["input"]
            if isinstance(_input, list):
                for file_path in _input:
                    file = File()
                    setattr(file, "path", file_path)
                    files.append(file)
            else:
                file = File()
                setattr(file, "path", _input)
                files.append(file)
        except Exception as e:
            pass
        Settings.FILES = files
        return files
        
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
        return DEFAULT.ROOT_PATH

    def get_sort_method():
        return config["sort"] or "random"

    def get_performers():
        try:
            performers = config["performers"] or []
            performers = [n.strip() for n in performers]
            return performers
        except Exception as e: pass
        return []

    def get_profile_path():
        try: return config["path_profile"]
        except Exception as e: pass
        return DEFAULT.PROFILE_PATH

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
        try: return config["path_download"]
        except Exception as e: pass
        return DEFAULT.DOWNLOAD_PATH

    def get_users_path():
        try: return config["path_users"]
        except Exception as e: pass
        return DEFAULT.USERS_PATH

    def get_config_path():
        try: return config["path_config"]   
        except Exception as e: pass
        return DEFAULT.CONFIG_PATH

    def get_local_path():
        localPath = os.path.join(Settings.get_root_path(), Settings.get_username())
        from pathlib import Path
        Path(localPath).mkdir(parents=True, exist_ok=True)
        for cat in Settings.get_categories():
            Path(os.path.join(localPath, cat)).mkdir(parents=True, exist_ok=True)
        return localPath

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
        schedule = ""
        try:
            schedule = config["schedule"]
            if str(schedule) == "None": schedule = DEFAULT.SCHEDULE
            if str(schedule) == DEFAULT.SCHEDULE:
                schedule = datetime.strptime(schedule, DEFAULT.SCHEDULE_FORMAT).strftime(DEFAULT.SCHEDULE_FORMAT)
            elif not isinstance(schedule, str):
                schedule = schedule.strftime(DEFAULT.SCHEDULE_FORMAT)
            Settings.maybe_print("schedule (settings): {}".format(schedule))
            return schedule
        except Exception as e:
            pass
        return datetime.strptime("{} {}".format(Settings.get_date(), Settings.get_time()), DEFAULT.SCHEDULE_FORMAT).strftime(DEFAULT.SCHEDULE_FORMAT)

    def get_keywords():
        keywords = []
        try:
            keywords = config["keywords"]
            keywords = [n.strip() for n in keywords]
        except Exception as e:
            pass
            # Settings.err_print(e)
        return keywords

    def get_text():
        return config["text"] or ""

    def get_time():
        try:
            config["time"] = Settings.format_time(config["time"])        
            if (str(config["time"]) == DEFAULT.TIME or str(config["time"]) == DEFAULT.TIME_NONE) and str(config["schedule"]) != DEFAULT.SCHEDULE and str(config["schedule"]) != "None":
                Settings.dev_print("time from schedule")
                date = datetime.strptime(str(config["schedule"]), DEFAULT.SCHEDULE_FORMAT)
                config["time"] = datetime.strptime(str(date.time().strftime(DEFAULT.TIME_FORMAT)), DEFAULT.TIME_FORMAT)
            else:
                Settings.dev_print("time from config")
                config["time"] = datetime.strptime(str(config["time"]), DEFAULT.TIME_FORMAT)
            config["time"] = config["time"].strftime(DEFAULT.TIME_FORMAT)
            Settings.maybe_print("time (settings): {}".format(config["time"]))
            return config["time"]
        except Exception as e:
            pass
        return datetime.strptime(DEFAULT.TIME, DEFAULT.TIME_FORMAT).strftime(DEFAULT.TIME_FORMAT)

    def get_title():
        return config["title"] or ""
        
    def get_skipped_users():
        return config["skipped_users"] or []
        
    def get_questions():
        try:
            return config["questions"]
        except Exception as e:
            pass
        return []
        
    def get_upload_max():
        try:
            return config["upload_max"]
        except Exception as e:
            pass
        return DEFAULT.IMAGE_LIMIT
        
    # def get_upload_max_messages():
        # return config["upload_max_messages"] or UPLOAD_MAX_MESSAGES

    def get_login_method():
        try: return config["login"]
        except Exception as e: pass
        return "auto"
        
    def get_upload_max_duration():
        return config["upload_max_duration"] or DEFAULT.UPLOAD_MAX_DURATION # 1 hour

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
                config["users"] = [User.get_random_user().username]
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

    def get_user_configs():
        # load configs from .onlysnarf or baseDir
        pass

    def get_user_config(username="default"):
        import configparser
        config_file = configparser.ConfigParser()
        # strip email
        if "@" in username: username = username[0 : username.index("@")]
        Settings.dev_print("retrieving user config: {}".format(username))
        Settings.dev_print(os.path.join(Settings.get_base_directory(), "conf", "users", username+".conf"))
        config_file.read(os.path.join(Settings.get_base_directory(), "conf", "users", username+".conf"))
        userConfig = {}
        for section in config_file.sections():
            # Settings.dev_print(section)
            for key in config_file[section]:
                # Settings.dev_print(section, key, config_file[section][key].strip("\""))
                userConfig[section.lower()+"_"+key.lower()] = config_file[section][key].strip("\"")
        # Settings.dev_print(userConfig)
        return userConfig

    def get_username():
        return config["username"] or "default"

    def get_username_onlyfans():
        try:
            return Settings.get_user_config(Settings.get_username())["onlyfans_username"]
        except Exception as e:
            Settings.err_print(e)
        return ""

    def get_username_google():
        try:
            return Settings.get_user_config(Settings.get_username())["google_username"]
        except Exception as e:
            Settings.err_print(e)
        return ""            

    def get_username_twitter():
        try:
            return Settings.get_user_config(Settings.get_username())["twitter_username"]
        except Exception as e:
            Settings.err_print(e)
        return ""

    def get_remote_browser_host():
        return config["remote_browser_host"]

    def get_remote_browser_port():
        return config["remote_browser_port"]

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
        return config["confirm"]

    def is_cookies():
        return config["cookies"]

    def is_delete():
        return config["delete"]

    def is_delete_empty():
        return config["delete_empty"]

    def is_debug(process=None):
        if process == "firefox": return config["debug_firefox"]
        elif process == "chrome": return config["debug_chrome"]
        elif process == "selenium": return config["debug_selenium"]
        elif process == "cookies": return config["debug_cookies"]
        # elif process == "tests": return 
        return config["debug"]

    def is_debug_delay():
        return config["debug_delay"]

    def is_force_upload():
        return config["force_upload"]

    def is_keep():
        return config["keep"]

    def is_prefer_local():
        return config["prefer_local"]
        
    def is_prefer_local_following():
        return config["prefer_local_following"]

    def is_save_users():
        return config["save_users"]
        
    def is_reduce():
        return config["reduce"]
    
    def is_show_window():
        return config["show"]
        
    def is_tweeting():
        return config["tweeting"]
        
    def is_backup():
        return config["backup"]
        
    def is_skip_download():
        return config["skip_download"]
        
    def is_skip_upload():
        return config["skip_upload"]

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
            pass
            # config["confirm"] = False
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