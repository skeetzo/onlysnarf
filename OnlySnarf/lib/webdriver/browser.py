import logging
logger = logging.getLogger(__name__)
import os
# import shutil
import platform

from .. import CONFIG, DEFAULT
from .util import configure_logging, read_session_data, write_session_data

##############
## Selenium ##
##############

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.file_detector import LocalFileDetector

###########################
# Chrome, Brave, Chromium #
###########################

from selenium.webdriver import Chrome as ChromeWebDriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType

########################
# Firefox: Geckodriver #
########################
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebDriver

######
# IE #
######
from selenium.webdriver.ie.service import Service as IEService
from webdriver_manager.microsoft import IEDriverManager

########
# Edge #
########
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

#########
# Opera #
#########
from webdriver_manager.opera import OperaDriverManager

def create_browser(browserType="auto"):
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

    browser = None
    logger.info("spawning web browser...")

    configure_logging()

    if "reconnect" in browserType:
        browser = attempt_reconnect(browserType.replace("reconnect:",""))
    elif "remote" in browserType:
        browser = attempt_remote(browserType.replace("remote:",""))

    elif "auto" in browserType:
        browser = attempt_reconnect(browserType)
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

    if not browser: raise Exception("failed to spawn a web browser!")

    browser.implicitly_wait(30) # seconds
    browser.set_page_load_timeout(1200)
    browser.maximize_window()
    browser.file_detector = LocalFileDetector() # for uploading via remote sessions
    
    write_session_data(browserType, browser.session_id, browser.command_executor._url)
    logger.debug(f"browser created successfully!{'' if CONFIG['show'] else ' (headless)'}")
    return browser

################################################################################################
################################################################################################
################################################################################################

def add_options(options):
    options.add_argument("--no-sandbox") # Bypass OS security model
    if not CONFIG["show"]:
        options.add_argument('--headless')
        options.add_argument("--window-size=1920,1080") # required for headless
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("enable-automation")
    # options.add_argument("--disable-infobars")

    # if os.name == 'nt':
        # options.add_argument(r"--user-data-dir=C:\Users\brain\AppData\Local\Google\Chrome\User Data")
    # else:
    # options.add_argument('--profile-directory=Default')

    if str(platform.processor()) == "aarch64": # raspi
        options.add_argument("--user-data-dir=/home/ubuntu/selenium") # do not disable, required for cookies to work 
    else:
        options.add_argument("--user-data-dir="+os.path.join(DEFAULT.ROOT_PATH,"tmp","selenium")) # do not disable, required for cookies to work 

    options.add_argument("--disable-browser-side-navigation") # https://stackoverflow.com/a/49123152/1689770

    # options.add_argument("--allow-insecure-localhost")            
    # possibly linux only
    # options.add_argument('disable-notifications')
    # https://stackoverflow.com/questions/50642308/webdriverexception-unknown-error-devtoolsactiveport-file-doesnt-exist-while-t
    # options.add_argument("start-maximized")
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
    # options.add_argument("--remote-debugging-port=9223") # required

def browser_error(err, browserName):
    if os.environ.get('ENV') == "True": print(err)
    logger.debug(err)
    logger.warning("unable to launch {}!".format(browserName))

# TODO: debug
def attempt_brave():
    browserAttempt = None
    try:
        logger.debug("attempting Brave web browser...")
        browserAttempt = ChromeWebDriver(service=ChromeService(executable_path=ChromeDriverManager(chrome_type=ChromeType.BRAVE).install(), log_path=DEFAULT.LOG_PATH_CHROMEDRIVER_BRAVE, service_args=configure_service_args()), options=configure_brave_options())
        logger.info("browser created - Brave")
    except Exception as e:
        browser_error(e, "brave")
    return browserAttempt

