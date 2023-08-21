import json
import logging
import os
from selenium.webdriver.remote.remote_connection import LOGGER as SeleniumLogger

from ..util.settings import Settings

def enable_logging():
    if str(Settings.is_debug("selenium")) == "False":
        SeleniumLogger.setLevel(logging.ERROR)
        logging.getLogger("urllib3").setLevel(logging.ERROR)
        logging.getLogger("requests").setLevel(logging.ERROR)
        logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.ERROR)
        if int(Settings.get_verbosity()) >= 2:
            SeleniumLogger.setLevel(logging.WARNING)
            logging.getLogger("urllib3").setLevel(logging.WARNING)
            logging.getLogger("requests").setLevel(logging.WARNING)
            logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.WARNING)


def read_session_data():
    Settings.maybe_print("reading local session...")
    path = os.path.join(Settings.get_base_directory(), "session.json")
    Settings.dev_print("local session path: "+str(path))
    try:
        with open(str(path)) as json_file:  
            data = json.load(json_file)
            return data['id'], data['url']
        Settings.maybe_print("loaded local users!")
    except Exception as e:
        Settings.dev_print(e)
    return None, None

def write_session_data(session_id, session_url):
    Settings.maybe_print("writing local session...")
    Settings.dev_print("saving session id: {}".format(session_id))        
    Settings.dev_print("saving session url: {}".format(session_url))
    path = os.path.join(Settings.get_base_directory(), "session.json")
    Settings.dev_print("local session path: "+str(path))
    data = {}
    data['id'] = session_id
    data['url'] = session_url
    try:
        with open(str(path), 'w') as outfile:  
            json.dump(data, outfile, indent=4, sort_keys=True)
        Settings.maybe_print("saved session data!")
    except FileNotFoundError:
        Settings.err_print("missing session file!")
    except OSError:
        Settings.err_print("missing session path!")