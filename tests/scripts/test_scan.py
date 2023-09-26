import os
os.environ['ENV'] = "test"
import unittest

from scripts.scan import get_oldest_file_in_files, get_youngest_file_in_files, scan, get_upload_options, process_upload_object

# TODO: create mock files that have ages
TESTS_PATH = os.path.expanduser("~/.onlysnarf/uploads")

class Test_Scan(unittest.TestCase):

    def setUp(self):
        self.args = {
            'action': "test",
            'name': "",
            'file_count': 10,
            'directory': False,
            "oldest": False,
            "youngest": False,
            "random": False,
            'yes': True,
            'no' : False,
            'default': False,
            'config': False,
            'folder' : 'Test',
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
        assert scan(self.args), "unable to scan"

    def test_scan_for_folder(self):
        assert scan({**self.args, "directory": True}), "unable to scan directories"

    def test_scan_for_name(self):
        assert scan({**self.args, "name": "test-image"}), "unable to scan for file by name"
        assert scan({**self.args, "directory": True, "name": "testpost3"}), "unable to scan for directory by name"

    def test_scan_configs(self):
        self.args["config"] = True
        assert scan(self.args), "unable to scan configs"

    def test_get_upload_options(self):
        upload_config, upload_path = get_upload_options(self.args)
        assert upload_path, "unable to get upload path via options"

    def test_get_upload_options_config(self):
        upload_config, upload_path = get_upload_options({**self.args, "config":True})
        assert upload_config, "unable to get upload config"
        assert upload_path, "unable to get upload path via config"

    def test_process_upload_object(self):
        upload_config, upload_path = get_upload_options(self.args)
        upload_object = process_upload_object(upload_config, upload_path)
        assert upload_object, "unable to get upload object"

    def test_get_oldest_file_in_files(self):
        mock_files = [ '/home/skeetzo/.onlysnarf/uploads/test/post/testpost/test-image-younger.jpg', '/home/skeetzo/.onlysnarf/uploads/test/post/testpost/test-image.jpg' ]
        self.assertEqual(get_oldest_file_in_files(mock_files), '/home/skeetzo/.onlysnarf/uploads/test/post/testpost/test-image.jpg', "unable to get oldest file")
        mock_directory = [ '/home/skeetzo/.onlysnarf/uploads/test/post/testpost', '/home/skeetzo/.onlysnarf/uploads/test/post/testpost2' ]
        self.assertEqual(get_oldest_file_in_files(mock_directory), '/home/skeetzo/.onlysnarf/uploads/test/post/testpost', "unable to get oldest folder")

    def test_get_youngest_file_in_files(self):
        mock_files = [ '/home/skeetzo/.onlysnarf/uploads/test/post/testpost/test-image-younger.jpg', '/home/skeetzo/.onlysnarf/uploads/test/post/testpost/test-image.jpg' ]
        self.assertEqual(get_youngest_file_in_files(mock_files), '/home/skeetzo/.onlysnarf/uploads/test/post/testpost/test-image-younger.jpg', "unable to get youngest file")
        mock_directory = [ '/home/skeetzo/.onlysnarf/uploads/test/post/testpost', '/home/skeetzo/.onlysnarf/uploads/test/post/testpost2' ]
        self.assertEqual(get_youngest_file_in_files(mock_directory), '/home/skeetzo/.onlysnarf/uploads/test/post/testpost2', "unable to get youngest folder")

    def test_backup(self):
        assert scan({**self.args, "backup": True, "directory":True}), "unable to backup scanned file"

    def test_delete(self):
        assert scan({**self.args, "delete": True}), "unable to delete scanned file"

############################################################################################

if __name__ == '__main__':
    unittest.main()