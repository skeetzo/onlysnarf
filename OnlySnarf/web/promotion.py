
from ..util.settings import Settings

# TODO: last

######################
##### Promotions #####
######################

def promotional_campaign(self, promotion=None):
    """
    Enter the promotion as a campaign.

    Parameters
    ----------
    promotion : classes.Promotion
        The promotion to enter as a campaign

    Returns
    -------
    bool
        Whether or not the promotion was successful

    """

    if not promotion:
        Settings.err_print("missing promotion!")
        return False
    # go to onlyfans.com/my/subscribers/active
    try:
        promotion.get()
        limit = promotion["limit"]
        expiration = promotion["expiration"]
        duration = promotion["duration"]
        # user = promotion["user"]
        amount = promotion["amount"]
        text = promotion["message"]
        Settings.maybe_print("goto -> /my/promotions")
        self.go_to_page("my/promotions")
        Settings.dev_print("checking existing promotion")
        copies = self.browser.find_elements(By.CLASS_NAME, "g-btn.m-rounded.m-uppercase")
        for copy in copies:
            if "copy link to profile" in str(copy.get_attribute("innerHTML")).lower():
            # Settings.print("{}".format(copy.get_attribute("innerHTML")))
                copy.click()
                Settings.dev_print("successfully clicked early copy")
                Settings.warn_print("a promotion already exists")
                Settings.print("Copied existing promotion")
                return True
        Settings.dev_print("clicking promotion campaign")
        self.find_element_to_click("promotionalCampaign").click()
        Settings.dev_print("successfully clicked promotion campaign")
        # Settings.debug_delay_check()
        time.sleep(10)
        # limit dropdown
        Settings.dev_print("setting campaign count")
        limitDropwdown = self.find_element_by_name("promotionalTrialCount")
        for n in range(11): # 11 max subscription limits
            limitDropwdown.send_keys(str(Keys.UP))
        Settings.debug_delay_check()
        if limit:
            for n in range(int(limit)):
                limitDropwdown.send_keys(Keys.DOWN)
        Settings.dev_print("successfully set campaign count")
        Settings.debug_delay_check()
        # expiration dropdown
        Settings.dev_print("settings campaign expiration")
        expirationDropdown = self.find_element_by_name("promotionalTrialExpiration")
        for n in range(11): # 31 max days
            expirationDropdown.send_keys(str(Keys.UP))
        Settings.debug_delay_check()
        if expiration:
            for n in range(int(expiration)):
                expirationDropdown.send_keys(Keys.DOWN)
        Settings.dev_print("successfully set campaign expiration")
        Settings.debug_delay_check()
        # duration dropdown
        # LIMIT_ALLOWED = ["1 day","3 days","7 days","14 days","1 month","3 months","6 months","12 months"]
        durationDropdown = self.find_element_by_name("promotionalCampaignAmount")
        Settings.dev_print("entering discount amount")
        for n in range(11):
            durationDropdown.send_keys(str(Keys.UP))
        for n in range(round(int(amount)/5)-1):
            durationDropdown.send_keys(Keys.DOWN)
        Settings.dev_print("successfully entered discount amount")
        # todo: add message to users
        message = self.find_element_by_name("promotionalTrialMessage")
        Settings.dev_print("found message text")
        message.clear()
        Settings.dev_print("sending text")
        message.send_keys(str(text))
        # todo: [] apply to expired subscribers checkbox
        Settings.debug_delay_check()
        # find and click promotionalTrialConfirm
        if str(Settings.is_debug()) == "True":
            Settings.dev_print("finding campaign cancel")
            self.find_element_to_click("promotionalTrialCancel").click()
            Settings.maybe_print("skipping promotion (debug)")
            Settings.dev_print("successfully cancelled promotion campaign")
            return True
        Settings.dev_print("finding campaign save")
        # save_ = self.find_element_to_click("promotionalTrialConfirm")
        # save_ = self.find_element_to_click("promotionalCampaignConfirm")
        save_ = self.browser.find_elements(By.CLASS_NAME, "g-btn.m-rounded")
        for save__ in save_:
            Settings.print(save__.get_attribute("innerHTML"))
        if len(save_) == 0:
            Settings.dev_print("unable to find promotion 'Create'")
            Settings.err_print("unable to save promotion")
            return False
        for save__ in save_:
            if save__.get_attribute("innerHTML").lower().strip() == "create":
                save_ = save__    
        Settings.print(save_.get_attribute("innerHTML"))
        Settings.dev_print("saving promotion")
        save_.click()
        Settings.dev_print("successfully saved promotion")
        Settings.dev_print("successful promotion campaign")
        # todo: add copy link to profile
        Settings.debug_delay_check()
        Settings.dev_print("clicking copy")
        copies = self.browser.find_elements(By.CLASS_NAME, "g-btn.m-rounded.m-uppercase")
        for copy in copies:
            Settings.print("{}".format(copy.get_attribute("innerHTML")))
            if "copy link to profile" in str(copy.get_attribute("innerHTML")).lower():
                copy.click()
                Settings.dev_print("successfully clicked copy")
        return True
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("failed to apply promotion")
        return None

