if str(username) == "all":
    return User.get_all_users()
elif str(username) == "recent":
    return User.get_recent_users()
elif str(username) == "favorite":
    return User.get_favorite_users()
elif str(username) == "random":
    return User.get_random_user()




@staticmethod
def select_user():
    user = Settings.get_user() or None
    if user: return user
    # if user: return User.get_user_by_username(user.username)
    # if not Settings.prompt("user"): return User.get_random_user()
    choices = Settings.get_message_choices()
    choices.append("enter username")
    choices.append("select username")
    choices = [str(choice).title() for choice in choices]
    question = {
        'type': 'list',
        'name': 'user',
        'message': 'User:',
        'choices': choices,
        'filter': lambda val: str(val).lower()
    }
    answers = PyInquirer.prompt(question)
    user = answers["user"]
    if str(user) == "enter username":
        username = input("Username: ")
        return User.get_user_by_username(username)
    elif str(user) == "select username":
        return User.select_username()
    elif str(user) == "favorites":
        return User.get_favorite_users()
    # elif str(user) == "list":
        # return User.list_menu()
    elif str(user) == "all":
        return User.get_all_users()
    if not Settings.confirm(user): return User.select_user()
    return user

@staticmethod
def select_users():
    # if not Settings.prompt("users"): return []
    users = []
    while True:
        user = User.select_user()
        if not user: break
        if str(user).lower() == "all" or str(user).lower() == "recent": return [user]
        users.append(user)
        if not Settings.prompt("another user"): break
    if not Settings.confirm([user.username for user in users]): return User.select_users()
    return users

@staticmethod
def select_username():
    # returns the list of usernames to select
    # if not Settings.prompt("select username"): return None
    users = User.get_all_users()
    users_ = []
    for user in users:
        user_ = {
            "name":user.username.replace("@",""),
            "value":user,
            "short":user.id
        }
        users_.append(user_)
    question = {
        'type': 'list',
        'name': 'user',
        'message': 'Username:',
        'choices': users_
    }
    user = PyInquirer.prompt(question)['user']
    if not Settings.confirm(user.username): return User.select_username()
    return user





@staticmethod
def list_menu():
    question = {
        'type': 'list',
        'name': 'answer',
        'message': 'User:',
        'choices': ["Back", "Enter", "Select"]
    }
    answer = PyInquirer.prompt(question)["answer"]
    if str(answer) == "Back":
        Settings.print(0)
        return User.select_user()
    elif str(answer) == "Enter":
        question = {
            'type': 'input',
            'message': 'Enter List (name or #):',
            'name': 'list'
        }
        list_ = PyInquirer.prompt(question)["list"]
        theList = None
        try:
            theList = int(list_)
            users = User.get_users_by_list(number=theList)
        except Exception as e:
            try:
                theList = str(list_)
                return User.get_users_by_list(name=theList)
            except Exception as e:
                Settings.err_print("unable to find list number")
    elif str(answer) == "Select":
        lists_ = Driver.get_driver().get_lists()
        lists__ = [{"name":"Back", "value":"back"}]
        for list___ in lists_:
            lists__.append({
                "name":list___[1],
                "value":list___[0],
            })
        question = {
            'type': 'list',
            'name': 'answer',
            'message': 'Lists:',
            'choices': lists_
        }
        answer = PyInquirer.prompt(question)["answer"]
        if str(answer) == "back":
            return User.select_user()
        else:
            return Driver.get_driver().get_list_members(answer)
    return []









# from selecting / confirming the tags/performers in messages.py
        # skip prompt
        if not Settings.prompt(variable): return []
        question = {
            'type': 'input',
            'name': 'keywords',
            'message': '{}:'.format(variable.camelCase()),
            'validate': ListValidator
        }
        if again: Settings.print("are you sure you've done this before, {}? ;)".format(Settings.get_username()))
        variables = prompt(question)[variable]
        variables = [n.strip() for n in variables.split(",")]
        # confirm variables or go in a circle
        # if not Settings.confirm(variables): return self.get_tags(performers=performers, again=True)
        dict(self)[variable] = variables
        return variables