def attempt_chrome():
    browserAttempt = None
    try:
        logger.debug("attempting Chrome web browser...")
        # TODO: is this still necessary?
        # raspberrypi arm processors don't work with webdriver manager
        # linux = x86_64
        # rpi = aarch64
        logger.debug("checking processor for use with RPi4s...")
        processor = platform.processor()
        logger.debug("cpu processor: {}".format(processor))
        if str(processor) == "aarch64":
            logger.debug("cpu process: RPi4")
            # TODO: add file check for chromedriver w/ reminder warning for rpi install requirement
            browserAttempt = ChromeWebDriver(service=ChromeService('/usr/bin/chromedriver', log_path=DEFAULT.LOG_PATH_CHROMEDRIVER, service_args=configure_service_args()), options=configure_chrome_options())
        else:
            logger.debug("cpu process: standard")
            browserAttempt = ChromeWebDriver(service=ChromeService(executable_path=ChromeDriverManager().install(), log_path=DEFAULT.LOG_PATH_CHROMEDRIVER, service_args=configure_service_args()), options=configure_chrome_options())
        logger.info("browser created - Chrome")        
    except Exception as e:
        browser_error(e, "chrome")
    return browserAttempt

# TODO: debug
def attempt_chromium():
    browserAttempt = None
    try:
        logger.debug("attempting Chromium web browser...")
        browserAttempt = ChromeWebDriver(service=ChromeService(executable_path=ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), log_path=DEFAULT.LOG_PATH_CHROMEDRIVER_CHROMIUM, service_args=configure_service_args()), options=configure_chromium_options())
        logger.info("browser created - Chromium")        
    except Exception as e:
        browser_error(e, "chromium")
    return browserAttempt

# TODO: debug
def attempt_edge():
    browserAttempt = None
    try:
        logger.debug("attempting Edge web browser...")
        browserAttempt = webdriver.Edge(service=EdgeService(executable_path=EdgeChromiumDriverManager().install(), log_path=DEFAULT.LOG_PATH_CHROMEDRIVER_EDGE, service_args=configure_service_args()), options=configure_edge_options())
        logger.info("browser created - Edge")
    except Exception as e:
        browser_error(e, "edge")
    return browserAttempt

def attempt_firefox():
    browserAttempt = None
    # firefox needs non root
    if os.geteuid() == 0:
        logger.info("You must run `onlysnarf` as non-root for Firefox to work correctly!")
        return None
    try:
        logger.debug("attempting Firefox web browser...")
        browserAttempt = FirefoxWebDriver(service=FirefoxService(log_path=DEFAULT.LOG_PATH_GECKODRIVER), options=configure_firefox_options())
        logger.info("browser created - Firefox")
    except Exception as e:
        browser_error(e, "firefox")
    return browserAttempt

# TODO: debug
def attempt_ie():
    browserAttempt = None
    try:
        logger.debug("attempting IE web browser...")
        # driver_path = IEDriverManager().install()
        # os.chmod(driver_path, 0o755)
        # browserAttempt = webdriver.Ie(executable_path=IEService(driver_path))
        browserAttempt = webdriver.Ie(service=IEService(executable_path=IEDriverManager().install(), log_path=DEFAULT.LOG_PATH_CHROMEDRIVER_IE, service_args=configure_service_args()), options=configure_ie_options())
        logger.info("browser created - IE")
    except Exception as e:
        browser_error(e, "ie")
    return browserAttempt

# TODO: debug
def attempt_opera():
    browserAttempt = None
    try:
        logger.debug("attempting Opera web browser...")

        from selenium.webdriver.chrome import service
        webdriver_service = service.Service(executable_path=OperaDriverManager().install(), log_path=DEFAULT.LOG_PATH_CHROMEDRIVER_OPERA, service_args=configure_service_args())
        webdriver_service.start()

        options = webdriver.ChromeOptions()
        options.add_experimental_option('w3c', True)

        browserAttempt = webdriver.Remote(webdriver_service.service_url, options=options)

        # browserAttempt = webdriver.Opera(executable_path=OperaDriverManager().install())
        logger.info("browser created - Opera")
    except Exception as e:
        browser_error(e, "opera")
    return browserAttempt

def attempt_reconnect(browserType):
    session_id, session_url = read_session_data(browserType)
    if not session_id and not session_url:
        logger.debug("unable to read session data!")
        return None
    logger.debug("reconnecting to web browser...")
    logger.debug("reconnect id: {}".format(session_id))
    logger.debug("reconnect url: {}".format(session_url))
    try:
        # options = configure_options(browserType)
        # TODO: finish debugging / wait for better documentation on 4.0 @ https://www.selenium.dev/documentation/webdriver/drivers/remote_webdriver/
        # browserAttempt = webdriver.Remote(command_executor=session_url, options=options)
        browserAttempt = webdriver.Remote(command_executor=session_url)
        browserAttempt.close()   # this closes the session's window - it is currently the only one, thus the session itself will be auto-killed, yet:
        # take the session that's already running
        browserAttempt.session_id = session_id
        browserAttempt.title # fails check with: 'NoneType' object has no attribute 'title'
        logger.info("browser reconnected!")
        return browserAttempt
    except Exception as e:
        browser_error(e, f"reconnect:{browserType}")
    return None

