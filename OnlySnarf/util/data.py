import os
import json
import logging

from .config import CONFIG

# TODO: finish data; currently overwrites weirdly; finish test scripts for reading/writing randomized



USERS_PATH = os.path.expanduser(CONFIG["path_users"])

def reset_userlist():
    try:
        os.remove(USERS_PATH)
    except Exception as e:
        print(e)
    with open(USERS_PATH, 'w') as f:
        json.dump({"users":[],"randomized_users":[]}, f)

# add random user to json file
def add_to_randomized_users(newUser):
    if not newUser: return
    logging.debug("saving random user...")
    data = {}
    data['users'] = []
    data['randomized_users'] = []
    existingUsers = get_already_randomized_users()
    for user in existingUsers:
        if user.equals(newUser):
            user.update(newUser)
        data['randomized_users'].append(user.dumps())
    for user in read_users_local():
        data["users"].append(user.dump())
    try:
        # with open(USERS_PATH, 'w') as outfile:  
            # json.dump(data, outfile, indent=4, sort_keys=True)
        logging.debug("saved random users!")
    except OSError:
        reset_userlist()
        return add_to_randomized_users(newUser)
    except OSError:
        logging.error("missing local path!")

# return random user from json file 
def get_already_randomized_users():
    logging.debug("getting already randomized users...")
    users = []
    from ..classes.user import User
    try:
        with open(USERS_PATH) as json_file:  
            for user in json.load(json_file)['randomized_users']:
                users.append(User.create_user(user))
        logging.debug("loaded randomized users")
    except OSError:
        reset_userlist()
    except Exception as e:
        logging.debug(e)
    return users

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
    from ..classes.user import User
    try:
        with open(USERS_PATH) as json_file:  
            for user in json.load(json_file)['users']:
                users.append(User.create_user(user))
        logging.debug("loaded local users")
    except OSError:
        reset_userlist()
    except Exception as e:
        logging.debug(e)
        print(e)
    return users

def write_users_local(users=[]):
    """
    Write to local users file.

    """

    if len(users) == 0:
        logging.debug("skipping local users save - empty")
        return
    logging.debug("saving users...")
    logging.debug(f"local users path: {USERS_PATH}")
    # merge with existing user data
    data = {}
    data['users'] = []
    data['randomized_users'] = []
    existingUsers = read_users_local()
    for user in users:
        for u in existingUsers:
            if user.equals(u):
                user.update(u)
        data['users'].append(user.dump())
    for user in get_already_randomized_users():
        data["randomized_users"].append(user.dumps())
    try:
        # with open(USERS_PATH, 'w') as outfile:  
            # json.dump(data, outfile, indent=4, sort_keys=True)
        logging.debug("saved users!")
    except OSError:
        logging.error("missing local users!")
        reset_userlist()
        write_users_local(users)
    except OSError:
        logging.error("missing local path!")
