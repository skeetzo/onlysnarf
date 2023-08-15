
    ####################
    ##### Schedule #####
    ####################

    def schedule_open(self):
        """Click schedule"""

        Settings.dev_print("opening schedule")
        self.find_element_to_click("scheduleAdd").click()
        Settings.dev_print("successfully opened schedule")

    def schedule_date(self, month, year):
        """Find and click month w/ correct date"""

        Settings.dev_print("setting date")
        while True:

            date = self.browser.find_element(By.CLASS_NAME, "vdatetime-calendar__current--month").get_attribute("innerHTML")

            # date = self.find_element_by_name("scheduleDate").get_attribute("innerHTML")
            Settings.dev_print("date: {} - {} {}".format(date, month, year))
            if str(month) in str(date) and str(year) in str(date):
                Settings.dev_print("set month and year")
                return True
            else:
                self.find_element_to_click("scheduleNextMonth").click()
        return False

    def schedule_day(self, day):
        """Set day in month"""

        Settings.dev_print("setting day")
        for ele in self.find_elements_by_name("scheduleDays"):
            if str(day) in ele.get_attribute("innerHTML").replace("<span><span>","").replace("</span></span>",""):
                ele.click()
                Settings.dev_print("set day")
                return True
        return False

    def schedule_save_date(self):
        """Save schedule date and move to next view in frame by hitting next"""
        
        self.find_element_to_click("scheduleNext").click()
        Settings.dev_print("successfully saved date")

    def schedule_hour(self, hour):
        """Set schedule hour"""

        Settings.dev_print("setting hours")
        eles = self.browser.find_element(By.CLASS_NAME, "vdatetime-time-picker__list--hours").find_elements(By.XPATH, "./child::*")
        for ele in eles:
            if str(hour) in ele.get_attribute("innerHTML").strip():
                # ActionChains(self.browser).move_to_element(ele).click().perform()
                ele.click()
                Settings.dev_print("set hour")
                return True
        return False

    def schedule_minutes(self, minutes):
        """Set schedule minutes"""

        Settings.dev_print("setting minutes")
        eles = self.browser.find_element(By.CLASS_NAME, "vdatetime-time-picker__list--minutes").find_elements(By.XPATH, "./child::*")
        for ele in eles:
            if str(minutes) in ele.get_attribute("innerHTML").strip():
                ele.click()
                Settings.dev_print("set minutes")
                return True
        return False

    def schedule_suffix(self, suffix):
        """Set am/pm suffix"""

        Settings.dev_print("setting suffix")
        eles = self.browser.find_element(By.CLASS_NAME, "vdatetime-time-picker__list--suffix").find_elements(By.XPATH, "./child::*")
        for ele in eles:
            if str(suffix).lower() in ele.get_attribute("innerHTML").strip().lower():
                ele.click()
                Settings.dev_print("set suffix")
                return True
        return False

    def schedule_cancel(self):
        """Cancel schedule by clicking cancel"""

        self.browser.find_element(By.CLASS_NAME, "vdatetime-popup__actions__button--cancel").find_elements(By.XPATH, "./child::*")[0].click()
        Settings.print("canceled schedule")
        return True

    def schedule_save(self):
        """Save schedule by clicking save"""

        # self.find_element_to_click("scheduleSave").click()
        self.browser.find_element(By.CLASS_NAME, "vdatetime-popup__actions__button--confirm").find_elements(By.XPATH, "./child::*")[0].click()
        Settings.print("saved schedule")
        return True

    def schedule(self, schedule):
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

        if str(schedule) == "None" or not schedule: return True
        try:
            Settings.print("Schedule:")
            Settings.print("- Date: {}".format(Settings.format_date(schedule["date"])))
            Settings.print("- Time: {}".format(Settings.format_time(schedule["time"])))
            # ensure schedule button can be accessed
            # self.open_more_options()

            # tries twice to solve various bugs
            try:
                self.schedule_open()
            except Exception as e:
                Settings.dev_print(e)
                self.go_to_home()
                self.schedule_open()

            # return self.schedule_cancel()

            # set month, year, and day
            if not self.schedule_date(schedule["month"], schedule["year"]):
                Settings.debug_delay_check()
                raise Exception("failed to enter date!")
            if not self.schedule_day(schedule["day"]):
                Settings.debug_delay_check()
                raise Exception("failed to enter day!")
            Settings.debug_delay_check()
            self.schedule_save_date()
            # set time
            if not self.schedule_hour(schedule["hour"]):
                Settings.debug_delay_check()
                raise Exception("failed to enter hour!")
            if not self.schedule_minutes(schedule["minute"]):
                Settings.debug_delay_check()
                raise Exception("failed to enter minutes!")
            if not self.schedule_suffix(schedule["suffix"]):
                Settings.debug_delay_check()
                raise Exception("failed to enter suffix!")
            # save time
            Settings.debug_delay_check()
            Settings.dev_print("saving schedule")
            # if str(Settings.is_debug()) == "True":
            #     Settings.print("skipping schedule save (debug)")
            #     return self.schedule_cancel()
            # else:
            return self.schedule_save()
        except Exception as e:
            Driver.error_checker(e)
        # attempt to cancel window
        return self.schedule_cancel()
