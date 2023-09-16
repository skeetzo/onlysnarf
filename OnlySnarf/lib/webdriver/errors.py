import os
import logging
logger = logging.getLogger(__name__)

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
        logger.error("shnarf unable to locate an element! shnarf may require an update!")
    elif "message: " in str(e).lower():
        logger.debug(e)
    else:
        logger.error(e)