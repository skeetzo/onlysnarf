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

    if "Unable to locate element" in str(e):
        logging.error("Unable to locate element; OnlySnarf may require an update!")
    elif "Message: " in str(e):
        logging.debug(e)
    else:
        logging.error(e)