
################
##### Poll #####
################

def poll(self, poll):
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

    if not poll or str(poll) == "None": return True
    try:
        Settings.print("Poll:")

        open_model(self.browser)
        
        Settings.debug_delay_check()
        
        add_duration(self.browser, poll["duration"])
        
        Settings.debug_delay_check()
        
        add_questions(self.browser, poll["questions"])

        Settings.debug_delay_check()

        if Settings.is_debug():
            Settings.maybe_print("skipping poll (debug)")
            cancel = self.find_element_to_click("pollCancel")
            # {
            #     "name": "pollCancel",
            #     "classes": ["b-dropzone__preview__delete"],
            #     "text": ["Cancel"],
            #     "id": []
            # },
            cancel.click()
        Settings.dev_print("### Poll Successful ###")
        return True
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("failed to enter poll!")
    return False

# open the poll model
def open_model(browser):
    Settings.dev_print("adding poll")
    elements = browser.find_elements(By.TAG_NAME, "use")
    element = [elem for elem in elements if '#icon-poll' in str(elem.get_attribute('href'))][0]
    ActionChains(browser).move_to_element(element).click().perform()
    time.sleep(1)

# open the poll duration
# can click anywhere near the top label
# TODO: finish updating any inserted wait times to be more dynamic
def add_duration(browser, duration, wait=1):
    # self.find_element_to_click("pollDuration").click()
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
    self.find_element_to_click("pollSave").click()
    # {
    #     "name": "pollSave",
    #     "classes": ["g-btn.m-flat.m-btn-gaps.m-reset-width"],
    #     "text": ["Save"],
    #     "id": []
    # },
    Settings.dev_print("successfully saved duration")

def add_questions(browser, questions):
    Settings.dev_print("configuring question paths...")
    questionsElement = browser.find_elements(By.CLASS_NAME, "v-text-field__slot")
    # add extra question space
    OFFSET = 2 # number of preexisting questionsElement
    if OFFSET + len(questions) > len(questionsElement):
        for i in range(OFFSET + len(questions)-len(questionsElement)):
            Settings.dev_print("adding question")
            question_ = self.find_element_to_click("pollQuestionAdd").click()
            # {
            #     "name": "pollQuestionAdd",
            #     "classes": ["g-btn.m-flat.new_vote_add_option", "button.g-btn.m-flat.new_vote_add_option"],
            #     "text": [],
            #     "id": []
            # },
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
