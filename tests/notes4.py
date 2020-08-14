# https://www.gridlastic.com/python-code-example.html

pip install pytest
pip install pytest-xdist
pip install pytest-rerunfailures


#file test_unittest.py
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
logging.basicConfig(filename="log.txt", level=logging.INFO)

class TestExamples(unittest.TestCase):

    def setUp(self):
        self.driver  = webdriver.Remote(
		command_executor="https://USERNAME:ACCESS_KEY@HUB_SUBDOMAIN.gridlastic.com/wd/hub",
		desired_capabilities={
            "browserName": "chrome",
            "browserVersion": "latest",
            "video": "True",
            "platform": "WIN10",
            "platformName": "windows",
        })
        self.driver.implicitly_wait(30)
        self.driver.maximize_window() # Note: driver.maximize_window does not work on Linux, instead set window size and window position like driver.set_window_position(0,0) and driver.set_window_size(1920,1080)

    def test_one(self):
        try:
           driver = self.driver
           driver.get("http://www.python.org")
           self.assertIn("Python", driver.title)
           elem = driver.find_element_by_name("q")
           elem.send_keys("documentation")
           elem.send_keys(Keys.RETURN)
           assert "No results found." not in driver.page_source
        finally:
           logging.info("Test One Video: " + VIDEO_URL + driver.session_id)
		   
    def test_two(self):
        try:
           driver = self.driver
           driver.get("http://www.google.com")
           elem = driver.find_element_by_name("q")
           elem.send_keys("webdriver")
           elem.send_keys(Keys.RETURN)
        finally:
           	logging.info("Test Two Video: " + VIDEO_URL + driver.session_id)
			
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()