# TODO: debug
def attempt_remote(browserType, host="skeetzo.com", port=8888):
    # link = f"http://{host}:{port}/wd/hub"
    link = f"http://{host}:{port}"
    logger.debug(f"remote webserver: {link}")
    browserAttempt = None
    try:        
        options = configure_options(browserType)

        logger.debug(f"attempting remote browser: {browserType}")

        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.set_capability("browserVersion", "67")
        # chrome_options.set_capability("platformName", "Windows XP")

        # TODO: finish debugging -> 'string indices must be integers'
        browserAttempt = webdriver.Remote(command_executor=link, options=options)
        logger.info(f"remote browser created: {browserType}")
        return browserAttempt
    except Exception as e:
        browser_error(e, f"remote:{browserType}")
    return None

################################################################################################
################################################################################################
################################################################################################

def configure_service_args():
    # Chromedriver and Chrome browser versions should match, and if they don’t the driver will error. If you disable the build check, you can force the driver to be used with any version of Chrome. Note that this is an unsupported feature, and bugs will not be investigated.
    # service = webdriver.chrome.service.Service(service_args=['--disable-build-check'], log_path=log_path)
    return [
        '--log-level=DEBUG',
        '--append-log', '--readable-timestamp',
    ]

# from below
def configure_options(browserType):
    if browserType == "brave":
        return configure_brave_options()
    elif browserType == "chrome":
        return configure_chrome_options()
    elif browserType == "chromium":
        return configure_chromium_options()
    elif browserType == "edge":
        return configure_edge_options()
    elif browserType == "firefox":
        return configure_firefox_options()
    elif browserType == "ie":
        return configure_ie_options()
    elif browserType == "opera":
        return configure_opera_options()

################################################################################################
################################################################################################
################################################################################################

def configure_brave_options():
    options = webdriver.BraveOptions()
    add_options(options)
    options.add_argument("--remote-debugging-port=9223") # required
    return options

def configure_chrome_options():
    options = webdriver.ChromeOptions()
    add_options(options)
    options.add_argument("--remote-debugging-port=9223") # required
    return options

def configure_chromium_options():
    options = webdriver.ChromeOptions()
    add_options(options)
    options.add_argument("--remote-debugging-port=9223") # required
    return options

def configure_edge_options():
    # options = EdgeOptions()
    options = webdriver.EdgeOptions()
    options.use_chromium = True
    add_options(options)
    options.add_argument("--remote-debugging-port=9223") # required
    # options.binary_location="/home/{user}/.wdm/drivers/edgedriver/linux64/111.0.1661/msedgedriver".format(user=os.getenv('USER'))
    # os.chmod(options.binary_location, 0o755)
    # shutil.chown(options.binary_location, user=os.getenv('USER'), group=None)

    # options.binary_location="/home/{user}/.wdm/drivers/edgedriver/linux64/111.0.1661/msedgedriver".format(user=os.getenv('USER'))
    # fix any permissions issues
    # os.chmod(options.binary_location, 0o755)
    # shutil.chown(options.binary_location, user=os.getenv('USER'), group=None)
    return options

def configure_firefox_options():
    options = FirefoxOptions()
    add_options(options)
    # BUG: required for cookies when using firefox
    # options.add_argument("-profile")
    # options.add_argument(os.path.expanduser("~/.mozilla/firefox/whatever.selenium"))
    options.add_argument("--enable-file-cookies") # probably not needed
    return options

def configure_ie_options():
    options = webdriver.ChromeOptions()
    add_options(options)
    options.add_argument("--remote-debugging-port=9223") # required
    return options

def configure_opera_options():
    options = webdriver.OperaOptions()
    add_options(options)
    options.add_argument("--remote-debugging-port=9223") # required
    # options.add_argument('allow-elevated-browser')
    # options.binary_location = "C:\\Users\\USERNAME\\FOLDERLOCATION\\Opera\\VERSION\\opera.exe"
    return options
