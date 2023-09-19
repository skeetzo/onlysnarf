
from .browser import create_browser
from .chat import get_user_chat, get_recent_chat_users
from .cookies import cookies_load, cookies_save
from .discount import discount
from .expiration import expiration
from .goto import go_to_home
from .login import login
from .message import message
from .poll import poll
from .post import post
from .schedule import schedule
from .users import get_current_username, get_userid_by_username, get_users_by_type, get_random_fan_username

# read_user_messages = Driver.read_user_messages # unfinished / missing




# def scroll_to_bottom(browser):
#     logging.debug("scrolling to bottom...")
#     SCROLL_PAUSE_TIME = 1

#     # Get scroll height
#     last_height = browser.execute_script("return document.body.scrollHeight")

#     while True:
#         logging.debug("scrolling...")
#         # Scroll down to bottom
#         browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#         # Wait to load page
#         time.sleep(SCROLL_PAUSE_TIME)

#         # Calculate new scroll height and compare with last scroll height
#         new_height = browser.execute_script("return document.body.scrollHeight")
#         if new_height == last_height:
#             break
#         last_height = new_height


# def scroll_to_bottom_once(browser):
#     logging.debug("scrolling to bottom once...")
#     # Scroll down to bottom
#     browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     # Wait to load page
#     time.sleep(1)