
    ##
    # Getters
    ##

    def get_action():
        return CONFIG["action"]

    def get_actions():
        return DEFAULT.ACTIONS

    def get_amount():
        return CONFIG["amount"]

    def get_base_directory():
        return DEFAULT.ROOT_PATH

    def get_browser_type():
        return CONFIG["browser"]

    def get_months():
        return CONFIG["months"]

    def get_category():
        cat = CONFIG["category"]
        if str(cat) == "image": cat = "images"
        if str(cat) == "gallery": cat = "galleries"
        if str(cat) == "video": cat = "videos"
        if str(cat) == "performer": cat = "performers"
        return cat or None

    def get_categories():
        cats = []
        cats.extend(list(DEFAULT.CATEGORIES))
        cats.extend(list(CONFIG["categories"]))
        return cats

    

    def get_price():
        try: return CONFIG["price"]
        except Exception as e: pass
        return 0

    def get_price_minimum():
        return DEFAULT.PRICE_MINIMUM

    def get_price_maximum():
        return DEFAULT.PRICE_MAXIMUM

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
        return CONFIG["download_limit"] or DEFAULT.IMAGE_LIMIT

    def get_duration():
        try: return CONFIG["duration"]
        except Exception as e: pass
        return None

    def get_promo_duration():
        try: return CONFIG["duration_promo"]
        except Exception as e: pass
        return None
        
    def get_duration_allowed():
        return DEFAULT.DURATION_ALLOWED or []
        
    def get_duration_promo_allowed():
        return DEFAULT.PROMOTION_DURATION_ALLOWED or []

    def get_expiration():
        try: return CONFIG["expiration"]
        except Exception as e: pass
        return DEFAULT.EXPIRATION_NONE

    def get_promo_expiration():
        return CONFIG["promotion_expiration"]

    def get_input():
        # fix pytest bug from 4.4.9
        files = []
        for file_path in CONFIG["input"]:
            if ".py" not in str(file_path):
                files.append[file_path]
        return set(files)

    def get_input_as_files():
        if Settings.FILES: return Settings.FILES
        from ..classes.file import File
        files = []
        try:
            _input = CONFIG["input"]
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
        return CONFIG["sort"] or "random"

    def get_phone_number():
        try:
            return CONFIG["phone"]
        except Exception as e:
            Settings.err_print("missing phone number!")
        return None

    def get_profile_path():
        try: return CONFIG["path_profile"]
        except Exception as e: pass
        return DEFAULT.PROFILE_PATH

    def get_recent_user_count():
        return CONFIG["recent_users_count"] or 0
    
    def get_promotion_limit():
        return CONFIG["promotion_limit"] or None

    def get_promotion_method():
        return CONFIG["promotion_method"] or None

    def get_password(username=None):
        try:
            if not username: username = Settings.get_username()
            return Settings.get_user_CONFIG(username)["onlyfans_password"]
        except Exception as e: pass
        return ""

    def get_password_google(username=None):
        try:
            if not username: username = Settings.get_username()
            return Settings.get_user_CONFIG(username)["google_password"]
        except Exception as e: pass
        return ""

    def get_password_twitter(username=None):
        try: 
            if not username: username = Settings.get_username()
            return Settings.get_user_CONFIG(username)["twitter_password"]
        except Exception as e: pass
        return ""

    def get_download_path():
        try: return CONFIG["path_download"]
        except Exception as e: pass
        return DEFAULT.DOWNLOAD_PATH

    def get_users_path():
        try: return CONFIG["path_users"]
        except Exception as e: pass
        return DEFAULT.USERS_PATH

    def get_CONFIG_path():
        try: return CONFIG["path_CONFIG"]   
        except Exception as e: pass
        return DEFAULT.CONFIG_PATH

    def get_local_path():
        localPath = os.path.join(Settings.get_root_path(), Settings.get_username())
        Path(localPath).mkdir(parents=True, exist_ok=True)
        for cat in Settings.get_categories():
            Path(os.path.join(localPath, cat)).mkdir(parents=True, exist_ok=True)
        return localPath

    def get_reconnect_id():
        return CONFIG["session_id"] or ""

    def get_reconnect_url():
        return CONFIG["session_url"] or ""

    def get_remote_host():
        return CONFIG["remote_host"] or DEFAULT.REMOTE_HOST

    def get_remote_port():
        return CONFIG["remote_port"] or DEFAULT.REMOTE_PORT

    def get_remote_path():
        return CONFIG["remote_path"] or DEFAULT.REMOTE_PATH

    def get_remote_username():
        return CONFIG["remote_username"] or ""

    def get_remote_password():
        return CONFIG["remote_password"] or ""

    def get_profile_method():
        return CONFIG["profile_method"] or None

    # TODO: finish moving these to Schedule class
    # def get_date():
    #     try:
    #         CONFIG["date"] = Settings.format_date(CONFIG["date"])
    #         if str(CONFIG["date"]) == DEFAULT.DATE and str(CONFIG["schedule"]) != DEFAULT.SCHEDULE and str(CONFIG["schedule"] != "None"):
    #             if isinstance(CONFIG["schedule"], str):
    #                 CONFIG["date"] = datetime.strptime(CONFIG["schedule"], DEFAULT.SCHEDULE_FORMAT).date().strftime(DEFAULT.DATE_FORMAT)
    #             else:
    #                 CONFIG["date"] = CONFIG["schedule"].date().strftime(DEFAULT.DATE_FORMAT)
    #             CONFIG["date"] = datetime.strptime(str(CONFIG["date"]), DEFAULT.DATE_FORMAT)
    #         else:
    #             CONFIG["date"] = datetime.strptime(str(CONFIG["date"]), DEFAULT.DATE_FORMAT)
    #         CONFIG["date"] = CONFIG["date"].strftime(DEFAULT.DATE_FORMAT)    
    #     except Exception as e:
    #         CONFIG["date"] = datetime.strptime(DEFAULT.DATE, DEFAULT.DATE_FORMAT)
    #     Settings.maybe_print("date (settings): {}".format(str(CONFIG["date"])[:10]))
    #     return str(CONFIG["date"])[:10]

    # def get_time():
    #     try:
    #         CONFIG["time"] = Settings.format_time(CONFIG["time"])        
    #         if (str(CONFIG["time"]) == DEFAULT.TIME or str(CONFIG["time"]) == DEFAULT.TIME_NONE) and str(CONFIG["schedule"]) != DEFAULT.SCHEDULE and str(CONFIG["schedule"]) != "None":
    #             Settings.dev_print("time from schedule")
    #             date = datetime.strptime(str(CONFIG["schedule"]), DEFAULT.SCHEDULE_FORMAT)
    #             CONFIG["time"] = datetime.strptime(str(date.time().strftime(DEFAULT.TIME_FORMAT)), DEFAULT.TIME_FORMAT)
    #         else:
    #             Settings.dev_print("time from CONFIG")
    #             CONFIG["time"] = datetime.strptime(str(CONFIG["time"]), DEFAULT.TIME_FORMAT)
    #         CONFIG["time"] = CONFIG["time"].strftime(DEFAULT.TIME_FORMAT)
    #     except Exception as e:
    #         CONFIG["time"] = datetime.strptime(DEFAULT.TIME, DEFAULT.TIME_FORMAT).strftime(DEFAULT.TIME_FORMAT)
    #     Settings.maybe_print("time (settings): {}".format(str(CONFIG["time"])[:9]))
    #     return str(CONFIG["time"])[:9]

    # def get_schedule():
    #     schedule = ""
    #     try:
    #         schedule = CONFIG["schedule"]
    #         if str(schedule) == "None": schedule = DEFAULT.SCHEDULE
    #         if str(schedule) == DEFAULT.SCHEDULE:
    #             schedule = datetime.strptime(schedule, DEFAULT.SCHEDULE_FORMAT).strftime(DEFAULT.SCHEDULE_FORMAT)
    #         elif not isinstance(schedule, str):
    #             schedule = schedule.strftime(DEFAULT.SCHEDULE_FORMAT)
    #     except Exception as e:
    #         schedule = datetime.strptime("{} {}".format(Settings.get_date(), Settings.get_time()), DEFAULT.SCHEDULE_FORMAT).strftime(DEFAULT.SCHEDULE_FORMAT)
    #     Settings.maybe_print("schedule (settings): {}".format(schedule))
    #     return str(schedule)[:20] # must be less than 19 characters

    def get_title():
        return CONFIG["title"] or ""
        
    def get_skipped_users():
        return CONFIG["skipped_users"] or []
        
    def get_upload_max():
        try:
            return CONFIG["upload_max"]
        except Exception as e:
            pass
        return DEFAULT.IMAGE_LIMIT
        
    # def get_upload_max_messages():
        # return CONFIG["upload_max_messages"] or UPLOAD_MAX_MESSAGES

    def get_login_method():
        try: return CONFIG["login"]
        except Exception as e: pass
        return "auto"
        
    def get_upload_max_duration():
        return CONFIG["upload_max_duration"] or DEFAULT.UPLOAD_MAX_DURATION # 1 hour

    # comma separated string of usernames
    def get_users():
        from ..classes.user import User
        if str(CONFIG["user"]) != "None":
            if str(CONFIG["user"]) == "all":
                CONFIG["users"].extend([user.username for user in User.get_all_users()])
            elif str(CONFIG["user"]) == "recent":
                CONFIG["users"].extend([user.username for user in User.get_recent_users()])
            elif str(CONFIG["user"]) == "favorite":
                CONFIG["users"].extend([user.username for user in User.get_favorite_users()])
            elif str(CONFIG["user"]) == "random":
                CONFIG["users"] = [User.get_random_user().username]
            else: CONFIG["users"].append(CONFIG["user"])
        users = []
        for user in [n.strip() for n in CONFIG["users"]]:
            if isinstance(user, User): pass
            elif isinstance(user, str): user = User({"username":user})
            # BUG (potential): might bug out if the username is for whatever reason all numbers
            elif isinstance(user, int): user = User({"id":user})
            users.append(user)
        return users

    def get_user():
        return Settings.get_users()[0]

    def get_user_CONFIGs():
        # load CONFIGs from .onlysnarf or baseDir
        pass

    def get_user_CONFIG(username="default"):
        import CONFIGparser
        CONFIG_file = CONFIGparser.ConfigParser()
        # strip email
        if "@" in username: username = username[0 : username.index("@")]
        username = username.replace(".conf", "") # filename formatting
        Settings.dev_print("retrieving user CONFIG: {}".format(username))
        Settings.dev_print(os.path.join(Settings.get_base_directory(), "conf/users", username+".conf"))
        CONFIG_file.read(os.path.join(Settings.get_base_directory(), "conf/users", username+".conf"))
        userConfig = {}
        for section in CONFIG_file.sections():
            # Settings.dev_print(section)
            for key in CONFIG_file[section]:
                # Settings.dev_print(section, key, CONFIG_file[section][key].strip("\""))
                userConfig[section.lower()+"_"+key.lower()] = CONFIG_file[section][key].strip("\"")
        # Settings.dev_print(userConfig)
        return userConfig

    def get_user_CONFIG_path(username="default"):
        if ".conf" not in str(username): username = username+".conf"
        return os.path.join(Settings.get_base_directory(), "conf/users", username)

    def get_username():
        return CONFIG["username"] or "default"

    def get_username_onlyfans(username=None):
        try:
            if not username: username = Settings.get_username()
            return Settings.get_user_CONFIG(username)["onlyfans_username"]
        except Exception as e: pass
        return ""

    def get_username_google(username=None):
        try:
            if not username: username = Settings.get_username()
            return Settings.get_user_CONFIG(username)["google_username"]
        except Exception as e: pass
        return ""            

    def get_username_twitter(username=None):
        try:
            if not username: username = Settings.get_username()
            return Settings.get_user_CONFIG(username)["twitter_username"]
        except Exception as e: pass
        return ""

    def get_remote_browser_host():
        return CONFIG["remote_browser_host"]

    def get_remote_browser_port():
        return CONFIG["remote_browser_port"]

    ## TODO
    # add arg -profile
    # add method for reading CONFIG profiles from conf/users

    def get_profile():
        pass

    def select_profile():
        pass

    # def get_users_favorite():
    #     return CONFIG["users_favorite"] or []
        
    def get_verbosity():
        return CONFIG["verbose"] or 0

    def get_version():
        return pkg_resources.get_distribution("onlysnarf").version

    def get_user_num():
        return CONFIG["users_read"] or DEFAULT.USER_LIMIT
