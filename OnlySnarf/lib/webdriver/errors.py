import os
import logging

##############
### Errors ###
##############

def error_checker(e):
    """
    Custom error checker

    Parameters
    ----------
    e : str
        Error text

    """

    if os.environ.get('ENV') == "True": print(err)
    if "unable to locate element" in str(e).lower():
        logging.error("shnarf unable to locate an element! shnarf may require an update!")
    elif "message: " in str(e).lower():
        logging.debug(e)
    else:
        logging.error(e)