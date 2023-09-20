import os
import json
import logging
logger = logging.getLogger(__name__)
# from selenium.webdriver.remote.remote_connection import LOGGER as SeleniumLogger
# from webdriver_manager.core.logger import set_logger

from .. import CONFIG, DEFAULT

def configure_logging():

    # set_logger(logging.getLogger("root"))
    
    # logging.getLogger("urllib3.connectionpool").setLevel(logging.ERROR)

    if int(CONFIG.get("verbose", 0)) >= 2:
        # SeleniumLogger.setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.WARNING)

    if not CONFIG.get("debug_selenium", False):
        # SeleniumLogger.setLevel(logging.ERROR)
        logging.getLogger("selenium.webdriver.common.service").setLevel(logging.ERROR)
        logging.getLogger("WDM").setLevel(logging.ERROR)
        logging.getLogger("urllib3").setLevel(logging.ERROR)
        logging.getLogger("requests").setLevel(logging.ERROR)
        logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.ERROR)

def read_session_data(browserType):
    logger.debug(f"reading local session for {browserType}...")
    path = os.path.join(DEFAULT.ROOT_PATH, f"session.json")
    logger.debug("local session path: "+str(path))
    try:
        with open(str(path)) as json_file:  
            data = json.load(json_file)
            browser_data = data.get(browserType, {'id':'','url':''})
            return browser_data['id'], browser_data['url']
    except Exception as e:
        logger.error(e)
    return "", ""

def write_session_data(browserType, session_id, session_url):
    logger.debug(f"writing local session for {browserType}...")
    logger.debug("saving session id: {}".format(session_id))        
    logger.debug("saving session url: {}".format(session_url))
    path = os.path.join(DEFAULT.ROOT_PATH, f"session.json")
    logger.debug("local session path: "+str(path))
    
    try:
        data = {}
        browser_data = {}
        try:
            with open(str(path)) as json_file:  
                data = json.load(json_file)
                browser_data = data.get(browserType, {'id':'','url':''})
        except FileNotFoundError:
            logger.debug(f"creating new session file for {browserType}...")
            data = {browserType:{'id':'','url':''}}

        browser_data['id'] = session_id
        browser_data['url'] = session_url
        data[browserType] = browser_data

        with open(str(path), 'w') as outfile:  
            json.dump(data, outfile, indent=4, sort_keys=True)

        logger.debug("saved session data!")
    except OSError:
        logger.error("missing session path!")
    except Exception as e:
        logger.error(e)