import flask_unittest
from flaskr.db import get_db

class TestFoo(flask_unittest.AppTestCase):

    def create_app(self):
        # Return/Yield a `Flask` object here
        pass

    def setUp(self, app):
        # Perform set up before each test, using app
        pass

    def tearDown(self, app):
        # Perform tear down after each test, using app
        pass

    '''
    Note: the setUp and tearDown method don't need to be explicitly declared
    if they don't do anything (like in here) - this is just an example
    Only declare the setUp and tearDown methods with a body, same as regular unittest testcases
    '''

    def test_foo_with_app(self, app):
        # Use the app here
        # Example of using test_request_context (on a hypothetical app)
        with app.test_request_context('/1/update'):
            self.assertEqual(request.endpoint, 'blog.update')

    def test_bar_with_app(self, app):
        # Use the app here
        # Example of using client from app (on a hypothetical app)
        with app.test_client() as client:
            rv = client.get('/hello')
            self.assertInResponse(rv, 'hello world!')

    def test_baz_with_app(self, app):
        # Use the app here
        # Example of using app_context (on a hypothetical app)
        with app.app_context():
            get_db().execute("INSERT INTO user (username, password) VALUES ('test', 'testpass');")