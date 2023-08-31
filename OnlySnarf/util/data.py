import json
import logging

from .config import CONFIG

USERS_PATH = CONFIG["path_users"]

# add random user to json file
def add_to_randomized_users(newUser):
    if not newUser: return
    logging.debug("saving random user...")
    data = {}
    data['randomized_users'] = []
    existingUsers = get_already_randomized_users()
    for user in existingUsers:
        if user.equals(newUser):
            user.update(newUser)
        data['randomized_users'].append(user.dump())
    try:
        with open(str(USERS_PATH), 'w') as outfile:  
            json.dump(data, outfile, indent=4, sort_keys=True)
    except FileNotFoundError:
        logging.error("missing local users!")
    except OSError:
        logging.error("missing local path!")
    logging.debug("saved users!")

# return random user from json file 
def get_already_randomized_users():
    logging.debug("getting already randomized users...")
    users = []
    from ..classes.user import User
    try:
        with open(str(USERS_PATH)) as json_file:  
            for user in json.load(json_file)['randomized_users']:
                users.append(User(json.loads(user)))
        logging.debug("loaded randomized users")
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
        with open(str(USERS_PATH)) as json_file:  
            for user in json.load(json_file)['users']:
                users.append(User(json.loads(user)))
        logging.debug("loaded local users")
    except Exception as e:
        logging.debug(e)
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
    existingUsers = read_users_local()
    for user in users:
        for u in existingUsers:
            if user.equals(u):
                user.update(u)
        data['users'].append(user.dump())
    try:
        with open(str(USERS_PATH), 'w') as outfile:  
            json.dump(data, outfile, indent=4, sort_keys=True)
    except FileNotFoundError:
        logging.error("missing local users!")
    except OSError:
        logging.error("missing local path!")
    logging.debug("saved users!")
