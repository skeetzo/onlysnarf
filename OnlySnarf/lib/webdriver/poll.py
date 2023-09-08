import time
import logging
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .element import find_element_to_click
from .. import CONFIG, debug_delay_check

################
##### Poll #####
################

def poll(browser, poll_object={}):
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
        logging.debug("skipping empty poll")
        return True
    try:
        logging.info("Poll:")
        open_poll_model(browser)        
        add_poll_duration(browser, poll_object["duration"])
        add_poll_questions(browser, poll_object["questions"])
        if CONFIG["debug"]:
            logging.debug("skipping poll (debug)")
            find_element_to_click(browser, "b-dropzone__preview__delete", text="Cancel").click()
        logging.debug("### Poll Successful ###")
        return True
    except Exception as e:
        Driver.error_checker(e)
        logging.error("failed to enter poll!")
    return False

# open the poll duration
# can click anywhere near the top label
# TODO: finish updating any inserted wait times to be more dynamic
def add_poll_duration(browser, duration, wait=1):
    logging.info("- Duration: {}".format(duration))
    logging.debug("setting duration")
    action = ActionChains(browser)
    action.click(on_element=browser.find_element(By.CLASS_NAME, "b-post-piece__value"))
    action.pause(int(wait))
    action.send_keys(Keys.TAB)
    action.send_keys(str(duration))
    action.perform()
    # save the duration
    logging.debug("saving duration")
    find_element_to_click(browser, "g-btn.m-flat.m-btn-gaps.m-reset-width", text="Save").click()
    logging.debug("successfully saved duration")
    debug_delay_check()

def add_poll_questions(browser, questions):
    logging.debug("configuring question paths...")
    questionsElement = browser.find_elements(By.CLASS_NAME, "v-text-field__slot")
    # add extra question space
    OFFSET = 2 # number of preexisting questionsElement
    if OFFSET + len(questions) > len(questionsElement):
        for i in range(OFFSET + len(questions)-len(questionsElement)):
            logging.debug("adding question...")
            find_element_to_click(browser, "g-btn.m-flat.new_vote_add_option").click()
            logging.debug("added question")
    # find the question inputs again
    questionsElement = browser.find_elements(By.CLASS_NAME, "v-text-field__slot")
    logging.debug("question paths: {}".format(len(questionsElement)))
    # enter the questions
    i = 0
    logging.debug("questions: {}".format(questions))
    logging.info("- Questions:")
    for question in list(questions):
        logging.info("> {}".format(question))
        logging.debug("entering question: {}".format(question))
        questionsElement[i].find_elements(By.XPATH, "./child::*")[0].send_keys(str(question))
        logging.debug("entered question")
        time.sleep(1)
        i+=1
    logging.debug("successfully entered questions")
    debug_delay_check()

# open the poll model
def open_poll_model(browser):
    logging.debug("adding poll")
    elements = browser.find_elements(By.TAG_NAME, "use")
    element = [elem for elem in elements if '#icon-poll' in str(elem.get_attribute('href'))][0]
    ActionChains(browser).move_to_element(element).click().perform()
    time.sleep(1)
    debug_delay_check()
