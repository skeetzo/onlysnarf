import os
os.environ['ENV'] = "test"
import unittest

from scripts.scan import get_oldest_file_in_files, get_youngest_file_in_files

# TODO: create mock files that have ages
mock_files = []

class TestSelenium_Reconnect(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_get_oldest_file_in_files(self):
        assert get_oldest_file_in_files(mock_files), "unable to get oldest file"

    def test_get_youngest_file_in_files(self):
        assert get_youngest_file_in_files(mock_files), "unable to get youngest file"

############################################################################################

if __name__ == '__main__':
    unittest.main()