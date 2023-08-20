
################
##### Post #####
################

@staticmethod
def post(message):
    """
    Post the message to OnlyFans.

    Optionally tweet if enabled. A message must contain text and can contain:
    - files
    - keywords
    - performers
    - expiration
    - schedule
    - poll

    Parameters
    ----------
    message : dict
        The message values to be entered into the post 

    Returns
    -------
    bool
        Whether or not the post was successful

    """

    Settings.dev_print("posting...")
    driver = Driver.get_driver()
    driver.auth()

    ## TODO
    # add check for clearing any text or images already in post field
    driver.message_clear()

    #################### Formatted Text ####################
    Settings.print("====================")
    Settings.print("Posting:")
    Settings.print("- Files: {}".format(len(message["files"])))
    Settings.print("- Performers: {}".format(message["performers"]))
    Settings.print("- Keywords: {}".format(message["keywords"]))
    Settings.print("- Text: {}".format(message["text"]))
    Settings.print("- Tweeting: {}".format(Settings.is_tweeting()))
    ## Expires, Schedule, Poll ##
    if not driver.expires(message["expiration"]): return False
    if message["schedule"] and message["schedule"].validate() and not driver.schedule(message["schedule"].get()): return False
    if message["poll"].validate() and not driver.poll(message["poll"].get()): return False
    Settings.print("====================")
    ############################################################

    ## Tweeting ##
    ## TODO
    ## test this
    if Settings.is_tweeting():
        Settings.dev_print("tweeting...")
        # twitter tweet button is 1st, post is 2nd
        ActionChains(driver.browser).move_to_element(driver.browser.find_element(By.CLASS_NAME, "b-btns-group").find_elements(By.XPATH, "./child::*")[0]).click().perform()
        WebDriverWait(driver.browser, 30, poll_frequency=3).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='new_post_tweet_send']"))).click()

    try:

        if not driver.enter_text(message["text"]):
            Settings.err_print("failed to post!")
            return False

        successful, skipped = driver.upload_files(message["files"])
        if successful and not skipped:
            # twitter tweet button is 1st, post is 2nd
            postButton = [ele for ele in driver.browser.find_elements(By.TAG_NAME, "button") if "Post" in ele.get_attribute("innerHTML")][0]
            WebDriverWait(driver.browser, Settings.get_upload_max_duration(), poll_frequency=3).until(EC.element_to_be_clickable(postButton))
            Settings.dev_print("upload complete")

        ## TODO: switch to boolean check last / never
        if str(Settings.is_debug()) == "True":
            driver.message_clear()
            Settings.print('skipped post (debug)')
            Settings.debug_delay_check()
            return True

        Settings.dev_print("uploading post...")
        postButton = [ele for ele in driver.browser.find_elements(By.TAG_NAME, "button") if "Post" in ele.get_attribute("innerHTML")][0]
        ActionChains(driver.browser).move_to_element(postButton).click().perform()
        Settings.print('Posted to OnlyFans!')
        return True
    except TimeoutException:
        Settings.err_print("timed out waiting for post upload!")
    except Exception as e:
        Settings.dev_print(e)
        Settings.err_print("failed to send post!")

    # necessary?
    # driver.go_to_home(force=True)

    return False