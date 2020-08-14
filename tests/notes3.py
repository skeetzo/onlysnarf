
browsers = [
   {“platform”: “Windows 7 64-bit”, “browserName”: “Internet Explorer”,”version”: “10”, “name”: “Python Parallel”}, {“platform”: “Windows 8.1”, “browserName”: “Chrome”, “version”: “50”, “name”: “Python Parallel”},
]



browsers_waiting = [ ]

def get_browser_and_wait(browser_data):
   print ("starting %s\n" % browser_data["browserName"])
   browser = get_browser(browser_data)
   browser.get("http://crossbrowsertesting.com")
   browsers_waiting.append({"data": browser_data, "driver": browser})
   print ("%s ready" % browser_data["browserName"])
   while len(browsers_waiting) < len(browsers):
     print ("working on %s.... please wait" % browser_data["browserName"])
browser.get("http://crossbrowsertesting.com")
     time.sleep(3)






threads = []
for i, browser in enumerate(browsers):
   thread = Thread(target=get_browser_and_wait, args=[browser])
   threads.append(thread)
   thread.start()

for thread in threads:
   thread.join()

print ("all browsers ready")
for i, b in enumerate(browsers_waiting):
   print ("browser %s's title: %s" % (b["data"]["name"], b["driver"].title))
   b["driver"].quit()