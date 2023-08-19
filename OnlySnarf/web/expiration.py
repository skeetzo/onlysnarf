from ..util.settings import Settings

######################
##### Expiration #####
######################

def expires(self, expiration):
    """
    Enters the provided expiration duration for a post

    Must be on home page

    Parameters
    ----------
    expiration : int
        The duration (in days) until the post expires
    
    Returns
    -------
    bool
        Whether or not entering the expiration was successful

    """

    if str(expiration) == "0" or not expiration: return True
    try:
        Settings.print("Expiration:")
        Settings.print("- Period: {}".format(expiration))
        # if expiration is 'no limit', then there's no expiration and hence no point here
        if expiration == 999: return True

        enter_expiration(self.browser, expiration)

        Settings.debug_delay_check()

        Settings.dev_print("### Expiration Successful ###")
        return True
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("failed to enter expiration!")

    cancel_expiration(self.browser)

    return False

def enter_expiration(browser, expires):
    Settings.dev_print("entering expiration...")
    # {
    #     "name": "expiresAdd",
    #     "classes": ["b-make-post__expire-period-btn"],
    #     "text": ["Save"],
    #     "id": []
    # },
    action = ActionChains(browser)
    action.click(on_element=self.find_element_to_click("expiresAdd"))
    action.pause(int(1))
    action.send_keys(Keys.TAB)
    action.send_keys(str(expires))
    action.pause(int(1))
    action.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
    action.pause(int(1))
    action.send_keys(Keys.ENTER)
    action.perform()
    Settings.dev_print("successfully entered expiration")

# not really necessary with 'Clear' button
def cancel_expiration(browser):
    Settings.dev_print("canceling expiration...")
    elements = browser.find_elements(By.TAG_NAME, "use")
    element = [elem for elem in elements if '#icon-close' in str(elem.get_attribute('href'))][0]
    ActionChains(browser).move_to_element(element).click().perform()
    Settings.dev_print("### Expiration Canceled ###")