
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

        if str(poll) == "None" or not poll: return True
        try:
            Settings.print("Poll:")

            # open the poll model
            def open_model():
                Settings.dev_print("adding poll")
                elements = self.browser.find_elements(By.TAG_NAME, "use")
                element = [elem for elem in elements if '#icon-poll' in str(elem.get_attribute('href'))][0]
                ActionChains(self.browser).move_to_element(element).click().perform()
                time.sleep(1)

            # open the poll duration
            # can click anywhere near the top label
            # TODO: finish updating any inserted wait times to be more dynamic
            def add_duration(duration, wait=1):
                # self.find_element_to_click("pollDuration").click()
                Settings.print("- Duration: {}".format(duration))
                Settings.dev_print("setting duration")
                action = ActionChains(self.browser)
                action.click(on_element=self.browser.find_element(By.CLASS_NAME, "b-post-piece__value"))
                action.pause(int(wait))
                action.send_keys(Keys.TAB)
                action.send_keys(str(duration))
                action.perform()
                # save the duration
                Settings.dev_print("saving duration")
                self.find_element_to_click("pollSave").click()
                Settings.dev_print("successfully saved duration")

            def add_questions(questions):
                Settings.dev_print("configuring question paths...")
                questionsElement = self.browser.find_elements(By.CLASS_NAME, "v-text-field__slot")
                # add extra question space
                OFFSET = 2 # number of preexisting questionsElement
                if OFFSET + len(questions) > len(questionsElement):
                    for i in range(OFFSET + len(questions)-len(questionsElement)):
                        Settings.dev_print("adding question")
                        question_ = self.find_element_to_click("pollQuestionAdd").click()
                        Settings.dev_print("added question")
                # find the question inputs again
                questionsElement = self.browser.find_elements(By.CLASS_NAME, "v-text-field__slot")
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

            open_model()
            Settings.debug_delay_check()
            add_duration(poll["duration"])
            Settings.debug_delay_check()
            add_questions(poll["questions"])
            Settings.debug_delay_check()

            if str(Settings.is_debug()) == "True":
                Settings.maybe_print("skipping poll (debug)")
                cancel = self.find_element_to_click("pollCancel")
                cancel.click()
            Settings.dev_print("### Poll Successful ###")
            return True
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failed to enter poll!")
        return False
