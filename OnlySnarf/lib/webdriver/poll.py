import time
import logging
logger = logging.getLogger(__name__)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .element import find_element_to_click
from .errors import error_checker
from .message import click_close_icons
from .. import CONFIG, debug_delay_check

################
##### Poll #####
################

def poll(browser, poll_object):
    """
    Enter the Poll object into the current post

    Parameters
    ----------
    poll : dict
        The values of the poll in a dict

    Returns
    -------
    bool
        Whether or not entering the poll was successful

    """

    if not poll_object or len(poll_object["questions"]) == 0:
        logger.debug("skipping empty poll")
        return True
    try:
        logger.info("Poll:")
        open_poll_model(browser)
        add_poll_duration(browser, poll_object["duration"])
        add_poll_questions(browser, poll_object["questions"])
        if CONFIG["debug"]:
            logger.debug("skipping poll save (debug)")
            click_close_icons(browser)
        logger.debug("poll successful!")
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("failed to enter poll!")

# open the poll duration
# can click anywhere near the top label
# TODO: finish updating any inserted wait times to be more dynamic
def add_poll_duration(browser, duration, wait=1):
    try:
        logger.info("- Duration: {}".format(duration))
        logger.debug("setting duration")
        action = ActionChains(browser)
        action.click(on_element=browser.find_element(By.CLASS_NAME, "b-post-piece__value"))
        action.pause(int(wait))
        action.send_keys(Keys.TAB)
        action.send_keys(str(duration))
        action.perform()
        # save the duration
        logger.debug("saving duration")
        find_element_to_click(browser, "g-btn.m-flat.m-btn-gaps.m-reset-width", text="Save").click()
        logger.debug("successfully saved duration")
        debug_delay_check()
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("unable to add poll duration!")

def add_poll_questions(browser, questions):
    try:
        logger.debug("configuring question paths...")
        questionsElement = browser.find_elements(By.CLASS_NAME, "v-text-field__slot")
        # add extra question space
        OFFSET = 2 # number of preexisting questionsElement
        if OFFSET + len(questions) > len(questionsElement):
            for i in range(OFFSET + len(questions)-len(questionsElement)):
                logger.debug("adding question...")
                find_element_to_click(browser, "g-btn.m-flat.new_vote_add_option").click()
                logger.debug("added question")
        # find the question inputs again
        questionsElement = browser.find_elements(By.CLASS_NAME, "v-text-field__slot")
        logger.debug("question paths: {}".format(len(questionsElement)))
        # enter the questions
        i = 0
        logger.debug("questions: {}".format(questions))
        logger.info("- Questions:")
        for question in list(questions):
            logger.info("> {}".format(question))
            logger.debug("entering question: {}".format(question))
            questionsElement[i].find_elements(By.XPATH, "./child::*")[0].send_keys(str(question))
            logger.debug("entered question")
            time.sleep(0.5)
            i+=1
        logger.debug("successfully entered questions!")
        debug_delay_check()
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("unable to add poll questions!")

# open the poll model
def open_poll_model(browser):
    try:
        logger.debug("adding poll..")
        for element in browser.find_element(By.CLASS_NAME, "b-make-post__actions__btns").find_elements(By.XPATH, "./child::*"):
            if "icon-poll" in str(element.get_attribute("innerHTML")):
                logger.debug("clicking poll button...")
                browser.execute_script("arguments[0].click()", element)
                return True
        # elements = browser.find_elements(By.TAG_NAME, "use")
        # element = [elem for elem in elements if '#icon-poll' in str(elem.get_attribute('href'))][0]
        # ActionChains(browser).move_to_element(element).click().perform()
        logger.debug("successfully opened poll menu!")
        debug_delay_check()
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("unable to open poll menu!")
