
def spawn_browser(self, browserType):
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

    if str(Settings.is_debug("selenium")) == "False":
        import logging
        from selenium.webdriver.remote.remote_connection import LOGGER as SeleniumLogger
        SeleniumLogger.setLevel(logging.ERROR)
        logging.getLogger("urllib3").setLevel(logging.ERROR)
        logging.getLogger("requests").setLevel(logging.ERROR)
        logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.ERROR)

        if int(Settings.get_verbosity()) >= 2:
            SeleniumLogger.setLevel(logging.WARNING)
            logging.getLogger("urllib3").setLevel(logging.WARNING)
            logging.getLogger("requests").setLevel(logging.WARNING)
            logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.WARNING)

    browser = None
    Settings.print("spawning web browser...")

    if "auto" in browserType:
        browser = attempt_reconnect()
        if not browser: browser = attempt_chrome(brave=True, chromium=False, edge=False)
        if not browser: browser = attempt_chrome(brave=False, chromium=False, edge=False)
        if not browser: browser = attempt_chrome(brave=False, chromium=True, edge=False)
        if not browser: browser = attempt_chrome(brave=False, chromium=False, edge=True)
        if not browser: browser = attempt_firefox()
        if not browser: browser = attempt_ie()
        if not browser: browser = attempt_opera()
    elif "brave" in browserType:
        browser = attempt_chrome(brave=True, chromium=False, edge=False)
    elif "chrome" in browserType:
        browser = attempt_chrome(brave=False, chromium=False, edge=False)
    elif "chromium" in browserType:
        browser = attempt_chrome(brave=False, chromium=True, edge=False)
    elif "edge" in browserType:
        browser = attempt_chrome(brave=False, chromium=False, edge=True)
    elif "firefox" in browserType:
        browser = attempt_firefox()
    elif "ie" in browserType:
        browser = attempt_ie()
    elif "opera" in browserType:
        browser = attempt_opera()
    elif "remote" in browserType:
        browser = attempt_remote()

    if browser and str(Settings.is_keep()) == "True":
        self.session_id = browser.session_id
        self.session_url = browser.command_executor._url
        self.write_session_data()

    if not browser:
        Settings.err_print("unable to spawn a web browser!")
        if os.environ.get("ENV") and str(os.environ.get("ENV")) == "test": return False
        os._exit(1)

    browser.implicitly_wait(30) # seconds
    browser.set_page_load_timeout(1200)
    browser.file_detector = LocalFileDetector() # for uploading via remote sessions
    if str(Settings.is_show_window()) == "False":
        Settings.print("browser spawned successfully (headless)".format(browserType))
    else:
        Settings.print("browser spawned successfully".format(browserType))
    return browser











def add_options(options):
    options.add_argument("--no-sandbox") # Bypass OS security model
    if str(Settings.is_show_window()) == "False":
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
        options.add_argument("--user-data-dir="+os.path.join(Settings.get_base_directory(),"tmp","selenium")) # do not disable, required for cookies to work 

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
    Settings.warn_print("unable to launch {}!".format(browserName))
    Settings.dev_print(err)

def attempt_chrome():
    browserAttempt = None
    try:
        Settings.maybe_print("attempting Chrome web browser...")
        # raspberrypi arm processors don't work with webdriver manager
        # linux = x86_64
        # rpi = aarch64
        processor = platform.processor()
        Settings.dev_print("cpu processor: {}".format(processor))
        if str(processor) == "aarch64":
            # TODO: add file check for chromedriver w/ reminder warning for rpi install requirement
            browserAttempt = webdriver.Chrome(service=ChromeService('/usr/bin/chromedriver'), options=chrome_options())
        else:
            browserAttempt = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options())
        Settings.print("browser created - Chrome")        
    except Exception as e:
        browser_error(e, "chrome")
    return browserAttempt

def attempt_brave():
    browserAttempt = None
    try:
        Settings.maybe_print("attempting Brave web browser...")
        browserAttempt = webdriver.Chrome(service=BraveService(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()), options=chrome_options())
        Settings.print("browser created - Brave")
    except Exception as e:
        browser_error(e, "brave")
    return browserAttempt

def attempt_chromium():
    browserAttempt = None
    try:
        Settings.maybe_print("attempting Chromium web browser...")
        browserAttempt = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), options=chrome_options())
        Settings.print("browser created - Chromium")        
    except Exception as e:
        browser_error(e, "chromium")
    return browserAttempt

# TODO: debug
def attempt_edge():
    browserAttempt = None
    try:
        Settings.maybe_print("attempting Edge web browser...")
        # browserAttempt = Edge(executable_path=options.binary_location, options=edge_options())
        browserAttempt = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
        Settings.print("browser created - Edge")
    except Exception as e:
        browser_error(e, "edge")
    return browserAttempt

def attempt_firefox():
    browserAttempt = None
    # firefox needs non root
    if os.geteuid() == 0:
        Settings.print("You must run `onlysnarf` as non-root for Firefox to work correctly!")
        return False
    try:
        Settings.maybe_print("attempting Firefox web browser...")
        browserAttempt = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options())
        Settings.print("browser created - Firefox")
    except Exception as e:
        browser_error(e, "firefox")
    return browserAttempt

# TODO: debug
def attempt_ie():
    browserAttempt = None
    try:
        Settings.maybe_print("attempting IE web browser...")
        driver_path = IEDriverManager().install()
        os.chmod(driver_path, 0o755)
        # browserAttempt = webdriver.Ie(executable_path=IEService(driver_path))
        browserAttempt = webdriver.Ie(service=IEService(IEDriverManager().install()))
        Settings.print("browser created - IE")
    except Exception as e:
        browser_error(e, "ie")
    return browserAttempt

