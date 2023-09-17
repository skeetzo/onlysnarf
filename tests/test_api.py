import os
os.environ['ENV'] = "test"

import flask_unittest
import flask.globals

import json

from OnlySnarf.lib.api import create_app

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

    def test_message(self, client):
        mockMessage = {
            "text":"testes",
            "user":"random"
        }
        response = client.post("/message", data=json.dumps(mockMessage))
        assert response.status_code == 200

    def test_post(self, client):
        mockPost = {
            "text":"testes"
        }
        response = client.post("/post", data=json.dumps(mockPost))
        assert response.status_code == 200
