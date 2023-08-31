import logging
from selenium.webdriver.common.by import By

from .element import find_element_to_click
from ..schedule import Schedule
from .. import CONFIG, debug_delay_check

####################
##### Schedule #####
####################

def schedule(browser, schedule_object={}):
    """
    Enter the provided schedule

    Parameters
    ----------
    schedule : dict
        The schedule object containing the values to enter

    Returns
    -------
    bool
        Whether or not the schedule was entered successfully

    """

    if not schedule_object:
        logging.debug("skipping empty schedule")
        return True
    try:
        logging.info("Schedule:")
        logging.info(f"- Date: {Schedule.format_date(schedule_object['date'])}")
        logging.info(f"- Time: {Schedule.format_time(schedule_object['time'])}")

        # TODO: fix
        ## BUG: tries twice to solve whatever issue is occurring
        ## disabled since no access to "self" aka driver object, add import workaround?
        # try:
        #     self.schedule_open()
        # except Exception as e:
        #     logging.debug(e)
        #     logging.debug("## SCHEDULE BUG ##")
        #     logging.debug("attempting to circumvent scheduling bug...")
        #     self.go_to_home()
        #     self.schedule_open()
        ##

        schedule_open(browser)
        # individually set month, year, and day
        if not self.schedule_date(browser, schedule_object['month'], schedule_object['year']):
            raise Exception("failed to enter date!")
        if not self.schedule_day(schedule_object['day']):
            raise Exception("failed to enter day!")
        self.schedule_save_date(browser)
        # individually set hour, minutes, and suffix
        if not self.schedule_hour(browser, schedule_object['hour']):
            raise Exception("failed to enter hour!")
        if not self.schedule_minutes(browser, schedule_object['minute']):
            raise Exception("failed to enter minutes!")
        if not self.schedule_suffix(browser, schedule_object['suffix']):
            raise Exception("failed to enter suffix!")
        logging.debug("saving schedule...")
        if CONFIG["debug"]:
            logging.info("skipping schedule save (debug)")
            return self.schedule_cancel(browser)
        return self.schedule_save(browser)
    except Exception as e:
        Driver.error_checker(e)
    # attempt to cancel window if reached this far
    return self.schedule_cancel(browser)

def schedule_open(browser):
    """Click schedule"""

    logging.debug("opening schedule...")
    find_element_to_click(browser, "g-btn.m-flat.b-make-post__datepicker-btn").click()
    logging.debug("opened schedule")

def schedule_date(browser, month, year):
    """Find and click month w/ correct date"""

    logging.debug("setting date...")
    while True:
        date = browser.find_element(By.CLASS_NAME, "vdatetime-calendar__current--month").get_attribute("innerHTML")
        logging.debug(f"date: {date} - {month} {year}")
        if str(month) in str(date) and str(year) in str(date):
            logging.debug("set month and year")
            debug_delay_check()
            return True
        else:
            find_element_to_click(browser, "vdatetime-calendar__navigation--next").click()
    return False

def schedule_day(browser, day):
    """Set day in month"""

    logging.debug("setting day...")
    for ele in Driver.find_elements_by_name("vdatetime-calendar__month__day"):
        if str(day) in ele.get_attribute("innerHTML").replace("<span><span>","").replace("</span></span>",""):
            ele.click()
            logging.debug("set day")
            debug_delay_check()
            return True
    return False

def schedule_save_date(browser):
    """Save schedule date and move to next view in frame by hitting next"""
    
    find_element_to_click(browser, "g-btn.m-flat.m-reset-width.m-btn-gaps", text="Next").click()
    logging.debug("saved date")

def schedule_hour(browser, hour):
    """Set schedule hour"""

    logging.debug("setting hours...")
    eles = browser.find_element(By.CLASS_NAME, "vdatetime-time-picker__list--hours").find_elements(By.XPATH, "./child::*")
    for ele in eles:
        if str(hour) in ele.get_attribute("innerHTML").strip():
            ele.click()
            logging.debug("set hour")
            debug_delay_check()
            return True
    return False

def schedule_minutes(browser, minutes):
    """Set schedule minutes"""

    logging.debug("setting minutes...")
    eles = browser.find_element(By.CLASS_NAME, "vdatetime-time-picker__list--minutes").find_elements(By.XPATH, "./child::*")
    for ele in eles:
        if str(minutes) in ele.get_attribute("innerHTML").strip():
            ele.click()
            logging.debug("set minutes")
            debug_delay_check()
            return True
    return False

def schedule_suffix(browser, suffix):
    """Set am/pm suffix"""

    logging.debug("setting suffix...")
    eles = browser.find_element(By.CLASS_NAME, "vdatetime-time-picker__list--suffix").find_elements(By.XPATH, "./child::*")
    for ele in eles:
        if str(suffix).lower() in ele.get_attribute("innerHTML").strip().lower():
            ele.click()
            logging.debug("set suffix")
            debug_delay_check()
            return True
    return False

def schedule_cancel(browser):
    """Cancel schedule by clicking cancel"""

    logging.debug("canceling schedule...")
    browser.find_element(By.CLASS_NAME, "vdatetime-popup__actions__button--cancel").find_elements(By.XPATH, "./child::*")[0].click()
    logging.info("Canceled schedule!")
    return True

def schedule_save(browser):
    """Save schedule by clicking save"""

    logging.debug("saving schedule...")
    browser.find_element(By.CLASS_NAME, "vdatetime-popup__actions__button--confirm").find_elements(By.XPATH, "./child::*")[0].click()
    logging.info("Saved schedule!")
    return True
