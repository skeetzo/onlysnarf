
from ..util.settings import Settings

##############
### Errors ###
##############

@staticmethod
def error_checker(e):
    """
    Custom error checker

    Parameters
    ----------
    e : str
        Error text

    """

    if "Unable to locate element" in str(e):
        Settings.err_print("Unable to locate element; OnlySnarf may require an update!")
    elif "Message: " in str(e):
        Settings.dev_print(e)
    else:
        Settings.err_print(e)
