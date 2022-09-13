import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.lib.driver import Driver
from OnlySnarf.util.settings import Settings
from OnlySnarf.snarf import Snarf
# from OnlySnarf.classes.user import User

class TestSnarfIPFS(unittest.TestCase):

    def setUp(self):
        Settings.set_debug("tests")
        self.test_snarf = Snarf()

    def tearDown(self):
        Driver.exit()

    @unittest.skip("todo")
    def test_backup_to_ipfs(self):
        config["input"] = "/home/skeetzo/Projects/onlysnarf/public/images/shnarf.jpg"
        config["text"] = "shnarf!"
        config["backup"] = True
        # config["force_backup"] = True
        config["destination"] = "IPFS"
        assert self.test_snarf.post(), "unable to backup content to ipfs"

    @unittest.skip("todo")
    def test_post_from_ipfs(self):
        config["input"] = "CID" # recognize CID format and automatically attempt to use IPFS
        config["price"] = DEFAULT.PRICE_MINIMUM
        config["text"] = "test balls"
        assert self.test_snarf.post(), "unable to post content from ipfs"

############################################################################################

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    # unittest.main()