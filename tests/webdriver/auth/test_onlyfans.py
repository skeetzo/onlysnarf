# import os
# os.environ['ENV'] = "test"
# import unittest

# from OnlySnarf.util.config import set_config
# CONFIG = set_config({})
# from OnlySnarf.util.logger import configure_logging, configure_logs_for_module_tests
# configure_logging(True, True)

# from OnlySnarf.lib.webdriver.cookies import reset_cookies
# from OnlySnarf.lib.webdriver.browser import create_browser as WEBDRIVER_create_browser
# from OnlySnarf.lib.webdriver.login import login as WEBDRIVER_login

# class TestAuth_OnlyFans_Webdriver(unittest.TestCase):

#     def setUp(self):
#         self.browser = WEBDRIVER_create_browser()

#     def tearDown(self):
#         self.browser.quit()

#     @classmethod
#     def setUpClass(cls):
#         configure_logs_for_module_tests("OnlySnarf.lib.webdriver.browser")
#         configure_logs_for_module_tests("OnlySnarf.lib.webdriver.login")
#         reset_cookies()

#     @classmethod
#     def tearDownClass(cls):
#         configure_logs_for_module_tests("###FLUSH###")

#     def test_login(self):
#         assert WEBDRIVER_login(self.browser), "unable to login"

# ############################################################################################

# if __name__ == '__main__':
#     unittest.main()