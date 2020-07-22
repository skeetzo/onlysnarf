def run_browserstack(self,os_name,os_version,browser,browser_version,remote_project_name,remote_build_name):
    "Run the test in browser stack when remote flag is 'Y'"
    #Get the browser stack credentials from browser stack credentials file
    USERNAME = remote_credentials.USERNAME
    PASSWORD = remote_credentials.ACCESS_KEY
    if browser.lower() == 'ff' or browser.lower() == 'firefox':
        desired_capabilities = DesiredCapabilities.FIREFOX            
    elif browser.lower() == 'ie':
        desired_capabilities = DesiredCapabilities.INTERNETEXPLORER
    elif browser.lower() == 'chrome':
        desired_capabilities = DesiredCapabilities.CHROME            
    elif browser.lower() == 'opera':
        desired_capabilities = DesiredCapabilities.OPERA        
    elif browser.lower() == 'safari':
        desired_capabilities = DesiredCapabilities.SAFARI
    desired_capabilities['os'] = os_name
    desired_capabilities['os_version'] = os_version
    desired_capabilities['browser_version'] = browser_version
    if remote_project_name is not None:
        desired_capabilities['project'] = remote_project_name
    if remote_build_name is not None:
        desired_capabilities['build'] = remote_build_name+"_"+str(datetime.now().strftime("%c"))

    return webdriver.Remote(RemoteConnection("http://%s:%s@hub-cloud.browserstack.com/wd/hub"%(USERNAME,PASSWORD),resolve_ip= False),
        desired_capabilities=desired_capabilities) 





def remote(self) -> None:
    if not self.debug:
        log("debug mode is turned off, can't reuse old session")
        return

    file = open(self.current_session_path, "r")
    content = file.read()
    lines = content.split(";")
    url = lines[0]
    session = lines[1]

    self.driver = webdriver.Remote(
        command_executor=url, desired_capabilities=DesiredCapabilities.CHROME
    )
    self.driver.session_id = session

    self.set_config() 




def attach_to_session(executor_url, session_id):
    original_execute = WebDriver.execute

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return original_execute(self, command, params)

    # Patch the function before creating the driver object
    WebDriver.execute = new_command_execute
    driver = webdriver.Remote(command_executor=executor_url,
                              desired_capabilities={})
    driver.session_id = session_id
    # Replace the patched function with original function
    WebDriver.execute = original_execute
    return driver 




def __init__(self, command_executor = None, session_id = None, previous_read_message = None):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")

    chrome_options.add_argument("--user-agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'")

    chrome_options.add_argument('--verbose')
    chrome_options.add_argument('--log-path=/tmp/chrome.log')


    if command_executor == None:
        if config.CHROMEDRIVER_LOCATION == 'None': #Launching in docker container
            chrome_options.add_argument('--headless')
            self.driver = webdriver.Chrome(chrome_options=chrome_options)
            self.driver.set_window_size(1920, 1080)

        else:
            self.driver = webdriver.Chrome(config.CHROMEDRIVER_LOCATION, chrome_options=chrome_options)

        self.driver.get('https://web.whatsapp.com')

        print(self.driver.session_id )
        print(self.driver.command_executor._url)

        self.find_scan_code()

    else:
        self.driver = webdriver.Remote(command_executor=command_executor,desired_capabilities={})
        self.driver.close()
        self.driver.session_id = session_id

    self.previous_read_message = previous_read_message 







from selenium import webdriver

driver = webdriver.Chrome()
executor_url = driver.command_executor._url
session_id = driver.session_id
driver.get("http://tarunlalwani.com")

print session_id
print executor_url


driver2 = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
driver2.session_id = session_id
print driver2.current_url








driver = webdriver.Firefox()  #python

# extract to session_id and _url from driver object.

url = driver.command_executor._url       #"http://127.0.0.1:60622/hub"
session_id = driver.session_id            #'4e167f26-dc1d-4f51-a207-f761eaf73c31'

# Use these two parameter to connect to your driver.

driver = webdriver.Remote(command_executor=url,desired_capabilities={})
driver.close()   # this prevents the dummy browser
driver.session_id = session_id

# And you are connected to your driver again.

driver.get("http://www.mrsmart.in")











add `destination` to backup functions

-keep -> keep browser open
-reconnect -> reconnect to existing/previous session

check if present @ spawn, determines reconnect behaviour without extra args
-session $sessionId -> session to reconnect to
-url $executorURL -> executor_url in conjunct w/ session

if keep: save session&url in mount_path
if reconnect & no session||url: check for saved session||url in mount_path
