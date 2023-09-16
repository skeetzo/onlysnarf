import logging
logger = logging.getLogger(__name__)

from .errors import error_checker
from .. import CONFIG

# TODO: also last

####################
##### Settings #####
####################

# gets all settings from whichever page its on
# or get a specific setting
# probably just way easier and resourceful to do it all at once
# though it would be ideal to also be able to update individual settings without risking other settings

# goes through the settings and get all the values
# @staticmethod
# def settings_get_all():
#     logger.info("Getting All Settings")
#     profile = Profile()
#     try:
#         pages = Profile.get_pages()
#         for page in pages:
#             data = self.sync_from_settings_page(page)
#             for key, value in data:
#                 profile[key] = value
#         logger.debug("successfully got settings")
#         logger.info("Settings Retrieved")
#     except Exception as e:
#         error_checker(e)
#     return profile

def sync_from_settings_page(self, profile=None, page=None):
    """
    Sync values from settings page.

    Parameters
    ----------
    profile : Profile
        The profile object to sync from
    page : str
        The profile page to sync settings from

    Returns
    -------
    bool
        Whether or not the sync was successful

    """

    logger.info("Getting Settings: {}".format(page))
    from ..classes.profile import Profile
    try:
        variables = Profile.get_variables_for_page(page)
        logger.debug("going to settings page: {}".format(page))
        self.go_to_settings(page)
        logger.debug("reached settings: {}".format(page))
        if profile == None:
            profile = Profile()
        for var in variables:
            name = var[0]
            page_ = var[1]
            type_ = var[2]
            status = None
            logger.debug("searching: {} - {}".format(name, type_))
            try:
                element = self.find_element_by_name(name)
                logger.debug("successful ele: {}".format(name))
            except Exception as e:
                error_checker(e)
                continue
            if str(type_) == "text":
                # get attr text
                status = element.get_attribute("innerHTML").strip() or None
                status2 = element.get_attribute("value").strip() or None
                logger.info("{} - {}".format(status, status2))
                if not status and status2: status = status2
            elif str(type_) == "toggle":
                # get state true|false
                status = element.is_selected()
            elif str(type_) == "dropdown":
                ele = self.find_element_by_name(name)
                Select(self.browser.find_element(By.ID, ele.getId()))
                status = element.first_selected_option
            elif str(type_) == "list":
                status = element.get_attribute("innerHTML")
            elif str(type_) == "file":
                logger.info("NEED TO UPDATE THIS")
                # can get file from image above
                # can set once found
                # status = element.get_attribute("innerHTML")
                # pass
            elif str(type_) == "checkbox":
                status = element.is_selected()
            if status is not None: logger.debug("successful value: {}".format(status))
            logger.debug("{} : {}".format(name, status))
            setattr(profile, str(name), status)
        logger.debug("successfully got settings page: {}".format(page))
        logger.info("Settings Page Retrieved: {}".format(page))
    except Exception as e:
        error_checker(e)

# goes through each page and sets all the values
def sync_to_settings_page(self, profile=None, page=None):
    """
    Sync values to settings page.

    Parameters
    ----------
    profile : Profile
        The profile object to sync to
    page : str
        The profile page to sync settings to

    Returns
    -------
    bool
        Whether or not the sync was successful

    """

    logger.info("Updating Page Settings: {}".format(page))
    from ..classes.profile import Profile
    try:
        variables = Profile.get_variables_for_page(page)
        logger.debug("going to settings page: {}".format(page))
        self.go_to_settings(page)
        logger.debug("reached settings: {}".format(page))
        if profile == None:
            profile = Profile()
        for var in variables:
            name = var[0]
            page_ = var[1]
            type_ = var[2]
            status = None
            logger.debug("searching: {} - {}".format(name, type_))
            try:
                element = self.find_element_by_name(name)
                logger.debug("successful ele: {}".format(name))
            except Exception as e:
                error_checker(e)
                continue
            if str(type_) == "text":

                element.send_keys(getattr(profile, str(name)))
            elif str(type_) == "toggle":
                # somehow set the other toggle state
                pass
            elif str(type_) == "dropdown":
                ele = self.find_element_by_name(name)
                Select(self.browser.find_element(By.ID, ele.getId()))
                # go to top
                # then go to matching value
                pass
            elif str(type_) == "list":
                element.send_keys(getattr(profile, str(name)))
            elif str(type_) == "file":
                element.send_keys(getattr(profile, str(name)))
            elif str(type_) == "checkbox":
                element.click()
        if str(CONFIG["debug"]) == "True":
            logger.debug("successfully cancelled settings page: {}".format(page))
        else:
            self.settings_save(page=page)
            logger.debug("successfully set settings page: {}".format(page))
        logger.info("Settings Page Updated: {}".format(page))
    except Exception as e:
        error_checker(e)

# @staticmethod
# def settings_set_all(Profile):
#     logger.info("Updating All Settings")
#     try:
#         pages = Profile.TABS
#         for page in pages:
#             self.sync_to_settings_page(Profile, page)
#         logger.debug("successfully set settings")
#         logger.info("Settings Updated")
#     except Exception as e:
#         error_checker(e)

# saves the settings page if it is a page that needs to be saved
    # has save:
    # profile
    # account
    # security
    ##
    # doesn't have save:
    # story
    # notifications
    # other
def settings_save(self, page=None):
    """
    Save the provided settings page if it is a page that saves

    Parameters
    ----------
    page : str
        The settings page to check if saves
    
    """

    if str(page) not in ["profile", "account", "security"]:
        logger.debug("not saving: {}".format(page))
        return
    try:
        logger.debug("saving: {}".format(page))
        element = self.find_element_by_name("profileSave")
        logger.debug("derp")
        element = self.find_element_to_click("profileSave")
        logger.debug("found page save")
        if str(CONFIG["debug"]) == "True":
            logger.info("skipping settings save (debug)")
        else:
            logger.debug("saving page")
            element.click()
            logger.debug("page saved")
    except Exception as e:
        error_checker(e)
