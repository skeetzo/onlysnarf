from .driver import Driver

discount_user = Driver.discount_user

get_recent_chat_users = Driver.get_recent_chat_users
get_userid_by_username = Driver.get_userid_by_username
get_username_by_id = Driver.get_username_by_id

post = Driver.post
message = Driver.message

# read_user_messages = Driver.read_user_messages # unfinished / missing

def exit_handler():
    """Exit cleanly"""

    try:
        Driver.exit(Driver.BROWSER)
    except Exception as e:
        print(e)

import atexit
atexit.register(exit_handler)