from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from .expiration import expiration as EXPIRES
from .errors import error_checker
from .message import message_clear
from .poll import poll as POLL
from .schedule import schedule as SCHEDULE
from .upload import upload_files
from ..util import debug_delay_check
from .. import CONFIG

################
##### Post #####
################

def post(browser, post_object):
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
    post_object : dict
        The message values to be entered into the post 

    Returns
    -------
    bool
        Whether or not the post was successful

    """

    if not post_object:
        Settings.dev_print("skipping empty post")
        return True
    message_clear(browser)
    #################### Formatted Text ####################
    Settings.print("====================")
    Settings.print("Posting:")
    Settings.print("- Files: {}".format(len(post_object["files"])))
    Settings.print("- Performers: {}".format(post_object["performers"]))
    Settings.print("- Keywords: {}".format(post_object["keywords"]))
    Settings.print("- Text: {}".format(post_object["text"]))
    Settings.print("- Tweeting: {}".format(Settings.is_tweeting()))
    ## Expires, Schedule, Poll ##
    if not EXPIRES(browser, post_object["expiration"]): return False
    if post_object["schedule"] and not SCHEDULE(browser, post_object["schedule"]): return False
    if post_object["poll"] and not POLL(browser, post_object["poll"]): return False
    Settings.print("====================")
    ############################################################
    try:
        if Settings.is_tweeting(): enable_tweeting(browser)
        if not enter_text(browser, post_object["text"]):
            Settings.err_print("failed to post!")
            return False
        successful, skipped = upload_files(browser, post_object["files"])
        if successful and not skipped:
            postButton = [ele for ele in browser.find_elements(By.TAG_NAME, "button") if "Post" in ele.get_attribute("innerHTML")][0]
            WebDriverWait(browser, Settings.get_upload_max_duration(), poll_frequency=3).until(EC.element_to_be_clickable(postButton))
            Settings.dev_print("upload complete!")
        send_post(browser)
    except TimeoutException:
        Settings.err_print("timed out waiting for post upload!")
    except Exception as e:
        Settings.dev_print(e)
        Settings.err_print("failed to send post!")
    message_clear(browser)
    return False

def enter_text(browser, text):
        """
        Enter the provided text into the page's text area

        Must be ran on a page with an OnlyFans text area.


        Parameters
        ----------
        text : str
            The text to enter

        Returns
        -------
        bool
            Whether or not entering the text was successful

        """

        try:
            Settings.dev_print("entering text: "+text)
            element = browser.find_element(By.ID, "new_post_text_input")
            action = ActionChains(browser)
            action.move_to_element(element)
            action.click(on_element=element)
            action.double_click()
            action.click_and_hold()
            action.send_keys(Keys.CLEAR)
            action.send_keys(str(text))
            action.perform()
            Settings.dev_print("successfully entered text!")
            return True
        except Exception as e:
            Settings.dev_print(e)
        return False

# TODO: test this
def enable_tweeting(brower):
    Settings.dev_print("enabling tweeting...")
    ActionChains(browser).move_to_element(browser.find_element(By.CLASS_NAME, "b-btns-group").find_elements(By.XPATH, "./child::*")[0]).click().perform()
    Settings.maybe_print("enabled tweeting")

def send_post(browser):
    ## TODO: switch to boolean check last / never
    if str(CONFIG["debug"]) == "True":
        message_clear(browser)
        Settings.print('skipped post (debug)')
        debug_delay_check()
        return True
    Settings.dev_print("sending post...")
    button = [ele for ele in browser.find_elements(By.TAG_NAME, "button") if "Post" in ele.get_attribute("innerHTML")][0]
    ActionChains(browser).move_to_element(button).click().perform()
    Settings.print('Posted to OnlyFans!')
    return True

# no longer used?
# tries both and throws error for not found element internally
def open_more_options(browser):
    """
    Click to open more options on a post.

    Returns
    -------
    bool
        Whether or not opening more options was successful

    """

    def option_one():
        """Click on '...' element"""

        Settings.dev_print("opening options (1)")
        moreOptions = find_element_to_click(browser, "button.g-btn.m-flat.b-make-post__more-btn")
        if not moreOptions: return False    
        moreOptions.click()
        Settings.dev_print("successfully opened more options (1)")
        return True
    def option_two():
        """Click in empty space"""

        Settings.dev_print("opening options (2)")
        moreOptions = find_element_to_click(browser, "new_post_text_input", isID=True)
        if not moreOptions: return False    
        moreOptions.click()
        Settings.dev_print("successfully opened more options (2)")
        return True

    try:
        return option_one()
    except Exception as e:
        error_checker(e)

    try:
        return option_two()
    except Exception as e:
        error_checker(e)
    
    raise Exception("unable to locate 'More Options' element")
