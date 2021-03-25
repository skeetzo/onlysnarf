Executing Test Runners

The Python application that executes your test code, checks the assertions, and gives you test results in your console is called the test runner.

At the bottom of test.py, you added this small snippet of code:

if __name__ == '__main__':
    unittest.main()

This is a command line entry point. It means that if you execute the script alone by running python test.py at the command line, it will call unittest.main(). This executes the test runner by discovering all classes in this file that inherit from unittest.TestCase.

This is one of many ways to execute the unittest test runner. When you have a single test file named test.py, calling python test.py is a great way to get started.

Another way is using the unittest command line. Try this:

$ python -m unittest test

This will execute the same test module (called test) via the command line.

You can provide additional options to change the output. One of those is -v for verbose. Try that next:

$ python -m unittest -v test
test_list_int (test.TestSum) ... ok

----------------------------------------------------------------------
Ran 1 tests in 0.000s

This executed the one test inside test.py and printed the results to the console. Verbose mode listed the names of the tests it executed first, along with the result of each test.

Instead of providing the name of a module containing tests, you can request an auto-discovery using the following:

$ python -m unittest discover

This will search the current directory for any files named test*.py and attempt to test them.

Once you have multiple test files, as long as you follow the test*.py naming pattern, you can provide the name of the directory instead by using the -s flag and the name of the directory:

$ python -m unittest discover -s tests

unittest will run all tests in a single test plan and give you the results.

Lastly, if your source code is not in the directory root and contained in a subdirectory, for example in a folder called src/, you can tell unittest where to execute the tests so that it can import the modules correctly with the -t flag:

$ python -m unittest discover -s tests -t src

unittest will change to the src/ directory, scan for all test*.py files inside the the tests directory, and execute them.