import os
os.environ['ENV'] = "test"

from OnlySnarf.snarf import Snarf
from OnlySnarf.util.config import config
from OnlySnarf.util import defaults as DEFAULT

config["confirm"] = False
config["prompt"] = False # needs to be updated to do the right thing in Settings

class TestXMAS(unittest.TestCase):

    def setUp(self):
        self.test_snarf = Snarf()
        
    def tearDown(self):
        from OnlySnarf.lib.driver import Driver
        Driver.exit_all()

    def test_teaser(self):
        config["input"] = "./public/images/xmas-shnarf-tease.jpg"
        config["bykeyword"] = "xmas tease"
        config["image_limit"] = int(DEFAULT.IMAGE_LIMIT / 5)
        config["text"] = "xmas tease"
        assert self.test_snarf.post(), "unable to send xmas tease"
        config["image_limit"] = int(DEFAULT.IMAGE_LIMIT)

    def test_xmas_message(self):
        config["input"] = "./public/images/xmas-shnarf.jpg"
        config["price"] = DEFAULT.PRICE_MINIMUM
        config["text"] = "xmas message test"
        config["user"] = "recent"
        assert self.test_snarf.message(), "unable to send xmas nude message"

    def test_xmas_post(self):
        config["input"] = "./public/images/xmas-shnarf-video.mp4"
        config["price"] = DEFAULT.PRICE_MINIMUM * 10
        config["text"] = "xmas post test"
        assert self.test_snarf.post(), "unable to post xmas gift"

############################################################################################

if __name__ == '__main__':
    unittest.main()
