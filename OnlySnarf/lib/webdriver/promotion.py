import time
import logging
logger = logging.getLogger(__name__)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from ..util import debug_delay_check
from .. import CONFIG, DEFAULT

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
        logger.error("missing promotion!")
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
        logger.debug("goto -> /my/promotions")
        self.go_to_page("my/promotions")
        logger.debug("checking existing promotion")
        copies = self.browser.find_elements(By.CLASS_NAME, "g-btn.m-rounded.m-uppercase")
        for copy in copies:
            if "copy link to profile" in str(copy.get_attribute("innerHTML")).lower():
            # logger.info("{}".format(copy.get_attribute("innerHTML")))
                copy.click()
                logger.debug("successfully clicked early copy")
                logger.warning("a promotion already exists")
                logger.info("Copied existing promotion")
                return True
        logger.debug("clicking promotion campaign")
        self.find_element_to_click("promotionalCampaign").click()
        logger.debug("successfully clicked promotion campaign")
        # debug_delay_check()
        time.sleep(10)
        # limit dropdown
        logger.debug("setting campaign count")
        limitDropwdown = self.find_element_by_name("promotionalTrialCount")
        for n in range(11): # 11 max subscription limits
            limitDropwdown.send_keys(str(Keys.UP))
        debug_delay_check()
        if limit:
            for n in range(int(limit)):
                limitDropwdown.send_keys(Keys.DOWN)
        logger.debug("successfully set campaign count")
        debug_delay_check()
        # expiration dropdown
        logger.debug("settings campaign expiration")
        expirationDropdown = self.find_element_by_name("promotionalTrialExpiration")
        for n in range(11): # 31 max days
            expirationDropdown.send_keys(str(Keys.UP))
        debug_delay_check()
        if expiration:
            for n in range(int(expiration)):
                expirationDropdown.send_keys(Keys.DOWN)
        logger.debug("successfully set campaign expiration")
        debug_delay_check()
        # duration dropdown
        # LIMIT_ALLOWED = ["1 day","3 days","7 days","14 days","1 month","3 months","6 months","12 months"]
        durationDropdown = self.find_element_by_name("promotionalCampaignAmount")
        logger.debug("entering discount amount")
        for n in range(11):
            durationDropdown.send_keys(str(Keys.UP))
        for n in range(round(int(amount)/5)-1):
            durationDropdown.send_keys(Keys.DOWN)
        logger.debug("successfully entered discount amount")
        # todo: add message to users
        message = self.find_element_by_name("promotionalTrialMessage")
        logger.debug("found message text")
        message.clear()
        logger.debug("sending text")
        message.send_keys(str(text))
        # todo: [] apply to expired subscribers checkbox
        debug_delay_check()
        # find and click promotionalTrialConfirm
        if str(CONFIG["debug"]) == "True":
            logger.debug("finding campaign cancel")
            self.find_element_to_click("promotionalTrialCancel").click()
            logger.debug("skipping promotion (debug)")
            logger.debug("successfully cancelled promotion campaign")
            return True
        logger.debug("finding campaign save")
        # save_ = self.find_element_to_click("promotionalTrialConfirm")
        # save_ = self.find_element_to_click("promotionalCampaignConfirm")
        save_ = self.browser.find_elements(By.CLASS_NAME, "g-btn.m-rounded")
        for save__ in save_:
            logger.info(save__.get_attribute("innerHTML"))
        if len(save_) == 0:
            logger.debug("unable to find promotion 'Create'")
            logger.error("unable to save promotion")
            return False
        for save__ in save_:
            if save__.get_attribute("innerHTML").lower().strip() == "create":
                save_ = save__    
        logger.info(save_.get_attribute("innerHTML"))
        logger.debug("saving promotion")
        save_.click()
        logger.debug("successfully saved promotion")
        logger.debug("successful promotion campaign")
        # todo: add copy link to profile
        debug_delay_check()
        logger.debug("clicking copy")
        copies = self.browser.find_elements(By.CLASS_NAME, "g-btn.m-rounded.m-uppercase")
        for copy in copies:
            logger.info("{}".format(copy.get_attribute("innerHTML")))
            if "copy link to profile" in str(copy.get_attribute("innerHTML")).lower():
                copy.click()
                logger.debug("successfully clicked copy")
        return True
    except Exception as e:
        Driver.error_checker(e)
        logger.error("failed to apply promotion")
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
        logger.error("missing promotion")
        return False
    # go to onlyfans.com/my/subscribers/active
    try:
        promotion.get()
        limit = promotion["limit"]
        expiration = promotion["expiration"]
        duration = promotion["duration"]
        user = promotion["user"]
        logger.debug("goto -> /my/promotions")
        self.go_to_page("/my/promotions")
        logger.debug("showing promotional trial link")
        self.find_element_to_click("promotionalTrialShow").click()
        logger.debug("successfully showed promotional trial link")
        logger.debug("creating promotional trial")
        self.find_element_to_click("promotionalTrial").click()
        logger.debug("successfully clicked promotional trial")
        # limit dropdown
        logger.debug("setting trial count")
        limitDropwdown = self.find_element_by_name("promotionalTrialCount")
        for n in range(11): # 11 max subscription limits
            limitDropwdown.send_keys(str(Keys.UP))
        debug_delay_check()
        if limit:
            for n in range(int(limit)):
                limitDropwdown.send_keys(Keys.DOWN)
        logger.debug("successfully set trial count")
        debug_delay_check()
        # expiration dropdown
        logger.debug("settings trial expiration")
        expirationDropdown = self.find_element_by_name("promotionalTrialExpiration")
        for n in range(11): # 31 max days
            expirationDropdown.send_keys(str(Keys.UP))
        debug_delay_check()
        if expiration:
            for n in range(int(expiration)):
                expirationDropdown.send_keys(Keys.DOWN)
        logger.debug("successfully set trial expiration")
        debug_delay_check()
        # duration dropdown
        # LIMIT_ALLOWED = ["1 day","3 days","7 days","14 days","1 month","3 months","6 months","12 months"]
        logger.debug("settings trial duration")
        durationDropwdown = self.find_element_by_name("promotionalTrialDuration")
        for n in range(11):
            durationDropwdown.send_keys(str(Keys.UP))
        debug_delay_check()
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
        logger.debug("successfully set trial duration")
        debug_delay_check()
        # find and click promotionalTrialConfirm
        # if CONFIG["debug"]:
        #     logger.debug("finding trial cancel")
        #     self.find_element_to_click("promotionalTrialCancel").click()
        #     logger.info("skipping: Promotion (debug)")
        #     logger.debug("successfully cancelled promotion trial")
        #     return True
        logger.debug("finding trial save")
        save_ = self.find_element_to_click("promotionalTrialConfirm")
        # "g-btn.m-rounded"

        save_ = self.browser.find_elements(By.CLASS_NAME, "g-btn.m-rounded")
        for save__ in save_:
            logger.info(save__.get_attribute("innerHTML"))
        if len(save_) == 0:
            logger.debug("unable to find promotion 'Create'")
            logger.error("unable to save promotion")
            return False
        for save__ in save_:
            if save__.get_attribute("innerHTML").lower().strip() == "create":
                save_ = save__    
        logger.info(save_.get_attribute("innerHTML"))
        logger.debug("saving promotion")
        save_.click()
        logger.debug("successfully saved promotion")
        ## TODO ##
        # finish this
        link = ""
        # logger.debug("copying trial link")
        # self.find_element_by_name("promotionalTrialLink").click()
        # logger.debug("successfully copied trial link")

        # in order for this to work accurately i need to figure out the number of trial things already on the page
        # then find the new trial thing
        # then get the link for the new trial thing
        # as of now it creates a new trial for the x duration so voila

        # todo maybe probably never:
        # go to /home
        # enter copied paste into new post
        # get text in new post
        # email link to user

        logger.debug("successful promotion trial")
        debug_delay_check()
        return link
    except Exception as e:
        Driver.error_checker(e)
        logger.error("failed to apply promotion")
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
        logger.error("missing promotion")
        return False
    # go to onlyfans.com/my/subscribers/active
    promotion.get()
    expiration = promotion["expiration"]
    months = promotion["duration"]
    user = promotion["user"]
    message = promotion["message"]

    # TODO: replace with defaults
    # if int(expiration) > int(Settings.get_discount_max_amount()):
    #     logger.warning("discount too high, max -> {}%".format(Settings.get_discount_max_amount()))
    #     discount = Settings.get_discount_max_amount()
    # elif int(expiration) > int(Settings.get_discount_min_amount()):
    #     logger.warning("discount too low, min -> {}%".format(Settings.get_discount_min_amount()))
    #     discount = Settings.get_discount_min_amount()
    # if int(months) > int(Settings.get_discount_max_months()):
    #     logger.warning("duration too high, max -> {} days".format(Settings.get_discount_max_months()))
    #     months = Settings.get_discount_max_months()
    # elif int(months) < int(Settings.get_discount_min_months()):
    #     logger.warning("duration too low, min -> {} days".format(Settings.get_discount_min_months()))
    #     months = Settings.get_discount_min_months()
    
    try:
        logger.debug("goto -> /{}".format(user))
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
        logger.debug("entering expiration")
        for n in range(11):
            expirations.send_keys(str(Keys.UP))
        for n in range(round(int(expiration)/5)-1):
            expirations.send_keys(Keys.DOWN)
        logger.debug("successfully entered expiration")
        logger.debug("entering duration")
        for n in range(11):
            durations.send_keys(str(Keys.UP))
        for n in range(int(months)-1):
            durations.send_keys(Keys.DOWN)
        logger.debug("successfully entered duration")
        debug_delay_check()
        logger.debug("entering message")
        message.clear()
        message.send_keys(message)
        logger.debug("successfully entered message")
        logger.debug("applying discount")
        save = self.find_element_by_name("promotionalTrialApply")
        if str(CONFIG["debug"]) == "True":
            self.find_element_by_name("promotionalTrialCancel").click()
            logger.debug("skipping save discount (debug)")
            logger.debug("successfully canceled discount")
            cancel.click()
            return True
        save.click()
        logger.info("discounted: {}".format(user.username))
        logger.debug("### User Discount Successful ###")
        return True
    except Exception as e:
        Driver.error_checker(e)
        try:
            self.find_element_by_name("promotionalTrialCancel").click()
            logger.debug("### Discount Successful Failure ###")
            return False
        except Exception as e:
            Driver.error_checker(e)
        logger.debug("### Discount Failure ###")
        return False
