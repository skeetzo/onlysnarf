https://stackoverflow.com/questions/35641019/how-do-you-use-credentials-saved-by-the-browser-in-auto-login-script-in-python-2

This is because selenium doesn't use your default browser instance, it opens a different instance with a temporary (empty) profile.

If you would like it to load a default profile you need to instruct it to do so.

Here's a chrome example:

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = webdriver.ChromeOptions() 
options.add_argument("user-data-dir=C:\\Path") #Path to your chrome profile
w = webdriver.Chrome(executable_path="C:\\Users\\chromedriver.exe", chrome_options=options)

And here's a firefox example:

from selenium import webdriver
from selenium.webdriver.firefox.webdriver import FirefoxProfile

profile = FirefoxProfile("C:\\Path\\to\\profile")
driver = webdriver.Firefox(profile)

Here we go, just dug up a link to this in the (unofficial) documentation. Firefox Profile and the Chrome driver info is right underneath it.








saving cookies

    import pickle 
    from selenium import webdriver 
    driver = webdriver.Firefox() 
    driver.get('http://www.quora.com') 
    # login code 
    pickle.dump(driver.get_cookies() , open("QuoraCookies.pkl","wb")) 

loading cookies

    import pickle 
    from selenium import webdriver 
    driver = webdriver.Firefox() 
    driver.get('http://www.quora.com') 
    for cookie in pickle.load(open("QuoraCookies.pkl", "rb")): 
        driver.add_cookie(cookie) 



# https://stackoverflow.com/questions/45651879/using-selenium-how-to-keep-logged-in-after-closing-driver-in-python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


options = Options()
options.add_argument("user-data-dir=/tmp/tarun")
driver = webdriver.Chrome(chrome_options=options)

driver.get('https://web.whatsapp.com/')
driver.quit()


# windows
options.add_argument("user-data-dir=C:\\Users\\Username\\AppData\\Local\\Google\\Chrome\\User Data")







# https://stackoverflow.com/questions/15058462/how-to-save-and-load-cookies-using-python-selenium-webdriver

import pickle
import selenium.webdriver 

driver = selenium.webdriver.Firefox()
driver.get("http://www.google.com")
pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))

and later to add them back:

import pickle
import selenium.webdriver 

driver = selenium.webdriver.Firefox()
driver.get("http://www.google.com")
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)