from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from .element import find_element_to_click
from .. import CONFIG, debug_delay_check

######################
##### Expiration #####
######################

def expiration(browser, expires="0"):
    """
    Enters the provided expiration duration for a post

    Must be on home page

    Parameters
    ----------
    expires : str
        The duration (in days) until the post expires
    
    Returns
    -------
    bool
        Whether or not entering the expiration was successful

    """

    if str(expires) == "0":
        Settings.dev_print("skipping empty expiration")
        return True
    # if expiration is 'no limit', then there's no expiration and hence no point here
    elif str(expires) == "999":
        Settings.dev_print("skipping no-limit expiration")
        return True
    try:
        Settings.print(f"Expiration: {expires}")
        enter_expiration(browser, expires)
        Settings.dev_print("### Expiration Successful ###")
        return True
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("failed to enter expiration!")
    cancel_expiration(browser)
    return False

def enter_expiration(browser, expires):
    Settings.dev_print("entering expiration...")
    action = ActionChains(browser)
    action.click(on_element=find_element_to_click(browser, "b-make-post__expire-period-btn", text="Save"))
    action.pause(int(1))
    action.send_keys(Keys.TAB)
    action.send_keys(str(expires))
    action.pause(int(1))
    action.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
    action.pause(int(1))
    action.send_keys(Keys.ENTER)
    action.perform()
    Settings.dev_print("successfully entered expiration!")
    debug_delay_check()

# not really necessary with 'Clear' button
def cancel_expiration(browser):
    Settings.dev_print("canceling expiration...")
    elements = browser.find_elements(By.TAG_NAME, "use")
    element = [elem for elem in elements if '#icon-close' in str(elem.get_attribute('href'))][0]
    ActionChains(browser).move_to_element(element).click().perform()
    Settings.dev_print("### Expiration Canceled ###")
    debug_delay_check()