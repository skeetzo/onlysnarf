# TODO: requires internal updates

# import os
# os.environ['ENV'] = "test"
# import unittest

# from OnlySnarf.util.config import set_config
# CONFIG = set_config({})

# from OnlySnarf.classes.driver import create_browser
# from OnlySnarf.classes.webdriver.login import login as WEBDRIVER_login

# class TestAuth(unittest.TestCase):

#     def setUp(self):
#         self.browser = create_browser(CONFIG["browser"])
#         CONFIG["login"] = "google"
        
#     def tearDown(self):
#         self.browser.quit()

#     def test_login(self):
#         CONFIG["cookies"] = False
#         assert WEBDRIVER_login(self.browser), "unable to login"
#         CONFIG["cookies"] = True # saves cookies for next test

#     def test_login_via_cookies(self):
#         CONFIG["cookies"] = True
#         CONFIG["debug_cookies"] = True
#         assert WEBDRIVER_login(self.browser), "unable to login from cookies"

# ############################################################################################

# if __name__ == '__main__':
#     unittest.main()