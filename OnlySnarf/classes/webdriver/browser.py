import logging
import os
# import shutil
import platform
## selenium
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.file_detector import LocalFileDetector
## webdriver_manager
# brave
# chrome
# chromium
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.core.utils import ChromeType
# firefox
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
# ie
from selenium.webdriver.ie.service import Service as IEService
from webdriver_manager.microsoft import IEDriverManager
# edge
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
# from msedge.selenium_tools import Edge, EdgeOptions
# opera
from webdriver_manager.opera import OperaDriverManager

from .. import CONFIG, DEFAULT
from .util import configure_logging, read_session_data

def create_browser(browserType):
    """
    Spawns a browser according to args.

    Browser options can be: auto, chrome, firefox, remote

    Parameters
    ----------
    browserType : str
        The configured browser type to use

    Returns
    -------
    Selenium.WebDriver
        The created browser object

    """


    print(CONFIG)
    browser = None
    logging.info("spawning web browser...")

    configure_logging()

    if "auto" in browserType:
        browser = attempt_reconnect()
        if not browser: browser = attempt_brave()
        if not browser: browser = attempt_chrome()
        if not browser: browser = attempt_chromium()
        if not browser: browser = attempt_edge()
        if not browser: browser = attempt_firefox()
        if not browser: browser = attempt_ie()
        if not browser: browser = attempt_opera()
    elif "brave" in browserType:
        browser = attempt_brave()
    elif "chrome" in browserType:
        browser = attempt_chrome()
    elif "chromium" in browserType:
        browser = attempt_chromium()
    elif "edge" in browserType:
        browser = attempt_edge()
    elif "firefox" in browserType:
        browser = attempt_firefox()
    elif "ie" in browserType:
        browser = attempt_ie()
    elif "opera" in browserType:
        browser = attempt_opera()
    elif "remote" in browserType:
        browser = attempt_remote()

    if not browser:
        logging.error("unable to spawn a web browser!")
        os._exit(1)

    browser.implicitly_wait(30) # seconds
    browser.set_page_load_timeout(1200)
    browser.maximize_window()
    browser.file_detector = LocalFileDetector() # for uploading via remote sessions
    if not CONFIG["show"]:
        logging.info("headless browser spawned successfully!")
    else:
        logging.info("browser spawned successfully!")
    return browser

################################################################################################
################################################################################################
################################################################################################

def add_options(options):
    options.add_argument("--no-sandbox") # Bypass OS security model
    if not CONFIG["show"]:
        options.add_argument('--headless')
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")

    options.add_argument("enable-automation")
    # options.add_argument("--disable-infobars")

    # if os.name == 'nt':
        # options.add_argument(r"--user-data-dir=C:\Users\brain\AppData\Local\Google\Chrome\User Data")
    # else:
    options.add_argument('--profile-directory=Default')

    if str(platform.processor()) == "aarch64": # raspi
        options.add_argument("--user-data-dir=/home/ubuntu/selenium") # do not disable, required for cookies to work 
    else:
        options.add_argument("--user-data-dir="+os.path.join(DEFAULT.ROOT_PATH,"tmp","selenium")) # do not disable, required for cookies to work 

    options.add_argument("--disable-browser-side-navigation") # https://stackoverflow.com/a/49123152/1689770

    # options.add_argument("--allow-insecure-localhost")            
    # possibly linux only
    # options.add_argument('disable-notifications')
    # https://stackoverflow.com/questions/50642308/webdriverexception-unknown-error-devtoolsactiveport-file-doesnt-exist-while-t
    # options.add_arguments("start-maximized"); // open Browser in maximized mode
    # options.add_argument("--window-size=1920,1080")
    # options.add_argument("--disable-crash-reporter")
    # options.add_argument("--disable-infobars")
    # options.add_argument("--disable-in-process-stack-traces")
    # options.add_argument("--disable-logging")
    # options.add_argument("--log-level=3")
    # options.add_argument("--output=/dev/null")
    # TODO: to be added to list of removed (if not truly needed by then)
    # options.add_argument('--disable-software-rasterizer')
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument("--remote-debugging-address=localhost")    
    # options.add_argument("--remote-debugging-port=9223")

def browser_error(err, browserName):
    logging.warning("unable to launch {}!".format(browserName))
    logging.debug(err)

def attempt_chrome():
    browserAttempt = None
    try:
        logging.debug("attempting Chrome web browser...")
        # raspberrypi arm processors don't work with webdriver manager
        # linux = x86_64
        # rpi = aarch64
        processor = platform.processor()
        logging.debug("cpu processor: {}".format(processor))
        if str(processor) == "aarch64":
            # TODO: add file check for chromedriver w/ reminder warning for rpi install requirement
            browserAttempt = webdriver.Chrome(service=ChromeService('/usr/bin/chromedriver'), options=chrome_options())
        else:
            browserAttempt = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options())
            # browserAttempt = webdriver.Chrome(options=chrome_options())
        logging.info("browser created - Chrome")        
    except Exception as e:
        browser_error(e, "chrome")
    return browserAttempt

def attempt_brave():
    browserAttempt = None
    try:
        logging.debug("attempting Brave web browser...")
        browserAttempt = webdriver.Chrome(service=ChromeService(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()), options=chrome_options())
        logging.info("browser created - Brave")
    except Exception as e:
        browser_error(e, "brave")
    return browserAttempt

def attempt_chromium():
    browserAttempt = None
    try:
        logging.debug("attempting Chromium web browser...")
        browserAttempt = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), options=chrome_options())
        logging.info("browser created - Chromium")        
    except Exception as e:
        browser_error(e, "chromium")
    return browserAttempt

