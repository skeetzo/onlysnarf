
    ##################
    ###### Login #####
    ##################

    def login(self):
        """
        Logs into OnlyFans account provided via args and chosen method.

        Checks if already logged in first. Logs in via requested method or tries all available.

        Returns
        -------
        bool
            Whether or not the login was successful

        """

        if self.logged_in: return True
        Settings.print('logging into OnlyFans for {}...'.format(Settings.get_username()))

        def loggedin_check():
            """Check if already logged in before attempting to login again"""

            self.go_to_home(force=True)
            try:
                # ele = self.browser.find_element(By.CLASS_NAME, Element.get_element_by_name("loginCheck").getClass())
                WebDriverWait(self.browser, 10, poll_frequency=1).until(EC.visibility_of_element_located((By.CLASS_NAME, Element.get_element_by_name("loginCheck").getClass())))
                # if ele: 
                Settings.print("already logged into OnlyFans!")
                return True
            except TimeoutException as te:
                Settings.dev_print(str(te))
            except Exception as e:
                Settings.dev_print(e)
            return False

        def login_check(which):
            """
            Check after login attempt for successful home page

            Returns
            -------
            bool
                Whether or not the login check was successful

            """


            def try_phone():
                Settings.maybe_print("verifying phone number...")
                element = self.browser.switch_to.active_element
                element.send_keys(str(Settings.get_phone_number()))
                element.send_keys(Keys.ENTER)

            # TODO: requires testing, not successfuly receiving email w/ code to test further
            def try_email():
                Settings.print("email verification required - please enter the code sent to your email!")
                element = self.browser.switch_to.active_element
                element.send_keys(str(input("Enter code: ")))
                element.send_keys(Keys.SHIFT + Keys.TAB)
                element.send_keys(Keys.ENTER)

            try:
                Settings.dev_print("waiting for login check...")
                WebDriverWait(self.browser, 30, poll_frequency=2).until(EC.visibility_of_element_located((By.CLASS_NAME, Element.get_element_by_name("loginCheck").getClass())))
                Settings.print("OnlyFans login successful!")
                Settings.dev_print("login successful - {}".format(which))
                return True
            except TimeoutException as te:
                bodyText = self.browser.find_element(By.TAG_NAME, "body").text
                Settings.dev_print(bodyText)
                # check for phone number page
                if "Verify your identity by entering the phone number associated with your Twitter account." in str(bodyText):
                    try_phone()
                    login_check(which)
                # check for email notification
                elif "Check your email" in str(bodyText):
                    try_email()
                    login_check(which)
                else:
                    # Settings.dev_print(str(te))
                    Settings.print("Login Failure: Timed Out! Please check your credentials.")
                    Settings.print(": If the problem persists, OnlySnarf may require an update.")
                    # output page text for debugging
                return False
            except Exception as e:
                Driver.error_checker(e)
                Settings.print("OnlyFans login failure: OnlySnarf may require an update")
                return False
            return True
        
        def via_form():
            """
            Logs in via OnlyFans username & password form
            
            Returns
            -------
            bool
                Whether or not the login attempt was successful

            """

            try:
                Settings.maybe_print("logging in via form")
                username = str(Settings.get_username_onlyfans())
                password = str(Settings.get_password())
                if str(username) == "" or str(password) == "":
                    Settings.err_print("missing onlyfans login info")
                    return False
                self.go_to_home()
                WAIT = WebDriverWait(self.browser, 10, poll_frequency=2)
                Settings.dev_print("finding username & password")
                usernameField = WAIT.until(EC.presence_of_element_located((By.NAME, "email")))
                passwordField = WAIT.until(EC.presence_of_element_located((By.NAME, "password")))
                usernameField.click()
                usernameField.send_keys(username)
                Settings.dev_print("username entered")
                passwordField.click()
                passwordField.send_keys(password)
                Settings.dev_print("password entered")
                passwordField.send_keys(Keys.ENTER)
                def check_captcha():
                    try:
                        time.sleep(10) # wait extra long to make sure it doesn't verify obnoxiously
                        el = self.browser.find_element("name", "password")
                        if not el: return # likely logged in without captcha
                        Settings.print("waiting for captcha completion by user...")
                        # action = webdriver.common.action_chains.ActionChains(self.browser)
                        action = ActionChains(self.browser)
                        action.move_to_element_with_offset(el, 40, 100)
                        action.click()
                        action.perform()
                        time.sleep(10)
                        sub = None
                        submit = self.browser.find_element(By.CLASS_NAME, "g-btn.m-rounded.m-flex.m-lg")
                        for ele in submit:
                            if str(ele.get_attribute("innerHTML")) == "Login":
                                sub = ele
                        if sub and sub.is_enabled():
                            submit.click()
                        elif sub and not sub.is_enabled():
                            Settings.err_print("unable to login via form - captcha")
                    except Exception as e:
                        if "Unable to locate element: [name=\"password\"]" not in str(e):
                            Settings.dev_print(e)
                check_captcha()
                return login_check("form")
            except Exception as e:
                Settings.dev_print("form login failure")
                Driver.error_checker(e)
            return False

        def via_google():
            """
            Logs in via linked Google account. (doesn't work)
            
            Returns
            -------
            bool
                Whether or not the login attempt was successful

            """

            try:
                Settings.maybe_print("logging in via google")
                username = str(Settings.get_username_google())
                password = str(Settings.get_password_google())
                if str(username) == "" or str(password) == "":
                    Settings.err_print("missing google login info")
                    return False
                # self.go_to_home()
                elements = self.browser.find_elements(By.TAG_NAME, "a")
                [elem for elem in elements if '/auth/google' in str(elem.get_attribute('href'))][0].click()
                time.sleep(5)
                username_ = self.browser.switch_to.active_element
                # then click username spot
                username_.send_keys(username)
                username_.send_keys(Keys.ENTER)
                Settings.dev_print("username entered")
                time.sleep(2)
                password_ = self.browser.switch_to.active_element
                # fill in password and hit the login button 
                password_.send_keys(password)
                Settings.dev_print("password entered")
                password_.send_keys(Keys.ENTER)
                return login_check("google")
            except Exception as e:
                Settings.dev_print("google login failure")
                Driver.error_checker(e)
            return False

        def via_twitter():
            """
            Logs in via linked Twitter account
            
            Returns
            -------
            bool
                Whether or not the login attempt was successful

            """

            try:
                Settings.maybe_print("logging in via twitter")
                username = str(Settings.get_username_twitter())
                password = str(Settings.get_password_twitter())
                if str(username) == "" or str(password) == "":
                    Settings.err_print("missing twitter login info")
                    return False
                # self.go_to_home()
                # rememberMe checkbox doesn't actually cause login to be remembered
                # rememberMe = self.browser.find_element_by_xpath(Element.get_element_by_name("rememberMe").getXPath())
                # if not rememberMe.is_selected():
                    # rememberMe.click()
                # if str(Settings.MANUAL) == "True":
                    # Settings.print("Please Login")
                elements = self.browser.find_elements(By.TAG_NAME, "a")
                [elem for elem in elements if '/twitter/auth' in str(elem.get_attribute('href'))][0].click()
                self.browser.find_element("name", "session[username_or_email]").send_keys(username)
                Settings.dev_print("username entered")
                # fill in password and hit the login button 
                password_ = self.browser.find_element("name", "session[password]")
                password_.send_keys(password)
                Settings.dev_print("password entered")
                password_.send_keys(Keys.ENTER)
                return login_check("twitter")
            except Exception as e:
                Settings.dev_print("twitter login failure")
                Driver.error_checker(e)
            return False

        # this needs to go after them because they reconnect then need to login check
        # if Settings.get_browser_type() == "reconnect" or Settings.get_browser_type() == "remote" or 

        try:
            if loggedin_check():
                self.logged_in = True
                return True
        except Exception as e:
            Settings.err_print(e)
            return False

        # if str(Settings.is_cookies()) == "True":
        #     self.cookies_load()
        #     if loggedin_check():
        #         self.logged_in = True
        #         return True
        #     elif str(Settings.is_cookies()) == "True" and str(Settings.is_debug("cookies")) == "True":
        #         Settings.err_print("failed to login from cookies!")
        #         Settings.set_cookies(False)
        #         return False
        #     elif str(Settings.is_cookies()) == "True":
        #         Settings.set_cookies(False)
        #         Settings.maybe_print("failed to login from cookies!")

        Settings.dev_print("attempting login...")
        successful = False
        try:
            if Settings.get_login_method() == "auto":
                successful = via_form()
                if not successful: successful = via_twitter()
                if not successful: successful = via_google()
            elif Settings.get_login_method() == "onlyfans":
                successful = via_form()
            elif Settings.get_login_method() == "twitter":
                successful = via_twitter()
            elif Settings.get_login_method() == "google":
                successful = via_google()
            if successful:
                self.logged_in = True
                return True
        except Exception as e:
            Driver.error_checker(e)
        Settings.err_print("OnlyFans login failed!")
        return False