# or email
def promotional_trial_link(self, promotion=None):
    """
    Enter the promotion as a trial link

    Parameters
    ----------
    promotion : classes.Promotion
        The promotion to enter as a link

    Returns
    -------
    bool
        Whether or not the promotion was successful

    """

    if not promotion:
        Settings.err_print("missing promotion")
        return False
    # go to onlyfans.com/my/subscribers/active
    try:
        promotion.get()
        limit = promotion["limit"]
        expiration = promotion["expiration"]
        duration = promotion["duration"]
        user = promotion["user"]
        Settings.maybe_print("goto -> /my/promotions")
        self.go_to_page("/my/promotions")
        Settings.dev_print("showing promotional trial link")
        self.find_element_to_click("promotionalTrialShow").click()
        Settings.dev_print("successfully showed promotional trial link")
        Settings.dev_print("creating promotional trial")
        self.find_element_to_click("promotionalTrial").click()
        Settings.dev_print("successfully clicked promotional trial")
        # limit dropdown
        Settings.dev_print("setting trial count")
        limitDropwdown = self.find_element_by_name("promotionalTrialCount")
        for n in range(11): # 11 max subscription limits
            limitDropwdown.send_keys(str(Keys.UP))
        Settings.debug_delay_check()
        if limit:
            for n in range(int(limit)):
                limitDropwdown.send_keys(Keys.DOWN)
        Settings.dev_print("successfully set trial count")
        Settings.debug_delay_check()
        # expiration dropdown
        Settings.dev_print("settings trial expiration")
        expirationDropdown = self.find_element_by_name("promotionalTrialExpiration")
        for n in range(11): # 31 max days
            expirationDropdown.send_keys(str(Keys.UP))
        Settings.debug_delay_check()
        if expiration:
            for n in range(int(expiration)):
                expirationDropdown.send_keys(Keys.DOWN)
        Settings.dev_print("successfully set trial expiration")
        Settings.debug_delay_check()
        # duration dropdown
        # LIMIT_ALLOWED = ["1 day","3 days","7 days","14 days","1 month","3 months","6 months","12 months"]
        Settings.dev_print("settings trial duration")
        durationDropwdown = self.find_element_by_name("promotionalTrialDuration")
        for n in range(11):
            durationDropwdown.send_keys(str(Keys.UP))
        Settings.debug_delay_check()
        num = 1
        if str(duration) == "1 day": num = 1
        if str(duration) == "3 day": num = 2
        if str(duration) == "7 days": num = 3
        if str(duration) == "14 days": num = 4
        if str(duration) == "1 month": num = 5
        if str(duration) == "3 months": num = 6
        if str(duration) == "6 months": num = 7
        if str(duration) == "12 months": num = 8
        for n in range(int(num)-1):
            durationDropwdown.send_keys(Keys.DOWN)
        Settings.dev_print("successfully set trial duration")
        Settings.debug_delay_check()
        # find and click promotionalTrialConfirm
        # if Settings.is_debug():
        #     Settings.dev_print("finding trial cancel")
        #     self.find_element_to_click("promotionalTrialCancel").click()
        #     Settings.print("skipping: Promotion (debug)")
        #     Settings.dev_print("successfully cancelled promotion trial")
        #     return True
        Settings.dev_print("finding trial save")
        save_ = self.find_element_to_click("promotionalTrialConfirm")
        # "g-btn.m-rounded"

        save_ = self.browser.find_elements(By.CLASS_NAME, "g-btn.m-rounded")
        for save__ in save_:
            Settings.print(save__.get_attribute("innerHTML"))
        if len(save_) == 0:
            Settings.dev_print("unable to find promotion 'Create'")
            Settings.err_print("unable to save promotion")
            return False
        for save__ in save_:
            if save__.get_attribute("innerHTML").lower().strip() == "create":
                save_ = save__    
        Settings.print(save_.get_attribute("innerHTML"))
        Settings.dev_print("saving promotion")
        save_.click()
        Settings.dev_print("successfully saved promotion")
        ## TODO ##
        # finish this
        link = ""
        # Settings.dev_print("copying trial link")
        # self.find_element_by_name("promotionalTrialLink").click()
        # Settings.dev_print("successfully copied trial link")

        # in order for this to work accurately i need to figure out the number of trial things already on the page
        # then find the new trial thing
        # then get the link for the new trial thing
        # as of now it creates a new trial for the x duration so voila

        # todo maybe probably never:
        # go to /home
        # enter copied paste into new post
        # get text in new post
        # email link to user

        Settings.dev_print("successful promotion trial")
        Settings.debug_delay_check()
        return link
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("failed to apply promotion")
        return None

