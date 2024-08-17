import os
os.environ['ENV'] = "test"
import shutil
import unittest

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

from scripts.sync import sync_downloads, sync_uploads

import dropbox
dbx = dropbox.Dropbox(
    app_key = str(os.getenv("DROPBOX_KEY")),
    app_secret = str(os.getenv("DROPBOX_SECRET")),
    oauth2_refresh_token = str(os.getenv("DROPBOX_REFRESH_TOKEN"))
)

class Test_Sync(unittest.TestCase):

    def setUp(self):
        self.args = {
            'yes': True,
            'no' : False,
            'default': False,
            'folder' : 'Test',
            # 'rootdir' : TESTS_PATH
        }

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_sync_downloads(self):
        TESTS_PATH = os.path.expanduser("~/.onlysnarf/dropbox")
        self.args["rootdir"] = TESTS_PATH
        # clear Tests folder
        try:
            shutil.rmtree(TESTS_PATH)
        except Exception as e:
            print(e)

        # download test file from dropbox
        assert sync_downloads(self.args, dbx), "unable to sync downloads"
        size = 0
        for path, dirs, files in os.walk(os.path.join(TESTS_PATH)):
            for f in files:
                size += os.path.getsize(os.path.join(path, f))
        assert size, "unable to download synced files"

    def test_sync_uploads(self):
        TESTS_PATH = os.path.expanduser("~/.onlysnarf/dropbox/test")
        self.args["rootdir"] = TESTS_PATH
        assert sync_uploads(self.args, dbx), "unable to sync uploads"
        # TODO: add tests for checking if file has been added to dropbox

############################################################################################

if __name__ == '__main__':
    unittest.main()