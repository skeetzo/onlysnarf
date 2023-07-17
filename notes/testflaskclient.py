import flask_unittest
import flask.globals

class TestAPI(flask_unittest.ClientTestCase):
    # Assign the `Flask` app object
    app = ...

    def setUp(self, client):
        # Perform set up before each test, using client
        pass

    def tearDown(self, client):
        # Perform tear down after each test, using client
        pass

    '''
    Note: the setUp and tearDown method don't need to be explicitly declared
    if they don't do anything (like in here) - this is just an example
    Only declare the setUp and tearDown methods with a body, same as regular unittest testcases
    '''

    def test_foo_with_client(self, client):
        # Use the client here
        # Example request to a route returning "hello world" (on a hypothetical app)
        rv = client.get('/hello')
        self.assertInResponse(rv, 'hello world!')

    def test_bar_with_client(self, client):
        # Use the client here
        # Example login request (on a hypothetical app)
        rv = client.post('/login', {'username': 'pinkerton', 'password': 'secret_key'})
        # Make sure rv is a redirect request to index page
        self.assertLocationHeader('http://localhost/')
        # Make sure session is set
        self.assertIn('user_id', flask.globals.session)