# TODO: debug
def attempt_opera():
    browserAttempt = None
    try:
        Settings.maybe_print("attempting Opera web browser...")
        browserAttempt = webdriver.Opera(executable_path=OperaDriverManager().install())
        Settings.print("browser created - Opera")
    except Exception as e:
        browser_error(e, "opera")
    return browserAttempt

def attempt_reconnect():
    self.read_session_data()
    if not self.session_id and not self.session_url:
        Settings.warn_print("unable to read session data!")
        return None
    Settings.maybe_print("reconnecting to web browser...")
    Settings.dev_print("reconnect id: {}".format(self.session_id))
    Settings.dev_print("reconnect url: {}".format(self.session_url))
    try:
        options = webdriver.ChromeOptions()
        add_options(options)
        browserAttempt = webdriver.Remote(command_executor=self.session_url, options=options)
        browserAttempt.close()   # this closes the session's window - it is currently the only one, thus the session itself will be auto-killed, yet:
        # take the session that's already running
        browserAttempt.session_id = self.session_id
        browserAttempt.title # fails check with: 'NoneType' object has no attribute 'title'
        Settings.print("browser reconnected!")
        return browserAttempt
    except Exception as e:
        Settings.warn_print("unable to reconnect!")
        Settings.dev_print(e)
    return None

# TODO: update and debug
def attempt_remote():
    link = 'http://{}:{}/wd/hub'.format(Settings.get_remote_browser_host(), Settings.get_remote_browser_port())
    Settings.dev_print("remote url: {}".format(link))
    def attempt(dc, opts):
        try:
            if str(Settings.is_show_window()) == "False":
                opts.add_argument('--headless')
            Settings.dev_print("attempting remote: {}".format(browserType))
            browserAttempt = webdriver.Remote(command_executor=link, desired_capabilities=dc, options=opts)
            Settings.print("remote browser created - {}".format(browserType))
            return browserAttempt
        except Exception as e:
            Settings.warn_print("unable to connect remotely!")
            Settings.dev_print(e)
        return None

    if "brave" in browserType: return attempt(*brave_options())
    elif "chrome" in browserType: return attempt(*chrome_options())
    elif "chromium" in browserType: return attempt(*chromium_options())
    elif "edge" in browserType: return attempt(*edge_options())
    elif "firefox" in browserType: return attempt(*firefox_options())
    elif "ie" in browserType: return attempt(*ie_options())
    elif "opera" in browserType: return attempt(*opera_options())
    Settings.warn_print("unable to connect remotely via {}!".format(browserType))
    return None



def brave_options():
    dC = DesiredCapabilities.BRAVE
    options = webdriver.BraveOptions()
    return dC, options

def chrome_options():
    dC = DesiredCapabilities.CHROME
    options = webdriver.ChromeOptions()
    add_options(options)
    return dC, options

def chromium_options():
    dC = DesiredCapabilities.CHROMIUM
    options = webdriver.ChromeOptions()
    return dC, options

def edge_options():
    dC = DesiredCapabilities.EDGE
    options = webdriver.EdgeOptions()
    options.use_chromium = True
    # options.binary_location="/home/{user}/.wdm/drivers/edgedriver/linux64/111.0.1661/msedgedriver".format(user=os.getenv('USER'))
    # os.chmod(options.binary_location, 0o755)
    # shutil.chown(options.binary_location, user=os.getenv('USER'), group=None)

    # options.binary_location="/home/{user}/.wdm/drivers/edgedriver/linux64/111.0.1661/msedgedriver".format(user=os.getenv('USER'))
    # fix any permissions issues
    # os.chmod(options.binary_location, 0o755)
    # shutil.chown(options.binary_location, user=os.getenv('USER'), group=None)

    return dC, options

def firefox_options():
    dC = DesiredCapabilities.FIREFOX
    options = webdriver.FirefoxOptions()
    if str(Settings.is_debug("firefox")) == "True":
        options.log.level = "trace"
    add_options(options)
    # options.add_argument("--enable-file-cookies")
    return dC, options

def ie_options():
    dC = DesiredCapabilities.IE
    options = webdriver.ChromeOptions()
    return dC, options

def opera_options():
    dC = DesiredCapabilities.OPERA
    options = webdriver.OperaOptions()
    # options.add_argument('allow-elevated-browser')
    # options.binary_location = "C:\\Users\\USERNAME\\FOLDERLOCATION\\Opera\\VERSION\\opera.exe"
    return dC, options






## possibly move these functions elsewhere (again)
def read_session_data(self):
    Settings.maybe_print("reading local session")
    path_ = os.path.join(Settings.get_base_directory(), "session.json")
    Settings.dev_print("local session path: "+str(path_))
    try:
        with open(str(path_)) as json_file:  
            data = json.load(json_file)
            self.session_id = data['id']
            self.session_url = data['url']
        Settings.maybe_print("loaded local users")
    except Exception as e:
        Settings.dev_print(e)

def write_session_data(self):
    Settings.maybe_print("writing local session")
    Settings.dev_print("saving session id: {}".format(self.session_id))        
    Settings.dev_print("saving session url: {}".format(self.session_url))
    path_ = os.path.join(Settings.get_base_directory(), "session.json")
    Settings.dev_print("local session path: "+str(path_))
    data = {}
    data['id'] = self.session_id
    data['url'] = self.session_url
    try:
        with open(str(path_), 'w') as outfile:  
            json.dump(data, outfile, indent=4, sort_keys=True)
        Settings.maybe_print("saved session data")
    except FileNotFoundError:
        Settings.err_print("Missing Session File")
    except OSError:
        Settings.err_print("Missing Session Path")