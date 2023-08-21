
from .message import message_user
from ..util.settings import Settings

############
### Chat ###
############

# code that is meant to revolve around reading / writing chats to users
def get_recent_chats(browser):
    # get recent chat users
    # get each chat for user
    pass


# TODO: update, test, and probably rename
# go to /chats page and retrieve top n users
def get_recent_chat_users(browser, num=0):
    """
    Scan messages page for recent users

    Parameters
    ----------
    num : int
        The number of users to consider recent (doesn't work)

    Returns
    -------
    list
        The list of users found

    """

    Settings.dev_print("scanning recent chats...")
    users = []
    try:
        go_to_page(browser, "/my/chats")
        users_ = browser.find_elements(By.CLASS_NAME, "g-user-username")
        Settings.dev_print("users: {}".format(len(users_)))
        user_ids = browser.find_elements(By.CLASS_NAME, "b-chats__item__link")
        Settings.dev_print("ids: {}".format(len(user_ids)))
        for user in user_ids:
            if not user or not user.get_attribute("href") or str(user.get_attribute("href")) == "None": continue
            users.append(str(user.get_attribute("href")).replace("https://onlyfans.com/my/chats/chat/", ""))
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("Failed to scan messages!")
    return users[:10]









# TODO: update this lastish

def get_user_chat(browser, username, user_id=None):
    """
    Read the messages of the target user by username or user id.

    Parameters
    ----------
    username : str
        The username of the user to read messages of
    user_id : str
        The user id of the user to read messages of

    Returns
    -------
    list
        A list containing the messages read

    """

    try:
        # go to onlyfans.com/my/subscribers/active
        message_user(browser, username, user_id=user_id)
        messages_sent_ = []

        try:
            messages_sent_ = browser.find_elements(By.CLASS_NAME, "m-from-me")
        except Exception as e:
            if "Unable to locate elements" in str(e):
                pass
            else: Settings.dev_print(e)
        
        messages_all_ = []
        try:
            messages_all_ = browser.find_elements(By.CLASS_NAME, "b-chat__message__text")
        except Exception as e:
            if "Unable to locate elements" in str(e):
                pass
            else: Settings.dev_print(e)


        # TODO: cleanup this process

        # do stuff to process the messages
        messages_all = []
        messages_received = []
        messages_sent = []
        # timestamps_ = browser.find_elements(By.CLASS_NAME, "b-chat__message__time")
        # timestamps = []
        # for timestamp in timestamps_:
            # Settings.maybe_print("timestamp1: {}".format(timestamp))
            # timestamp = timestamp["data-timestamp"]
            # timestamp = timestamp.get_attribute("innerHTML")
            # Settings.maybe_print("timestamp: {}".format(timestamp))
            # timestamps.append(timestamp)
        for message in messages_all_:
            message = message.get_attribute("innerHTML")
            message = re.sub(r'<[a-zA-Z0-9=\"\\/_\-!&;%@#$\(\)\.:\+\s]*>', "", message)
            Settings.maybe_print("all: {}".format(message))
            messages_all.append(message)
        messages_and_timestamps = []
        # messages_and_timestamps = [j for i in zip(timestamps,messages_all) for j in i]
        # Settings.maybe_print("chat log:")
        # for f in messages_and_timestamps:
            # Settings.maybe_print(": {}".format(f))
        for message in messages_sent_:
            # Settings.maybe_print("from1: {}".format(message.get_attribute("innerHTML")))
            message = message.find_element(By.CLASS_NAME, Element.get_element_by_name("enterMessage").getClass()).get_attribute("innerHTML")
            message = re.sub(r'<[a-zA-Z0-9=\"\\/_\-!&;%@#$\(\)\.:\+\s]*>', "", message)
            Settings.maybe_print("sent: {}".format(message))
            messages_sent.append(message)
        i = 0

        # messages_all = list(set(messages_all))
        # messages_sent = list(set(messages_sent))
        # i really only want to remove duplicates if they're over a certain str length

        def remove_dupes(list_):
            """Remove duplicates from the list"""

            for i in range(len(list_)):
                for j in range(len(list_)):
                    # if j >= len(list_): break
                    if i==j: continue
                    if str(list_[i]) == str(list_[j]) and len(str(list_[i])) > 10:
                        del list_[j]
                        remove_dupes(list_)
                        return
                        
        remove_dupes(messages_all)
        remove_dupes(messages_sent)

        for message in messages_all:
            if message not in messages_sent:
                messages_received.append(message)
            i += 1
        Settings.maybe_print("received: {}".format(messages_received))
        Settings.maybe_print("sent: {}".format(messages_sent))
        Settings.maybe_print("messages sent: {}".format(len(messages_sent)))
        Settings.maybe_print("messages received: {}".format(len(messages_received)))
        Settings.maybe_print("messages all: {}".format(len(messages_all)))
        return [messages_all, messages_and_timestamps, messages_received, messages_sent]
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("failure to read chat - {}".format(username))
        return [[],[],[],[]]
