import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.lib.driver import Driver
from OnlySnarf.util.settings import Settings
from OnlySnarf.snarf import Snarf
# from OnlySnarf.classes.user import User

class TestIPFS(unittest.TestCase):

    def setUp(self):
        config["text"] = "shnarf!"
        config["destination"] = "IPFS"
        config["source"] = "IPFS"
        Settings.set_debug("tests")
        self.test_snarf = Snarf()

    def tearDown(self):
        config["input"] = []
        Driver.exit_all()

    @unittest.skip("todo")
    def test_backup_to_ipfs(self):
        config["input"] = ["/home/skeetzo/Projects/onlysnarf/public/images/shnarf.jpg"]
        config["backup"] = True
        # config["force_backup"] = True
        assert self.test_snarf.post(), "unable to backup content to ipfs"
        config["backup"] = False
        # config["force_backup"] = False

    @unittest.skip("todo")
    def test_post_from_ipfs(self):
        config["input"] = ["CID"] # recognize CID format and automatically attempt to use IPFS
        config["price"] = DEFAULT.PRICE_MINIMUM
        assert self.test_snarf.post(), "unable to post content from ipfs"
        config["price"] = 0

############################################################################################

if __name__ == '__main__':
    unittest.TextTestRunner().run(suite)
    # unittest.main()