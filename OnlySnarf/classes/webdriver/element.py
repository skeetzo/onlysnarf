from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from .. import Settings

################
### Elements ###
################

# text: the text that should be included in the element text
# isID: use id instead of class_name
# fuzzymatch: use "in" instead of "==" when matching text
# index: the index of the element to search for, used to ignore early matches
def find_element_to_click(browser, name, text="", isID=False, fuzzyMatch=False, index=0):
    """
    Find element on page by name to click

    Does not auth check or otherwise change the focus. Checks that located element is properly 
    capable of being clicked.

    Parameters
    ----------
    name : str
        The name of the element to click as referenced from its /elements/element name

    Returns
    -------
    Selenium.WebDriver.WebElements
        The located web element that can be clicked

    """

    Settings.dev_print("finding element: {}".format(name))
    try:
        elements = browser.find_elements(By.ID if isID else By.CLASS_NAME, className)
        Settings.dev_print(f"elements found: {len(elements)}")
        i = 0
        for element in elements:
            Settings.dev_print(f"element: {element.get_attribute('innerHTML').strip()}")
            if element.is_displayed() and element.is_enabled() and i == index:
                if text and str(text) == element.get_attribute("innerHTML").strip().lower():
                    Settings.dev_print("found matching element!")
                    return element
                elif text and fuzzyMatch and str(text) in element.get_attribute("innerHTML").strip().lower():
                    Settings.dev_print("found matching fuzzy element!")
                    return element
                else:
                    Settings.dev_print("found matching element!")
                    return element
            i += 1
    except Exception as e:
        Settings.dev_print(e)
    raise Exception(f"unable to find element: {name}")

def move_to_then_click_element(element):
    """
    Move to then click element.
    
    From: https://stackoverflow.com/questions/44777053/selenium-movetargetoutofboundsexception-with-firefox

    Parameters
    ----------
    element : Selenium.WebDriver.WebElement
        The element to move to then click

    """

    def scroll_shim(passed_in_driver, object):
        x = object.location['x']
        y = object.location['y']
        scroll_by_coord = 'window.scrollTo(%s,%s);' % (
            x,
            y
        )
        scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
        passed_in_driver.execute_script(scroll_by_coord)
        passed_in_driver.execute_script(scroll_nav_out_of_way)
    #
    try:
        ActionChains(Driver.browser).move_to_element(element).click().perform()
        return True
    except Exception as e:
        # Settings.dev_print(e)
        # if 'firefox' in Driver.browser.capabilities['browserName']:
        try:
            scroll_shim(Driver.browser, element)
            ActionChains(Driver.browser).move_to_element(element).click().perform()
        except Exception as e:
            pass
            # Settings.dev_print(e)
            Driver.browser.execute_script("arguments[0].scrollIntoView();", element)
            # try:
            #     Driver.browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)
            #     ActionChains(Driver.browser).move_to_element(element).click().perform()
            # except Exception as e:
            #     Settings.dev_print(e)
    return False




# TODO: check
# these are probably deprecated in favor of find_element_to_click

def find_element_by_name(name):
    """
    Find element on page by name

    Does not auth check or otherwise change the focus

    Parameters
    ----------
    name : str
        The name of the element to reference from its /elements/element name

    Returns
    -------
    Selenium.WebDriver.WebElement
        The located web element if found by id, class name, or css selector

    """
    element = Element.get_element_by_name(name)
    if not element:
        Settings.err_print("unable to find element reference")
        return None
    # prioritize id over class name
    eleID = None
    try: eleID = Driver.browser.find_element(By.ID, element.getId())
    except: eleID = None
    if eleID: return eleID
    for className in element.getClasses():
        ele = None
        eleCSS = None
        try: ele = Driver.browser.find_element(By.CLASS_NAME, className)
        except: ele = None
        # try: eleCSS = Driver.browser.find_element(By.CSS_SELECTOR, className)
        # except: eleCSS = None
        Settings.dev_print("class: {} - {}:css".format(ele, eleCSS))
        if ele: return ele
        # if eleCSS: return eleCSS
    raise Exception("unable to locate element")

def find_elements_by_name(name):
    """
    Find elements on page by name. Does not change window focus.

    Parameters
    ----------
    name : str
        The name of the element to reference from its /elements/element name

    Returns
    -------
    list
        A list of the located Selenium.WebDriver.WebElements as found by id, class name, or css selector. 
        Elements must also be displayed

    """

    element = Element.get_element_by_name(name)
    if not element:
        Settings.err_print("unable to find element reference")
        return []
    eles = []
    for className in element.getClasses():
        eles_ = []
        elesCSS_ = []
        try: eles_ = Driver.browser.find_elements(By.CLASS_NAME, className)
        except: eles_ = []
        # try: elesCSS_ = Driver.browser.find_elements(By.CSS_SELECTOR, className)
        # except: elesCSS_ = []
        Settings.dev_print("class: {} - {}:css".format(len(eles_), len(elesCSS_)))
        eles.extend(eles_)
        # eles.extend(elesCSS_)
    eles_ = []
    for i in range(len(eles)):
        # Settings.dev_print("ele: {} -> {}".format(eles[i].get_attribute("innerHTML").strip(), element.getText()))
        if eles[i].is_displayed():
            Settings.dev_print("found displayed ele: {}".format(eles[i].get_attribute("innerHTML").strip()))
            eles_.append(eles[i])
    if len(eles_) == 0:
        raise Exception("unable to locate elements: {}".format(name))
    return eles_