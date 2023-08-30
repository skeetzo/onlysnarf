import json

from .settings import Settings

# add random user to json file
def add_to_randomized_users(newUser):
    if not newUser: return
    Settings.maybe_print("saving random user...")
    data = {}
    data['randomized_users'] = []
    existingUsers = get_already_randomized_users()
    for user in existingUsers:
        if user.equals(newUser):
            user.update(newUser)
        data['randomized_users'].append(user.dump())
    try:
        with open(str(Settings.get_users_path()), 'w') as outfile:  
            json.dump(data, outfile, indent=4, sort_keys=True)
    except FileNotFoundError:
        Settings.err_print("missing local users!")
    except OSError:
        Settings.err_print("missing local path!")
    Settings.dev_print("saved users!")

# return random user from json file 
def get_already_randomized_users():
    Settings.dev_print("getting already randomized users...")
    users = []
    from ..classes.user import User
    try:
        with open(str(Settings.get_users_path())) as json_file:  
            for user in json.load(json_file)['randomized_users']:
                users.append(User(json.loads(user)))
        Settings.maybe_print("loaded randomized users")
    except Exception as e:
        Settings.dev_print(e)
    return users

def read_users_local():
    """
    Read the locally saved users file.

    Returns
    -------
    list
        The locally saved users

    """
    Settings.dev_print("getting local users...")
    users = []
    from ..classes.user import User
    try:
        with open(str(Settings.get_users_path())) as json_file:  
            for user in json.load(json_file)['users']:
                users.append(User(json.loads(user)))
        Settings.maybe_print("loaded local users")
    except Exception as e:
        Settings.dev_print(e)
    return users

def write_users_local(users=[]):
    """
    Write to local users file.

    """

    if len(users) == 0:
        Settings.maybe_print("skipping local users save - empty")
        return
    Settings.maybe_print("saving users...")
    Settings.dev_print(f"local users path: {Settings.get_users_path()}")
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
        with open(str(Settings.get_users_path()), 'w') as outfile:  
            json.dump(data, outfile, indent=4, sort_keys=True)
    except FileNotFoundError:
        Settings.err_print("missing local users!")
    except OSError:
        Settings.err_print("missing local path!")
    Settings.dev_print("saved users!")
