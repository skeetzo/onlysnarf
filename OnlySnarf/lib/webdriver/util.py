import os
import json
import logging
# from selenium.webdriver.remote.remote_connection import LOGGER as SeleniumLogger
# from webdriver_manager.core.logger import set_logger

from .. import CONFIG, DEFAULT

def configure_logging():

    # set_logger(logging.getLogger("root"))
    
    # logging.getLogger("urllib3.connectionpool").setLevel(logging.ERROR)

    if int(CONFIG["verbose"]) >= 2:
        # SeleniumLogger.setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.WARNING)

    if not CONFIG["debug_selenium"]:
        # SeleniumLogger.setLevel(logging.ERROR)
        logging.getLogger("selenium.webdriver.common.service").setLevel(logging.ERROR)
        logging.getLogger("WDM").setLevel(logging.ERROR)
        logging.getLogger("urllib3").setLevel(logging.ERROR)
        logging.getLogger("requests").setLevel(logging.ERROR)
        logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.ERROR)

def read_session_data(browserType):
    logging.debug("reading local session...")
    path = os.path.join(DEFAULT.ROOT_PATH, f"session-{browserType}.json")
    logging.debug("local session path: "+str(path))
    try:
        with open(str(path)) as json_file:  
            data = json.load(json_file)
            return data['id'], data['url']
        logging.debug("loaded local users!")
    except Exception as e:
        logging.debug(e)
    return None, None

def write_session_data(browserType, session_id, session_url):
    logging.debug("writing local session...")
    logging.debug("saving session id: {}".format(session_id))        
    logging.debug("saving session url: {}".format(session_url))
    path = os.path.join(DEFAULT.ROOT_PATH, f"session-{browserType}.json")
    logging.debug("local session path: "+str(path))
    data = {}
    data['id'] = session_id
    data['url'] = session_url
    try:
        with open(str(path), 'w') as outfile:  
            json.dump(data, outfile, indent=4, sort_keys=True)
        logging.debug("saved session data!")
    except FileNotFoundError:
        logging.error("missing session file!")
    except OSError:
        logging.error("missing session path!")