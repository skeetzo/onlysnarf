import os
import json
import logging

from .config import CONFIG

USERS_PATH = os.path.expanduser(CONFIG["path_users"])

def reset_userlist():
    try:
        os.remove(USERS_PATH)
    except Exception as e:
        logging.debug(e)
    with open(USERS_PATH, 'w') as f:
        json.dump({"users":[],"randomized_users":[]}, f)

# TODO: this could be combined into write_users_local but for now i'm keeping it separate
# add random user to json file
def add_to_randomized_users(newUser):
    if CONFIG["debug"]: return
    if not newUser: return
    logging.debug("saving random user...")
    users, randomized_users = read_users_local()
    for user in randomized_users:
        if newUser.equals(user):
            raise Exception("there shouldn't be duplicate random users!")
    randomized_users.append(newUser.dump())
    try:
        data = {}
        data['users'] = users
        data['randomized_users'] = randomized_users
        with open(USERS_PATH, 'w') as outfile:  
            json.dump(data, outfile, indent=4, sort_keys=True)
        logging.debug("saved random user!")
    except OSError:
        reset_userlist()
        return add_to_randomized_users(newUser)
    except OSError:
        logging.error("missing local path!")
    except Exception as e:
        reset_userlist()
        logging.debug(e)

def remove_from_randomized_users(removedUser):
    pass

def reset_random_users():
    logging.debug("resetting random users...")
    existing_users, randomized_users = read_users_local()
    try:
        data = {}
        data['users'] = existing_users
        data['randomized_users'] = []
        with open(USERS_PATH, 'w') as outfile:  
            json.dump(data, outfile, indent=4, sort_keys=True)
        logging.debug("successfully reset random users!")
    except Exception as e:
        logging.error(e)

def read_users_local():
    """
    Read the locally saved users file.

    Returns
    -------
    list
        The locally saved users

    """
    logging.debug("getting local users...")
    users = []
    randomized_users = []
    from ..classes.user import User
    try:
        with open(USERS_PATH) as json_file:  
            loaded = json.load(json_file)
            for user in loaded['users']:
                users.append(User.create_user(user).dump())
            for user in loaded['randomized_users']:
                randomized_users.append(User.create_user(user).dump())
        # logging.debug(users)
        # logging.debug(randomized_users)
        logging.debug(f"successfully loaded local users: {len(users)}")
    except OSError:
        reset_userlist()
    except Exception as e:
        logging.debug(e)
        # reset_userlist()
    return users, randomized_users

def write_users_local(added_users):
    """
    Write to local users file.

    """

    if not isinstance(added_users, list) and len(added_users) == 0:
        logging.debug("skipping local users save - empty")
        return
    logging.debug("saving users...")
    logging.debug(f"local users path: {USERS_PATH}")
    # merge with existing user data
    existing_users, randomized_users = read_users_local()

    new_users = []
    usernames = []
    for each_added_user in added_users:
        found = False
        for existing_user in existing_users:
            updated = False
            for added_user in added_users:
                # if added_user.equals(existing_user):
                if added_user.equals(existing_user) and added_user.username not in usernames:
                    existing_user.update(added_user.dump())
                    logging.debug(f"updated: {added_user.username}")
                    new_users.append(existing_user)
                    usernames.append(added_user.username)
                    updated = True
                    if added_user.equals(each_added_user):
                        found = True
                    break
            if found:
                break
            if not updated and existing_user["username"] not in usernames:
                logging.debug(f"existing: {existing_user['username']}")
                new_users.append(existing_user)
                usernames.append(existing_user["username"])
                break
        if not found and each_added_user.username not in usernames:
            logging.debug(f"adding: {each_added_user.username}")
            new_users.append(each_added_user.dump())
            usernames.append(each_added_user.username)

    # for user in new_users:
    #     list(filter(lambda d: d['type'] in keyValList, exampleSet))
    # expectedResult = [d for d in exampleSet if d['type'] in keyValList]


    # logging.debug("new users:")
    # logging.debug(new_users)

    data = {}
    data['users'] = new_users
    data['randomized_users'] = randomized_users
    try:
        with open(USERS_PATH, 'w') as outfile:  
            json.dump(data, outfile, indent=4, sort_keys=True)
        logging.debug("saved users!")
    except OSError:
        logging.error("missing local users!")
        reset_userlist()
        write_users_local(added_users)
    except Exception as e:
        logging.debug(e)
