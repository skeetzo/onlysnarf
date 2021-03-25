import unittest


class TestSum(unittest.TestCase):

    def test_sum(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_sum_tuple(self):
        self.assertEqual(sum((1, 2, 2)), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()




Method  Equivalent to
.assertEqual(a, b)  a == b
.assertTrue(x)  bool(x) is True
.assertFalse(x)     bool(x) is False
.assertIs(a, b)     a is b
.assertIsNone(x)    x is None
.assertIn(a, b)     a in b
.assertIsInstance(a, b)     isinstance(a, b)

.assertIs(), .assertIsNone(), .assertIn(), and .assertIsInstance() all have opposite methods, named .assertIsNot(), and so forth.





An integration test checks that components in your application operate with each other.
A unit test checks a small component in your application.



Before you dive into writing tests, you’ll want to first make a couple of decisions:

    What do you want to test?
    Are you writing a unit test or an integration test?

Then the structure of a test should loosely follow this workflow:

    Create your inputs
    Execute the code being tested, capturing the output
    Compare the output with an expected result





# Note: What if your application is a single script?

# You can import any attributes of the script, such as classes, functions, and variables by using the built-in __import__() function. Instead of from my_sum import sum, you can write the following:

# target = __import__("my_sum.py")
# sum = target.sum

# The benefit of using __import__() is that you don’t have to turn your project folder into a package, and you can specify the file name. This is also useful if your filename collides with any standard library packages. For example, math.py would collide with the math module.