def promotion_user_directly(self, promotion=None):
    """
    Apply the promotion directly to the user.

    Parameters
    ----------
    promotion : classes.Promotion
        The promotion to provide to the user

    Returns
    -------
    bool
        Whether or not the promotion was successful

    """

    if not promotion:
        Settings.err_print("missing promotion")
        return False
    # go to onlyfans.com/my/subscribers/active
    promotion.get()
    expiration = promotion["expiration"]
    months = promotion["duration"]
    user = promotion["user"]
    message = promotion["message"]
    if int(expiration) > int(Settings.get_discount_max_amount()):
        Settings.warn_print("discount too high, max -> {}%".format(Settings.get_discount_max_amount()))
        discount = Settings.get_discount_max_amount()
    elif int(expiration) > int(Settings.get_discount_min_amount()):
        Settings.warn_print("discount too low, min -> {}%".format(Settings.get_discount_min_amount()))
        discount = Settings.get_discount_min_amount()
    if int(months) > int(Settings.get_discount_max_months()):
        Settings.warn_print("duration too high, max -> {} days".format(Settings.get_discount_max_months()))
        months = Settings.get_discount_max_months()
    elif int(months) < int(Settings.get_discount_min_months()):
        Settings.warn_print("duration too low, min -> {} days".format(Settings.get_discount_min_months()))
        months = Settings.get_discount_min_months()
    try:
        Settings.maybe_print("goto -> /{}".format(user))
        self.go_to_page(user)
        # click discount button
        self.find_element_to_click("discountUserPromotion").click()
        # enter expiration
        expirations = self.find_element_by_name("promotionalTrialExpirationUser")
        # enter duration
        durations = self.find_element_by_name("promotionalTrialDurationUser")
        # enter message
        message = self.find_element_by_name("promotionalTrialMessageUser")
        # save
        Settings.dev_print("entering expiration")
        for n in range(11):
            expirations.send_keys(str(Keys.UP))
        for n in range(round(int(expiration)/5)-1):
            expirations.send_keys(Keys.DOWN)
        Settings.dev_print("successfully entered expiration")
        Settings.dev_print("entering duration")
        for n in range(11):
            durations.send_keys(str(Keys.UP))
        for n in range(int(months)-1):
            durations.send_keys(Keys.DOWN)
        Settings.dev_print("successfully entered duration")
        Settings.debug_delay_check()
        Settings.dev_print("entering message")
        message.clear()
        message.send_keys(message)
        Settings.dev_print("successfully entered message")
        Settings.dev_print("applying discount")
        save = self.find_element_by_name("promotionalTrialApply")
        if str(Settings.is_debug()) == "True":
            self.find_element_by_name("promotionalTrialCancel").click()
            Settings.maybe_print("skipping save discount (debug)")
            Settings.dev_print("successfully canceled discount")
            cancel.click()
            return True
        save.click()
        Settings.print("discounted: {}".format(user.username))
        Settings.dev_print("### User Discount Successful ###")
        return True
    except Exception as e:
        Driver.error_checker(e)
        try:
            self.find_element_by_name("promotionalTrialCancel").click()
            Settings.dev_print("### Discount Successful Failure ###")
            return False
        except Exception as e:
            Driver.error_checker(e)
        Settings.dev_print("### Discount Failure ###")
        return False
