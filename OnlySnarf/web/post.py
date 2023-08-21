
from .expiration import expires as EXPIRES
from .message import message_clear
from .poll import poll as POLL
from .schedule import schedule as SCHEDULE
from .upload import upload_files
from ..classes.message import Post
from ..util.settings import Settings

################
##### Post #####
################

def post(post_object=Post()):
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
    browser = Driver.get_browser()
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
    if post_object["schedule"] and post_object["schedule"].validate() and not SCHEDULE(browser, post_object["schedule"].get()): return False
    if post_object["poll"].validate() and not POLL(browser, post_object["poll"].get()): return False
    Settings.print("====================")
    ############################################################
    ## Tweeting ##
    # TODO: test this
    if Settings.is_tweeting():
        Settings.dev_print("tweeting...")
        # twitter tweet button is 1st, post is 2nd
        ActionChains(browser).move_to_element(browser.find_element(By.CLASS_NAME, "b-btns-group").find_elements(By.XPATH, "./child::*")[0]).click().perform()
        WebDriverWait(browser, 30, poll_frequency=3).until(EC.element_to_be_clickable((By.XPATH, "//label[@for='new_post_tweet_send']"))).click()
    try:
        if not enter_text(browser, post_object["text"]):
            Settings.err_print("failed to post!")
            return False
        successful, skipped = upload_files(browser, post_object["files"])
        if successful and not skipped:
            # twitter tweet button is 1st, post is 2nd
            postButton = [ele for ele in browser.find_elements(By.TAG_NAME, "button") if "Post" in ele.get_attribute("innerHTML")][0]
            WebDriverWait(browser, Settings.get_upload_max_duration(), poll_frequency=3).until(EC.element_to_be_clickable(postButton))
            Settings.dev_print("upload complete")
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

def send_post(browser):
    ## TODO: switch to boolean check last / never
    if str(Settings.is_debug()) == "True":
        message_clear(browser)
        Settings.print('skipped post (debug)')
        Settings.debug_delay_check()
        return True
    Settings.dev_print("sending post...")
    button = [ele for ele in browser.find_elements(By.TAG_NAME, "button") if "Post" in ele.get_attribute("innerHTML")][0]
    ActionChains(browser).move_to_element(button).click().perform()
    Settings.print('Posted to OnlyFans!')
    return True