import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
# from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.lib.driver import Driver
from OnlySnarf.util.settings import Settings
from OnlySnarf.snarf import Snarf
# from OnlySnarf.classes.user import User

class TestProfile(unittest.TestCase):

    def setUp(self):
        self.test_snarf = Snarf()
        Settings.set_debug("tests")
        config["prefer_local"] = False

    def tearDown(self):
        self.test_snarf.close()

    @unittest.skip("todo")
    def test_profile_backup(self):
        config["profile_method"] = "backup"
        assert self.test_snarf.profile(), "unable to backup profile"

    @unittest.skip("todo")
    def test_profile_syncfrom(self):
        config["profile_method"] = "syncfrom"
        assert self.test_snarf.profile(), "unable to sync from profile"

    @unittest.skip("todo")
    def test_profile_syncto(self):
        config["profile_method"] = "syncto"
        assert self.test_snarf.profile(), "unable to sync to profile"

############################################################################################

if __name__ == '__main__':
    unittest.main()