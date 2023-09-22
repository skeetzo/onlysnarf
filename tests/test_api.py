import os
os.environ['ENV'] = "test"

import flask_unittest
import flask.globals

import json

from OnlySnarf.util.config import set_config
CONFIG = set_config({})
from OnlySnarf.util.logger import configure_logging, configure_logs_for_module_tests
configure_logging(True, True)

from OnlySnarf.lib.api import create_app
from OnlySnarf.util import defaults as DEFAULT

class TestAPI(flask_unittest.ClientTestCase):
    # Assign the `Flask` app object
    # app = Flask(__name__)
    app = create_app()
    app.debug = True
    app.testing = True

    def setUp(self, client):
        # Perform set up before each test, using client
        pass

    def tearDown(self, client):
        # Perform tear down after each test, using client
        pass

    @classmethod
    def setUpClass(cls):
        configure_logs_for_module_tests("OnlySnarf.lib.api")
        configure_logs_for_module_tests("OnlySnarf.classes.message")
        configure_logs_for_module_tests("OnlySnarf.classes.discount")
        configure_logs_for_module_tests("OnlySnarf.lib.webdriver.discount")
        configure_logs_for_module_tests("OnlySnarf.lib.webdriver.message")
        configure_logs_for_module_tests("OnlySnarf.lib.webdriver.post")

    @classmethod
    def tearDownClass(cls):
        configure_logs_for_module_tests(flush=True)

    def test_discount(self, client):
        mockDiscount = {
            "username":"testes",
            "amount": DEFAULT.DISCOUNT_MIN_AMOUNT,
            "months": DEFAULT.DISCOUNT_MIN_MONTHS
        }
        response = client.post("/discount", data=json.dumps(mockDiscount))
        assert response.status_code == 200

    def test_message(self, client):
        mockMessage = {
            "text":"testes",
            "recipients": ["random"]
        }
        response = client.post("/message", data=json.dumps(mockMessage))
        assert response.status_code == 200

    def test_post(self, client):
        mockPost = {
            "text":"testes"
        }
        response = client.post("/post", data=json.dumps(mockPost))
        assert response.status_code == 200
