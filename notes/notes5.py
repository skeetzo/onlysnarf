pip install pytest-selenium
pip install pytest-variables


 JSON config file (capabilities.json) 
{ "capabilities": {
	"video": "True",
	"gridlasticUser": USERNAME,
	"gridlasticKey": ACCESS_KEY
	}
}



#file test_pytest_selenium.py
import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging
logging.basicConfig(filename="log.txt", level=logging.INFO)

@pytest.fixture
def selenium(selenium):
    selenium.implicitly_wait(30)
    selenium.maximize_window()
    return selenium
	
def test_one(selenium):
	try:
		selenium.get("http://www.python.org")
		assert "Python" in selenium.title
		elem = selenium.find_element_by_name("q")
		elem.send_keys("documentation")
		elem.send_keys(Keys.RETURN)
		assert "No results found." not in selenium.page_source
	finally:
		logging.info("Test One Video: " + VIDEO_URL + selenium.session_id)

def test_two(selenium):
	try:
		selenium.get("http://www.google.com")
		elem = selenium.find_element_by_name("q")
		elem.send_keys("webdriver")
		elem.send_keys(Keys.RETURN)
	finally:
		logging.info("Test Two Video: " + VIDEO_URL + selenium.session_id)