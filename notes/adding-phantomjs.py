# https://stackoverflow.com/questions/13287490/is-there-a-way-to-use-phantomjs-in-python

# The easiest way to use PhantomJS in python is via Selenium. The simplest installation method is

#     Install NodeJS
#     Using Node's package manager install phantomjs: npm -g install phantomjs-prebuilt
#     install selenium (in your virtualenv, if you are using that)

# After installation, you may use phantom as simple as:

from selenium import webdriver

driver = webdriver.PhantomJS() # or add to your PATH
driver.set_window_size(1024, 768) # optional
driver.get('https://google.com/')
driver.save_screenshot('screen.png') # save a screenshot to disk
sbtn = driver.find_element_by_css_selector('button.gbqfba')
sbtn.click()

# If your system path environment variable isn't set correctly, you'll need to specify the exact path as an argument to webdriver.PhantomJS(). Replace this:

driver = webdriver.PhantomJS() # or add to your PATH

# ... with the following:

driver = webdriver.PhantomJS(executable_path='/usr/local/lib/node_modules/phantomjs/lib/phantom/bin/phantomjs')
