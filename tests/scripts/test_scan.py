import os
os.environ['ENV'] = "test"
import unittest

from scripts.scan import get_oldest_file_in_files, get_youngest_file_in_files, scan

# TODO: create mock files that have ages
TESTS_PATH = os.path.expanduser("~/.onlysnarf/uploads/tests")

class TestSelenium_Reconnect(unittest.TestCase):

    def setUp(self):
        self.args = {
            'action': "post",
            'name': "",
            "oldest": False,
            "youngest": False,
            "random": False,
            'yes': True,
            'no' : False,
            'default': False,
            'config': False,
            'folder' : 'Tests',
            'rootdir' : TESTS_PATH
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
        # use a mock directory
        # create and use mock files in the mock directory

        assert scan(self.args), "unable to scan"

    # @unittest.skip("todo")
    # def test_get_file_or_folder_to_upload(self):
    #     # figure out how to mock each search setting: {'random': False,'oldest': False,'youngest': False,'name':False,'file':False,'folder':False}
    #     pass

    # @unittest.skip("todo")
    # def test_get_oldest_file_in_files(self):
    #     # use the mock directory
    #     assert get_oldest_file_in_files(mock_files), "unable to get oldest file"

    # @unittest.skip("todo")
    # def test_get_youngest_file_in_files(self):
    #     # use the mock directory
    #     assert get_youngest_file_in_files(mock_files), "unable to get youngest file"

############################################################################################

if __name__ == '__main__':
    unittest.main()