import os
os.environ['ENV'] = "test"
import unittest

from scripts.scan_dropbox import scan

import dropbox
dbx = dropbox.Dropbox(
    app_key = str(os.getenv("DROPBOX_KEY")),
    app_secret = str(os.getenv("DROPBOX_SECRET")),
    oauth2_refresh_token = str(os.getenv("DROPBOX_REFRESH_TOKEN"))
)

class Test_Scan_Dropbox(unittest.TestCase):

    def setUp(self):
        self.args = {
            'yes': True,
            'no' : False,
            'default': False,
            'folder' : 'Test'
        }


    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_scan(self):
        assert scan_for_uploads(self.args, dbx), "unable to scan for uploads"

############################################################################################

if __name__ == '__main__':
    unittest.main()