import configparser
import logging
logger = logging.getLogger(__name__)
import os

from .config import CONFIG
from . import defaults as DEFAULT

def get_user_config(username="default"):
    config_file = configparser.ConfigParser()
    # strip email
    if "@" in username: username = username[0 : username.index("@")]
    username = username.replace(".conf", "") # filename formatting
    logger.debug("retrieving user config: {}".format(username))
    logger.debug(os.path.join(DEFAULT.ROOT_PATH, "conf/users", username+".conf"))
    config_file.read(os.path.join(DEFAULT.ROOT_PATH, "conf/users", username+".conf"))
    userConfig = {}
    for section in config_file.sections():
        # logger.debug(section)
        for key in config_file[section]:
            # logger.debug(section, key, config_file[section][key].strip("\""))
            userConfig[section.lower()+"_"+key.lower()] = config_file[section][key].strip("\"")
    # logger.debug(userConfig)
    return userConfig

def get_user_config_path(username="default"):
    if ".conf" not in str(username): username = username+".conf"
    return os.path.join(DEFAULT.ROOT_PATH, "conf/users", username)

def get_username_onlyfans(username="default"):
    try:
        if not username: username = CONFIG["username"]
        username = get_user_config(username)["onlyfans_username"]
        if username == DEFAULT.USERNAME: return ""
    except Exception as e: pass
    return username

def get_username_google(username="default"):
    try:
        if not username: username = CONFIG["username"]
        username = get_user_config(username)["google_username"]
        if username == DEFAULT.GOOGLE_USERNAME: return ""
    except Exception as e: pass
    return username           

def get_username_twitter(username="default"):
    try:
        if not username: username = CONFIG["username"]
        username = get_user_config(username)["twitter_username"]
        if username == DEFAULT.TWITTER_USERNAME: return ""
    except Exception as e: pass
    return username

def get_password(username="default"):
    try:
        if not username: username = CONFIG["username"]
        username = get_user_config(username)["onlyfans_password"]
        if username == DEFAULT.PASSWORD: return ""
    except Exception as e: pass
    return username

def get_password_google(username="default"):
    try:
        if not username: username = CONFIG["username"]
        username = get_user_config(username)["google_password"]
        if username == DEFAULT.GOOGLE_PASSWORD: return ""
    except Exception as e: pass
    return username

def get_password_twitter(username="default"):
    try:
        if not username: username = CONFIG["username"]
        username = get_user_config(username)["twitter_password"]
        if username == DEFAULT.TWITTER_PASSWORD: return ""
    except Exception as e: pass
    return username
