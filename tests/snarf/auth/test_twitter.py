# import os
# os.environ['ENV'] = "test"
# import unittest

# from OnlySnarf.util.config import get_config
# from OnlySnarf.webdriver.login import login as WEBDRIVER_login
# from OnlySnarf.util.settings import Settings

# config = {}

# class TestAuth(unittest.TestCase):

#     def setUp(self):
#         config = get_config()
#         config["login"] = "twitter"
#         Settings.set_debug("tests")

#     def tearDown(self):
#         pass

#     def test_login(self):
#         config["cookies"] = False
#         assert WEBDRIVER_login(), "unable to login"
#         config["cookies"] = True # saves cookies for next test

#     def test_login_via_cookies(self):
#         config["cookies"] = True
#         config["debug_cookies"] = True
#         assert WEBDRIVER_login(), "unable to login from cookies"

# ############################################################################################

# if __name__ == '__main__':
#     unittest.main()