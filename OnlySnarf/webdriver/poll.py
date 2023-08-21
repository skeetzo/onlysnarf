
from .element import find_element_to_click
from ..classes.poll import Poll
from ..util.settings import Settings

################
##### Poll #####
################

def poll(browser, poll_object=Poll()):
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

    if not poll_object:
        Settings.dev_print("skipping empty poll")
        return True
    try:
        Settings.print("Poll:")
        open_poll_model(browser)        
        add_poll_duration(browser, poll_object["duration"])
        add_poll_questions(browser, poll_object["questions"])
        if Settings.is_debug():
            Settings.maybe_print("skipping poll (debug)")
            find_element_to_click(browser, "b-dropzone__preview__delete", text="Cancel").click()
        Settings.dev_print("### Poll Successful ###")
        return True
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("failed to enter poll!")
    return False

# open the poll duration
# can click anywhere near the top label
# TODO: finish updating any inserted wait times to be more dynamic
def add_poll_duration(browser, duration, wait=1):
    Settings.print("- Duration: {}".format(duration))
    Settings.dev_print("setting duration")
    action = ActionChains(browser)
    action.click(on_element=browser.find_element(By.CLASS_NAME, "b-post-piece__value"))
    action.pause(int(wait))
    action.send_keys(Keys.TAB)
    action.send_keys(str(duration))
    action.perform()
    # save the duration
    Settings.dev_print("saving duration")
    find_element_to_click(browser, "g-btn.m-flat.m-btn-gaps.m-reset-width", text="Save").click()
    Settings.dev_print("successfully saved duration")
    Settings.debug_delay_check()

def add_poll_questions(browser, questions):
    Settings.dev_print("configuring question paths...")
    questionsElement = browser.find_elements(By.CLASS_NAME, "v-text-field__slot")
    # add extra question space
    OFFSET = 2 # number of preexisting questionsElement
    if OFFSET + len(questions) > len(questionsElement):
        for i in range(OFFSET + len(questions)-len(questionsElement)):
            Settings.dev_print("adding question...")
            find_element_to_click(browser, "g-btn.m-flat.new_vote_add_option").click()
            Settings.dev_print("added question")
    # find the question inputs again
    questionsElement = browser.find_elements(By.CLASS_NAME, "v-text-field__slot")
    Settings.dev_print("question paths: {}".format(len(questionsElement)))
    # enter the questions
    i = 0
    Settings.dev_print("questions: {}".format(questions))
    Settings.print("- Questions:")
    for question in list(questions):
        Settings.print("> {}".format(question))
        Settings.dev_print("entering question: {}".format(question))
        questionsElement[i].find_elements(By.XPATH, "./child::*")[0].send_keys(str(question))
        Settings.dev_print("entered question")
        time.sleep(1)
        i+=1
    Settings.dev_print("successfully entered questions")
    Settings.debug_delay_check()

# open the poll model
def open_poll_model(browser):
    Settings.dev_print("adding poll")
    elements = browser.find_elements(By.TAG_NAME, "use")
    element = [elem for elem in elements if '#icon-poll' in str(elem.get_attribute('href'))][0]
    ActionChains(browser).move_to_element(element).click().perform()
    time.sleep(1)
    Settings.debug_delay_check()
