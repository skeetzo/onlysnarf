
# Uploads a directory with a video file or image files to OnlyFans
def upload_to_OnlyFans(path=None, text="", keywords=[], performers=[], expires=False, schedule=False, poll=False):
    try:
        if not auth(): return False
        global BROWSER
        goToHome()
        if not path:
            print("Error: Missing Upload Path")
            return False
        if not text or text == None or str(text) == "None":
            print("Warning: Missing Upload Text")
            text = ""
        text = text.replace(".mp4","")
        text = text.replace(".MP4","")
        text = text.replace(".jpg","")
        text = text.replace(".jpeg","")
        if isinstance(performers, list) and len(performers) > 0: text += " w/ @"+" @".join(performers)
        if isinstance(keywords, list) and len(keywords) > 0: text += " #"+" #".join(keywords)
        text = text.strip()
        print("Uploading:")
        settings.maybePrint("- Path: {}".format(path))
        print("- Keywords: {}".format(keywords))
        print("- Performers: {}".format(performers))
        print("- Text: {}".format(text))
        print("- Tweeting: {}".format(settings.TWEETING))
        if expires: expiration(expires)
        if schedule: scheduling(schedule)
        if poll: polling(poll)
        WAIT = WebDriverWait(BROWSER, 600, poll_frequency=10)
        if str(settings.TWEETING) == "True":
            WAIT.until(EC.element_to_be_clickable((By.XPATH, ONLYFANS_TWEET))).click()
        files = []
        if str(settings.SKIP_DOWNLOAD) == "True":
            print("Warning: Unable to upload, skipped download")
            return True
        if os.path.isfile(str(path)):
            files = [str(path)]
        elif os.path.isdir(str(path)):
            # files = os.listdir(str(path))
            for file in os.listdir(str(path)):
                files.append(os.path.join(os.path.abspath(str(path)),file))
        else:
            print("Error: Unable to parse path")
            return False
        if str(settings.SKIP_UPLOAD) == "True":
            print("Skipping Upload")
            return True
        files = files[:int(settings.IMAGE_UPLOAD_MAX)]
        for file in files:  
            print('Uploading: '+str(file))
            BROWSER.find_element_by_id(ONLYFANS_UPLOAD_PHOTO).send_keys(str(file))
        maxUploadCount = 12 # 2 hours max attempt time
        i = 0
        while True:
            try:                
                WAIT.until(EC.element_to_be_clickable((By.XPATH, SEND_BUTTON_XPATH)))
                break
            except Exception as e:
                # try: 
                #     # check for existence of "thumbnail is fucked up" modal and hit ok button
                #     BROWSER.switchTo().frame("iframe");
                #     BROWSER.find_element_by_class("g-btn m-rounded m-border").send_keys(Keys.ENTER)
                #     print("Error: Thumbnail Missing")
                #     break
                # except Exception as ef:
                #     settings.maybePrint(ef)
                print('uploading...')
                settings.maybePrint(e)
                i+=1
                if i == maxUploadCount and settings.FORCE_UPLOAD is not True:
                    print('Error: Max Upload Time Reached')
                    return False
        try:
            BROWSER.find_element_by_id(ONLYFANS_POST_TEXT_CLASS).send_keys(str(text))
            # first one is disabled
            # sends = BROWSER.find_elements_by_class_name(SEND_BUTTON_CLASS)
            sends = BROWSER.find_elements_by_xpath("//button[@class='{}']".format(SEND_BUTTON_CLASS))

            send = None
            for i in range(len(sends)):
                print(sends[i].get_attribute("innerHTML"))
                if sends[i].is_enabled():
                    send = sends[i]
            if str(settings.DEBUG) == "True" and str(settings.DEBUG_DELAY) == "True":
                time.sleep(int(settings.DEBUG_DELAY_AMOUNT))
            if str(settings.DEBUG) == "True":
                print('Skipped: OnlyFans Upload (debug)')
                return True
            if send:
                send.click()
            else:
                send = BROWSER.find_element_by_class_name(SEND_BUTTON_CLASS)
                if send:
                    send.click()
                else:
                    print("Warning: Unable to Send Post")
                    return
        except Exception as e:
            if "Unable to locate element" in str(e):
                print("Unable to locate send, retrying")
                send = BROWSER.find_element_by_class_name(SEND_BUTTON_CLASS)
                if send:
                    send.click()
                else:
                    print("Warning: Unable to Send Post")
                    return
            else:
                settings.maybePrint(e)
            # if error message
            # print("Warning: Upload Error Message, Closing")
            try:
                buttons = BROWSER.find_elements_by_class_name(ONLYFANS_UPLOAD_BUTTON)
                for butt in buttons:
                    if butt.get_attribute("innerHTML").strip() == "Close":
                        butt.click()
                        settings.maybePrint("Success: Upload Error Message Closed")
                send_text = BROWSER.find_element_by_id(ONLYFANS_POST_TEXT_CLASS)
                send_text.clear()
                send_text.send_keys(str(text))
                # first one is disabled
                sends = BROWSER.find_elements_by_class_name(SEND_BUTTON_CLASS)
                send = None
                for i in range(len(sends)):
                    if sends[i].is_enabled():
                        send = sends[i]
                if str(settings.DEBUG) == "True" and str(settings.DEBUG_DELAY) == "True":
                    time.sleep(int(settings.DEBUG_DELAY_AMOUNT))
                if str(settings.DEBUG) == "True":
                    print('Skipped: OnlyFans Upload (debug)')
                    return True
                if send:
                    send.click()
                else:
                    send = BROWSER.find_element_by_class_name(SEND_BUTTON_CLASS)
                    if send:
                        send.click()
                    else:
                        print("Warning: Unnable to Send Post")
                        return
            except Exception as e:
                print("Error: Unnable to Upload Images")
                settings.maybePrint(e)
                return False
        # send[1].click() # the 0th one is disabled
        print('OnlyFans Upload Complete')
        return True
    except Exception as e:
        settings.maybePrint(e)
        print("Error: OnlyFans Upload Failure")
        return False
