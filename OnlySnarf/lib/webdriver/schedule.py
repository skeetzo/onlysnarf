import logging
logger = logging.getLogger(__name__)
from selenium.webdriver.common.by import By

from .element import find_element_to_click
from .errors import error_checker
from ...classes.schedule import Schedule
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
        logger.debug("skipping empty schedule")
        return True
    try:
        logger.info("Schedule:")
        logger.info(f"- Date: {Schedule.format_date(schedule_object['date'])}")
        logger.info(f"- Time: {Schedule.format_time(schedule_object['time'])}")
        schedule_open(browser)
        # individually set month, year, and day
        schedule_date(browser, schedule_object['month'], schedule_object['year'])
        schedule_day(browser, schedule_object['day'])
        schedule_save_date(browser)
        # individually set hour, minutes, and suffix
        schedule_hour(browser, schedule_object['hour'])
        schedule_minutes(browser, schedule_object['minute'])
        schedule_suffix(browser, schedule_object['suffix'])
        logger.debug("saving schedule...")
        if CONFIG["debug"]:
            logger.info("skipping schedule save (debug)")
            return schedule_cancel(browser)
        return schedule_save(browser)
    except Exception as e:
        error_checker(e)
    # attempt to cancel window if reached this far
    try:
        schedule_cancel(browser)
    except Exception as e:
        logger.debug(e)
    return False

def schedule_open(browser):
    """Click schedule"""

    try:
        logger.debug("opening schedule...")
        find_element_to_click(browser, "g-btn.m-flat.b-make-post__datepicker-btn").click()
        logger.debug("sucessfully opened schedule!")
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("failed to open schedule menu!")

def schedule_date(browser, month, year):
    """Find and click month w/ correct date"""

    try:
        logger.debug("setting date...")
        while True:
            date = browser.find_element(By.CLASS_NAME, "vdatetime-calendar__current--month").get_attribute("innerHTML")
            logger.debug(f"date: {date} - {month} {year}")
            if str(month) in str(date) and str(year) in str(date):
                logger.debug("successfully set month and year!")
                debug_delay_check()
                return True
            else:
                find_element_to_click(browser, "vdatetime-calendar__navigation--next").click()
    except Exception as e:
        error_checker(e)
    raise Exception("failed to set schedule date!")

def schedule_day(browser, day):
    """Set day in month"""

    try:
        logger.debug("setting day...")
        # for ele in Driver.find_elements_by_name("vdatetime-calendar__month__day"):
        for ele in browser.find_elements(By.CLASS_NAME, "vdatetime-calendar__month__day"):
            # if str(day) in ele.get_attribute("innerHTML").replace("<span><span>","").replace("</span></span>",""):
            if str(day) in ele.get_attribute("innerHTML"):
                ele.click()
                logger.debug("successfully set day!")
                debug_delay_check()
                return True
    except Exception as e:
        error_checker(e)
    raise Exception("failed to set schedule day!")

def schedule_save_date(browser):
    """Save schedule date and move to next view in frame by hitting next"""
    
    try:
        logger.debug("saving date...")
        find_element_to_click(browser, "g-btn.m-flat.m-reset-width.m-btn-gaps", text="Next").click()
        logger.debug("sucessfully saved date!")
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("failed to save schedule date!")

def schedule_hour(browser, hour):
    """Set schedule hour"""

    try:
        logger.debug("setting hours...")
        eles = browser.find_element(By.CLASS_NAME, "vdatetime-time-picker__list--hours").find_elements(By.XPATH, "./child::*")
        for ele in eles:
            if str(hour) in ele.get_attribute("innerHTML").strip():
                ele.click()
                logger.debug("sucessfully set hour!")
                debug_delay_check()
                return True
    except Exception as e:
        error_checker(e)
    raise Exception("failed to set schedule hour!")

def schedule_minutes(browser, minutes):
    """Set schedule minutes"""

    try:
        logger.debug("setting minutes...")
        eles = browser.find_element(By.CLASS_NAME, "vdatetime-time-picker__list--minutes").find_elements(By.XPATH, "./child::*")
        for ele in eles:
            if str(minutes) in ele.get_attribute("innerHTML").strip():
                ele.click()
                logger.debug("sucessfully set minutes!")
                debug_delay_check()
                return True
    except Exception as e:
        error_checker(e)
    raise Exception("failed to set schedule minutes!")

def schedule_suffix(browser, suffix):
    """Set am/pm suffix"""

    try:
        logger.debug("setting suffix...")
        eles = browser.find_element(By.CLASS_NAME, "vdatetime-time-picker__list--suffix").find_elements(By.XPATH, "./child::*")
        for ele in eles:
            if str(suffix).lower() in ele.get_attribute("innerHTML").strip().lower():
                ele.click()
                logger.debug("sucessfully set suffix!")
                debug_delay_check()
                return True
    except Exception as e:
        error_checker(e)
    raise Exception("failed to set schedule suffix!")

def schedule_cancel(browser):
    """Cancel schedule by clicking cancel"""

    try:
        logger.debug("canceling schedule...")
        browser.find_element(By.CLASS_NAME, "vdatetime-popup__actions__button--cancel").find_elements(By.XPATH, "./child::*")[0].click()
        logger.debug("sucessfully canceled schedule!")
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("failed to cancel schedule menu!")

def schedule_save(browser):
    """Save schedule by clicking save"""

    try:
        logger.debug("saving schedule...")
        browser.find_element(By.CLASS_NAME, "vdatetime-popup__actions__button--confirm").find_elements(By.XPATH, "./child::*")[0].click()
        logger.debug("sucessfully saved schedule!")
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("failed to save schedule menu!")
