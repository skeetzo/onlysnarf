@staticmethod
def auth():
    spawned = Driver.spawn()
    if not spawned: return False
    if not Driver.LOGGED_IN:
        if not Driver.login():
            Settings.err_print("Failure to Login")
            return False
    Driver.LOGGED_IN = True
    return True

@staticmethod
def spawn():
    if not Driver.BROWSER or Driver.BROWSER == None:
        spawned = Driver.spawn_browser()
    if not spawned: 
        Settings.err_print("Failure to Spawn Browser")
        return False
    return True

@staticmethod
def spawn_browser():      
    type_ = None
    Settings.maybe_print("spawning browser...")
    def google():
        Settings.maybe_print("spawning chrome browser...")
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--no-sandbox") # Bypass OS security model
            # options.add_argument("--disable-setuid-sandbox")
            # options.add_argument("--disable-dev-shm-usage") # overcome limited resource problems
            # options.add_argument("--disable-gpu") # applicable to windows os only
            options.add_argument('--disable-software-rasterizer')
            if not Settings.is_show_window():
                options.add_argument('--headless')
                # options.add_argument('--disable-smooth-scrolling')
            #
            options.add_argument("--disable-extensions") # disabling extensions
            options.add_argument("--disable-infobars") # disabling infobars
            # options.add_argument("--start-maximized")
            # options.add_argument("--window-size=1920,1080")
            # options.add_argument("--user-data-dir=/tmp/");
            # options.add_argument('--disable-login-animations')
            # options.add_argument('--disable-modal-animations')
            # options.add_argument('--disable-sync')
            # options.add_argument('--disable-background-networking')
            # options.add_argument('--disable-web-resources')
            options.add_argument('--ignore-certificate-errors')
            # options.add_argument('--disable-logging')
            # options.add_argument('--no-experiments')
            # options.add_argument('--incognito')
            # options.add_argument('--user-agent=MozillaYerMomFox')
            options.add_argument("--remote-debugging-address=localhost")
            options.add_argument("--remote-debugging-port=9223")
            options.add_argument("--allow-insecure-localhost")
            # options.add_argument("--acceptInsecureCerts")
            #
            # options.add_experimental_option("prefs", {
              # "download.default_directory": str(DOWNLOAD_PATH),
              # "download.prompt_for_download": False,
              # "download.directory_upgrade": True,
              # "safebrowsing.enabled": True
            # })
            capabilities = {
              'browserName': 'chrome',
              'platform': 'LINUX',
              'chromeOptions':  {
                'acceptInsecureCerts': True,
                'useAutomationExtension': False,
                'forceDevToolsScreenshot': True,
                'args': ['--start-maximized', '--disable-infobars']
              }
            }  
            service_args = []
            if Settings.is_debug():
                service_args = ["--verbose", "--log-path=/var/log/onlysnarf/chromedriver.log"]
            # desired_capabilities = capabilities
            Settings.dev_print("executable_path: {}".format(chromedriver_binary.chromedriver_filename))
            # options.binary_location = chromedriver_binary.chromedriver_filename
            driver = webdriver.Chrome(desired_capabilities=capabilities, executable_path=chromedriver_binary.chromedriver_filename, chrome_options=options, service_args=service_args)
            print("Browser Created - Chrome")
            Settings.dev_print("Successful Browser - Chrome")
            return driver
        except Exception as e:
            Settings.maybe_print(e)
            Settings.warn_print("Missing Chromedriver")
            return False

    def firefox():
        Settings.maybe_print("spawning firefox browser...")
        # firefox needs non root
        if os.geteuid() == 0:
            print("You must run `onlysnarf` as non-root for Firefox to work correctly!")
            return False
           # sys.exit("You need root permissions to do this, laterz!")
        try:
            d = DesiredCapabilities.FIREFOX
            d['loggingPrefs'] = {'browser': 'ALL'}
            opts = FirefoxOptions()
            opts.log.level = "trace"
            if not Settings.is_show_window():
                opts.add_argument("--headless")
            # driver = webdriver.Firefox(options=opts, log_path='/var/log/onlysnarf/geckodriver.log')
            # driver = webdriver.Firefox(firefox_binary="/usr/local/bin/geckodriver", options=opts, capabilities=d)
            driver = webdriver.Firefox(options=opts, desired_capabilities=d, log_path='/var/log/onlysnarf/geckodriver.log')
            print("Browser Created - Firefox")
            Settings.dev_print("Successful Browser - Firefox")
            return driver
        except Exception as e:
            Settings.maybe_print(e)
            Settings.warn_print("Missing Geckodriver")
            return False

    def reconnect(reconnect_id=None, url=None):
        if reconnect_id and url:
            Settings.maybe_print("reconnecting browser...")
            Settings.dev_print("reconnect id: {}".format(reconnect_id))
            Settings.dev_print("reconnect url: {}".format(url))
            # executor_url = driver.command_executor._url
            # session_id = driver.session_id
            # https://stackoverflow.com/questions/8344776/can-selenium-interact-with-an-existing-browser-session
            # def attach_to_session(executor_url, session_id):
            original_execute = WebDriver.execute
            def new_command_execute(self, command, params=None):
                if command == "newSession":
                    # Mock the response
                    return {'success': 0, 'value': None, 'sessionId': reconnect_id}
                else:
                    return original_execute(self, command, params)
            # Patch the function before creating the driver object
            WebDriver.execute = new_command_execute
            driver = webdriver.Remote(command_executor=url, desired_capabilities={})
            driver.session_id = reconnect_id
            # Replace the patched function with original function
            WebDriver.execute = original_execute
            if Settings.use_tabs():
                tabs = len(driver.window_handles) - 1
                tabNumber = int(Settings.use_tabs())
                Settings.dev_print("tabs: {} | {} :tabNumber".format(tabs, tabNumber))
                if int(tabNumber) == 0: pass # nothing required
                if int(tabNumber) > int(tabs):
                    driver.execute_script('''window.open("{}","_blank");'''.format(ONLYFANS_HOME_URL))
                elif int(tabNumber) <= int(tabs):
                    driver.switch_to.window(driver.window_handles[tabNumber])
                time.sleep(2)
            Settings.dev_print("Successful Reconnect")
            return driver

        if Settings.get_reconnect_id() and Settings.get_reconnect_url():
            return reconnect(reconnect_id=Settings.get_reconnect_id(), url=Settings.get_reconnect_url())
        try:
            id_, url_ = Settings.read_session_data()
            if id_ and url_: return reconnect(reconnect_id=id_, url=url_)
        except Exception as e:
            Settings.maybe_print(e)
            Settings.err_print("Unable to connect to remote server")
            return None        
        Settings.err_print("Missing reconnect ID or URL")
        return None

    def remote():
        Settings.maybe_print("spawning remote browser...")
        def attempt_firefox():
            Settings.dev_print("attempting remote: firefox")
            try:
                firefox_options = webdriver.FirefoxOptions()
                if not Settings.is_show_window():
                    firefox_options.add_argument('--headless')
                dC = DesiredCapabilities.FIREFOX
                driver = webdriver.Remote(
                   command_executor=link,
                   desired_capabilities=dC,
                   options=firefox_options)
                print("Remote Browser Created - Firefox")
                Settings.dev_print("Successful Remote - Firefox")
                return driver
            except Exception as e:
                Settings.dev_print(e)
        def attempt_chrome():
            Settings.dev_print("attempting remote: chrome")
            try:
                chrome_options = webdriver.ChromeOptions()
                if not Settings.is_show_window():
                    chrome_options.add_argument('--headless')
                dC = DesiredCapabilities.CHROME
                driver = webdriver.Remote(
                   command_executor=link,
                   desired_capabilities=dC,
                   options=chrome_options)
                print("Remote Browser Created - Chrome")
                Settings.dev_print("Successful Remote - Chrome")
                return driver
            except Exception as e:
                Settings.dev_print(e)
        try:
            host = Settings.get_remote_browser_host()
            port = Settings.get_remote_browser_port()
            link = 'http://{}:{}/wd/hub'.format(host, port)
            Settings.dev_print(link)
            if Settings.get_browser_type() == "remote-firefox":
                successful_driver = attempt_firefox()
            elif Settings.get_browser_type() == "remote-chrome":
                successful_driver = attempt_chrome()
            else:
                successful_driver = attempt_firefox()
                if not successful_driver or successful_driver == None:
                    successful_driver = attempt_chrome()
            if not successful_driver or successful_driver == None:
                Settings.err_print("Unable to connect remotely")
            return successful_driver
        except Exception as e:
            Settings.maybe_print(e)
            Settings.err_print("Unable to connect remotely")
            return False

    BROWSER_TYPE = Settings.get_browser_type()

    def auto(driver_):
        if "remote" in BROWSER_TYPE and not driver_:
            driver_ = remote()
        if not driver:
            driver_ = firefox()
            if not driver_:
                driver_ = google()
        return driver_

    if BROWSER_TYPE == "google":
        driver = google()
    elif BROWSER_TYPE == "firefox":
        driver = firefox()
    elif "auto" in BROWSER_TYPE:
        try:
            driver = reconnect()
            driver.title
            print("Browser Successfully Reconnected")
            driver = auto(driver)
        except Exception as e:
            Settings.dev_print(e)
            driver = auto(None)
    elif "remote" in str(BROWSER_TYPE):
        driver = remote()
    elif BROWSER_TYPE == "reconnect":
        try:
            driver = reconnect()
            driver.title
            print("Browser Successfully Reconnected")
        except Exception as e:
            Settings.dev_print(e)
            driver = None        
    if driver and Settings.is_keep():
        Settings.write_session_data(driver.session_id, driver.command_executor._url)

    if not driver:
        Settings.err_print("Unable to spawn browser")
        # sys.exit(1)
        os._exit(1)

    driver.implicitly_wait(30) # seconds
    driver.set_page_load_timeout(1200)
    driver.file_detector = LocalFileDetector()
    if not Driver.BROWSER: Driver.BROWSER = driver
    return driver