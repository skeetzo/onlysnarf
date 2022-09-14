import os
os.environ['ENV'] = "test"

from OnlySnarf.util.config import config
from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.lib.driver import Driver
from OnlySnarf.util.settings import Settings
from OnlySnarf.snarf import Snarf
# from OnlySnarf.classes.user import User

## TODO: maybe add date checks to only run tests around end of the year?

class TestXMAS(unittest.TestCase):

    def setUp(self):
        config["text"] = "xmas tests"
        Settings.set_debug("tests")
        self.test_snarf = Snarf()
        
    def tearDown(self):
        config["input"] = []
        Driver.exit()

    def test_teaser(self):
        config["input"] = ["./public/images/xmas-shnarf-tease.jpg"]
        config["bykeyword"] = "xmas tease"
        config["upload_max"] = int(DEFAULT.IMAGE_LIMIT / 5)
        assert self.test_snarf.post(), "unable to send xmas tease"
        config["bykeyword"] = []
        config["upload_max"] = int(DEFAULT.IMAGE_LIMIT)

    def test_xmas_message(self):
        config["input"] = ["./public/images/xmas-shnarf.jpg"]
        config["price"] = DEFAULT.PRICE_MINIMUM
        config["user"] = "recent"
        assert self.test_snarf.message(), "unable to send xmas nude message"
        config["price"] = 0
        config["user"] = ""

    def test_xmas_post(self):
        config["input"] = ["./public/images/xmas-shnarf-video.mp4"]
        config["price"] = DEFAULT.PRICE_MINIMUM * 10
        assert self.test_snarf.post(), "unable to post xmas gift"
        config["price"] = 0

############################################################################################

if __name__ == '__main__':
    unittest.main()
