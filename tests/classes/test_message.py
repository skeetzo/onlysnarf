import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({'prefer_local':True})
from OnlySnarf.util.logger import configure_logging, configure_logs_for_module_tests
configure_logging(True, True)

from OnlySnarf.classes.message import Message
from OnlySnarf.util import defaults as DEFAULT

class TestClasses_Message(unittest.TestCase):

    def setUp(self):
        # self.schedule_object = {
        #     "date" : tomorrow.strftime(DEFAULT.DATE_FORMAT),
        #     "time" : (today + datetime.timedelta(hours=1, minutes=30)).strftime(DEFAULT.TIME_FORMAT)
        # }
        self.message_object = {
            "text" : "test balls",
            "files" : [],
            "price": "0.0",
            "recipients" : ["@onlyfans"],
            # "schedule" : self.schedule_object,
            "keywords": ["balls", "deep"],
            "performers": ["yourmom", "yourdad"]
        }
        self.formatted_message_object = {
            "text": "test balls #balls #deep w/ @yourmom @yourdad",
            "files": [],
            "price": 0,
            "recipients": ["onlyfans"],
            # "schedule": self.schedule_object,
            "keywords": "#balls #deep",
            "performers": "@yourmom @yourdad"
        }

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        configure_logs_for_module_tests("OnlySnarf.classes.message")

    @classmethod
    def tearDownClass(cls):
        configure_logs_for_module_tests(flush=True)

    def test_format_keywords(self):
        self.assertEqual(Message.format_keywords(self.message_object["keywords"]), self.formatted_message_object["keywords"], "unable to format message keywords")

    def test_format_performers(self):
        self.assertEqual(Message.format_performers(self.message_object["performers"]), self.formatted_message_object["performers"], "unable to format message performers")
        
    def test_format_text(self):
        self.assertEqual(Message.format_text(self.message_object["text"], self.message_object["keywords"], \
                                                    self.message_object["performers"], self.message_object["files"]), \
                                                    self.formatted_message_object["text"], "unable to format message text")

    def test_format_recipients(self):
        self.assertEqual(Message.format_recipients(self.message_object["recipients"]), self.formatted_message_object["recipients"], "unable to format message recipients")

    def test_format_recipients_duplicates(self):
        self.message_object["recipients"].extend(self.message_object["recipients"])
        self.assertEqual(Message.format_recipients(self.message_object["recipients"]), self.formatted_message_object["recipients"], "unable to format duplicate message recipients")

    # TODO: necessary? functionality basically handled by the schedule class & tests
    # def test_format_schedule(self):
        # self.assertEqual(Message.format_schedule(self.message_object["schedule"]), self.formatted_message_object["schedule"], "unable to format message schedule")

    def test_format_files(self):
        self.assertEqual(Message.format_files(self.message_object["files"]), self.formatted_message_object["files"], "unable to format message files")
        
    def test_format_price(self):
        self.assertEqual(Message.format_price(self.message_object["price"]), self.formatted_message_object["price"], "unable to format message price")
        self.assertEqual(Message.format_price(DEFAULT.PRICE_MAXIMUM+1), DEFAULT.PRICE_MAXIMUM), "unable to format message price greater than maximum"
        self.assertEqual(Message.format_price(DEFAULT.PRICE_MINIMUM-1), DEFAULT.PRICE_MINIMUM), "unable to format message price less than minimum"
        
    def test_get_text_from_filename(self):
        from OnlySnarf.classes.file import File
        filename = "/home/skeetzo/Projects/onlysnarf/public/images/snarf.jpg"
        formatted_filename = "snarf.jpg"
        self.assertEqual(Message.get_text_from_filename(File(filename)), formatted_filename, "unable to format message files")
        
    @unittest.skip("todo")
    def test_user_on_success(self):
        assert Message.create_message(self.message_object).on_success(), "unable to process successful message"
        # TODO: get user data from file and verify that the same data has been updated
        # TODO: add asserts for checking text & files variables in user object and saved user data have been updated

############################################################################################

if __name__ == '__main__':
    unittest.main()