# TODO: debug
def attempt_edge():
    browserAttempt = None
    try:
        logging.debug("attempting Edge web browser...")
        # browserAttempt = Edge(executable_path=options.binary_location, options=edge_options())
        browserAttempt = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
        logging.info("browser created - Edge")
    except Exception as e:
        browser_error(e, "edge")
    return browserAttempt

def attempt_firefox():
    browserAttempt = None
    # firefox needs non root
    if os.geteuid() == 0:
        logging.info("You must run `onlysnarf` as non-root for Firefox to work correctly!")
        return False
    try:
        logging.debug("attempting Firefox web browser...")
        browserAttempt = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options())
        logging.info("browser created - Firefox")
    except Exception as e:
        browser_error(e, "firefox")
    return browserAttempt

# TODO: debug
def attempt_ie():
    browserAttempt = None
    try:
        logging.debug("attempting IE web browser...")
        # driver_path = IEDriverManager().install()
        # os.chmod(driver_path, 0o755)
        # browserAttempt = webdriver.Ie(executable_path=IEService(driver_path))
        browserAttempt = webdriver.Ie(service=IEService(IEDriverManager().install()))
        logging.info("browser created - IE")
    except Exception as e:
        browser_error(e, "ie")
    return browserAttempt

# TODO: debug
def attempt_opera():
    browserAttempt = None
    try:
        logging.debug("attempting Opera web browser...")
        browserAttempt = webdriver.Opera(executable_path=OperaDriverManager().install())
        logging.info("browser created - Opera")
    except Exception as e:
        browser_error(e, "opera")
    return browserAttempt

def attempt_reconnect():
    session_id, session_url = read_session_data()
    if not session_id and not session_url:
        logging.warning("unable to read session data!")
        return None
    logging.debug("reconnecting to web browser...")
    logging.debug("reconnect id: {}".format(session_id))
    logging.debug("reconnect url: {}".format(session_url))
    try:
        options = webdriver.ChromeOptions()
        add_options(options)
        browserAttempt = webdriver.Remote(command_executor=session_url, options=options)
        browserAttempt.close()   # this closes the session's window - it is currently the only one, thus the session itself will be auto-killed, yet:
        # take the session that's already running
        browserAttempt.session_id = session_id
        browserAttempt.title # fails check with: 'NoneType' object has no attribute 'title'
        logging.info("browser reconnected!")
        return browserAttempt
    except Exception as e:
        logging.warning("unable to reconnect!")
        logging.debug(e)
    return None

# TODO: update and debug
def attempt_remote():
    link = 'http://{}:{}/wd/hub'.format(CONFIG["remote_browser_host"], CONFIG["remote_browser_port"])
    logging.debug("remote url: {}".format(link))
    def attempt(dc, opts):
        try:
            if not CONFIG["show"]:
                opts.add_argument('--headless')
            logging.debug("attempting remote: {}".format(browserType))
            browserAttempt = webdriver.Remote(command_executor=link, desired_capabilities=dc, options=opts)
            logging.info("remote browser created - {}".format(browserType))
            return browserAttempt
        except Exception as e:
            logging.warning("unable to connect remotely!")
            logging.debug(e)
        return None

    if "brave" in browserType: return attempt(*brave_options())
    elif "chrome" in browserType: return attempt(*chrome_options())
    elif "chromium" in browserType: return attempt(*chromium_options())
    elif "edge" in browserType: return attempt(*edge_options())
    elif "firefox" in browserType: return attempt(*firefox_options())
    elif "ie" in browserType: return attempt(*ie_options())
    elif "opera" in browserType: return attempt(*opera_options())
    logging.warning("unable to connect remotely via {}!".format(browserType))
    return None

################################################################################################
################################################################################################
################################################################################################

def brave_options():
    dC = DesiredCapabilities.BRAVE
    options = webdriver.BraveOptions()
    return options
    # return dC, options

def chrome_options():
    dC = DesiredCapabilities.CHROME
    options = webdriver.ChromeOptions()
    add_options(options)
    return options
    # return dC, options

def chromium_options():
    dC = DesiredCapabilities.CHROMIUM
    options = webdriver.ChromeOptions()
    return options
    # return dC, options

def edge_options():
    dC = DesiredCapabilities.EDGE
    # options = EdgeOptions()
    options = webdriver.EdgeOptions()
    options.use_chromium = True
    # options.binary_location="/home/{user}/.wdm/drivers/edgedriver/linux64/111.0.1661/msedgedriver".format(user=os.getenv('USER'))
    # os.chmod(options.binary_location, 0o755)
    # shutil.chown(options.binary_location, user=os.getenv('USER'), group=None)

    # options.binary_location="/home/{user}/.wdm/drivers/edgedriver/linux64/111.0.1661/msedgedriver".format(user=os.getenv('USER'))
    # fix any permissions issues
    # os.chmod(options.binary_location, 0o755)
    # shutil.chown(options.binary_location, user=os.getenv('USER'), group=None)
    return options
    # return dC, options

def firefox_options():
    dC = DesiredCapabilities.FIREFOX
    # options = webdriver.FirefoxOptions()
    options = FirefoxOptions()
    if CONFIG["debug_firefox"]:
        options.log.level = "trace"
    add_options(options)
    # options.add_argument("--enable-file-cookies")
    return options
    # return dC, options

def ie_options():
    dC = DesiredCapabilities.IE
    options = webdriver.ChromeOptions()
    return options
    # return dC, options

def opera_options():
    dC = DesiredCapabilities.OPERA
    options = webdriver.OperaOptions()
    # options.add_argument('allow-elevated-browser')
    # options.binary_location = "C:\\Users\\USERNAME\\FOLDERLOCATION\\Opera\\VERSION\\opera.exe"
    return options
    # return dC, options
