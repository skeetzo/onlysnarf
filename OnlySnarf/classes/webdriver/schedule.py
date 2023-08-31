
from .element import find_element_to_click
from ..util import debug_delay_check
from .. import Settings

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
        Settings.dev_print("skipping empty schedule")
        return True
    try:
        Settings.print("Schedule:")
        Settings.print(f"- Date: {Settings.format_date(schedule_object['date'])}")
        Settings.print(f"- Time: {Settings.format_time(schedule_object['time'])}")

        # TODO: fix
        ## BUG: tries twice to solve whatever issue is occurring
        ## disabled since no access to "self" aka driver object, add import workaround?
        # try:
        #     self.schedule_open()
        # except Exception as e:
        #     Settings.dev_print(e)
        #     Settings.dev_print("## SCHEDULE BUG ##")
        #     Settings.maybe_print("attempting to circumvent scheduling bug...")
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
        Settings.dev_print("saving schedule...")
        if CONFIG["debug"]:
            Settings.print("skipping schedule save (debug)")
            return self.schedule_cancel(browser)
        return self.schedule_save(browser)
    except Exception as e:
        Driver.error_checker(e)
    # attempt to cancel window if reached this far
    return self.schedule_cancel(browser)

def schedule_open(browser):
    """Click schedule"""

    Settings.dev_print("opening schedule...")
    find_element_to_click(browser, "g-btn.m-flat.b-make-post__datepicker-btn").click()
    Settings.dev_print("opened schedule")

def schedule_date(browser, month, year):
    """Find and click month w/ correct date"""

    Settings.dev_print("setting date...")
    while True:
        date = browser.find_element(By.CLASS_NAME, "vdatetime-calendar__current--month").get_attribute("innerHTML")
        Settings.dev_print(f"date: {date} - {month} {year}")
        if str(month) in str(date) and str(year) in str(date):
            Settings.dev_print("set month and year")
            debug_delay_check()
            return True
        else:
            find_element_to_click(browser, "vdatetime-calendar__navigation--next").click()
    return False

def schedule_day(browser, day):
    """Set day in month"""

    Settings.dev_print("setting day...")
    for ele in Driver.find_elements_by_name("vdatetime-calendar__month__day"):
        if str(day) in ele.get_attribute("innerHTML").replace("<span><span>","").replace("</span></span>",""):
            ele.click()
            Settings.dev_print("set day")
            debug_delay_check()
            return True
    return False

def schedule_save_date(browser):
    """Save schedule date and move to next view in frame by hitting next"""
    
    find_element_to_click(browser, "g-btn.m-flat.m-reset-width.m-btn-gaps", text="Next").click()
    Settings.dev_print("saved date")

def schedule_hour(browser, hour):
    """Set schedule hour"""

    Settings.dev_print("setting hours...")
    eles = browser.find_element(By.CLASS_NAME, "vdatetime-time-picker__list--hours").find_elements(By.XPATH, "./child::*")
    for ele in eles:
        if str(hour) in ele.get_attribute("innerHTML").strip():
            ele.click()
            Settings.dev_print("set hour")
            debug_delay_check()
            return True
    return False

def schedule_minutes(browser, minutes):
    """Set schedule minutes"""

    Settings.dev_print("setting minutes...")
    eles = browser.find_element(By.CLASS_NAME, "vdatetime-time-picker__list--minutes").find_elements(By.XPATH, "./child::*")
    for ele in eles:
        if str(minutes) in ele.get_attribute("innerHTML").strip():
            ele.click()
            Settings.dev_print("set minutes")
            debug_delay_check()
            return True
    return False

def schedule_suffix(browser, suffix):
    """Set am/pm suffix"""

    Settings.dev_print("setting suffix...")
    eles = browser.find_element(By.CLASS_NAME, "vdatetime-time-picker__list--suffix").find_elements(By.XPATH, "./child::*")
    for ele in eles:
        if str(suffix).lower() in ele.get_attribute("innerHTML").strip().lower():
            ele.click()
            Settings.dev_print("set suffix")
            debug_delay_check()
            return True
    return False

def schedule_cancel(browser):
    """Cancel schedule by clicking cancel"""

    Settings.dev_print("canceling schedule...")
    browser.find_element(By.CLASS_NAME, "vdatetime-popup__actions__button--cancel").find_elements(By.XPATH, "./child::*")[0].click()
    Settings.print("Canceled schedule!")
    return True

def schedule_save(browser):
    """Save schedule by clicking save"""

    Settings.dev_print("saving schedule...")
    browser.find_element(By.CLASS_NAME, "vdatetime-popup__actions__button--confirm").find_elements(By.XPATH, "./child::*")[0].click()
    Settings.print("Saved schedule!")
    return True
