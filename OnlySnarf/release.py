
def release(opt, methodChoice="random", file=None):
    print("0/3 : Deleting Locals")
    remove_local()
    sys.stdout.flush()
    #################################################
    print("1/3 : Running - {}".format(opt))
    if str(opt) == "image":
        released = release_image(methodChoice, file)
    elif str(opt) == "video":
        released = release_video(methodChoice, file)
    elif str(opt) == "gallery":
        released = release_gallery(methodChoice, file)
    elif str(opt) == "performer":
        released = release_performer(methodChoice, file)
    elif str(opt) == "scene":
        released = release_scene(methodChoice, file)
    else:
        print('Missing Args!')
        return
    sys.stdout.flush()
    if released == False:
        print("Error: Failed to release - {}".format(opt))
        return
    #################################################
    print('2/3 : Cleaning Up Files')
    remove_local()
    print('Files Cleaned ')
    #################################################
    print('3/3 : Google Drive to OnlyFans Upload Complete')
    sys.stdout.flush()
    OnlySnarf.exit()

def release_image(methodChoice="random", file=None):
    try:
        print("Releasing Image")
        response = download("image", methodChoice=methodChoice, file=file)
        if response == None:
            print("Error: Failure Releasing Image")
            return False
        # settings.maybePrint("Image: {}".format(response))
        text = None
        content = None
        file = None
        keywords = None
        try:
            text = response[0]
            content = response[1]
            file = response[2]
            keywords = response[3].split(" ")
        except Exception as e:
            settings.maybePrint(e)
        if str(keywords) == " " or str(keywords[0]) == " ":
            keywords = []
        if text == None:
            print("Error: Missing Image Title")
            return False
        if content == None:
            print("Error: Missing Image Content")
            return False
        if file == None:
            print("Error: Missing Image File")
            return False
        if keywords == None:
            print("Warning: Missing Image Keywords")
        print("Image:")
        print("- Title: {}".format(text)) # name of scene
        print("- Keywords: {}".format(keywords)) # text sent in messages
        print("- Content: {}".format(content)) # the file(s) to upload
        successful = upload("image", path=content, text=text, keywords=keywords)
        if successful:
            Google.move_file(file)
        else:
            return False
        return True
    except Exception as e:
        settings.maybePrint(e)
        return False

def release_gallery(methodChoice="random", file=None):
    try:
        print("Releasing Gallery")
        response = download("gallery", methodChoice=methodChoice, file=file)
        if response == None:
            print("Error: Failure Releasing Gallery")
            return False
        # settings.maybePrint("Gallery: {}".format(response))
        text = None
        content = None
        google_file = None
        google_files = None
        keywords = None
        try:
            text = response[0]
            content = response[1]
            google_file = response[2]
            google_files = response[3]
            keywords = response[4].split(" ")
        except Exception as e:
            settings.maybePrint(e)
        if keywords == " " or str(keywords[0]) == " ":
            keywords = []
        if text == None:
            print("Error: Missing Gallery Title")
            return False
        if content == None:
            print("Error: Missing Gallery Content")
            return False
        if google_file == None:
            print("Error: Missing Gallery File")
            return False
        if google_files == None or len(google_files) == 0:
            print("Error: Missing Gallery Files")
            return False
        if str(keywords) == None:
            print("Warning: Missing Gallery Keywords")
        print("Gallery:")
        print("- Title: {}".format(text)) # name of scene
        print("- Keywords: {}".format(keywords)) # text sent in messages
        print("- Content: {}".format(content)) # the file(s) to upload
        files = os.listdir(content)
        file = files[0]
        ext = str(os.path.splitext(file)[1].lower())
        settings.maybePrint('ext: '+str(ext))
        successful = upload("gallery", path=content, text=text, keywords=keywords)
        if successful:
            Google.move_files(google_file['title'], google_files)
        else:
            return False
        return True
    except Exception as e:
        settings.maybePrint(e)
        return False

def release_performer(methodChoice="random", file=None):
    try:
        print("Releasing Performer")
        response = download("performer", methodChoice=methodChoice, file=file)
        if response == None:
            print("Error: Failure Releasing Performer")
            return False
        # settings.maybePrint("Performer: {}".format(response))
        text = None
        performer = None
        content = None
        google_file = None
        folder_name = None
        try:
            content = response[0]
            google_file = response[1]
            performer = response[2]
            text = response[3]
            folder_name = response[4]
        except Exception as e:
            settings.maybePrint(e)
        if text == None:
            print("Error: Missing Performer Text")
            return False
        if performer == None:
            print("Error: Missing Performer Name")
            return False
        if content == None:
            print("Error: Missing Performer Content")
            return False
        text += " w/ @{}".format(performer)
        print("Performer:")
        print("- Performer: {}".format(performer)) # name of scene
        print("- Text: {}".format(text)) # name of scene
        print("- Content: {}".format(content)) # the file(s) to upload
        files = os.listdir(content)
        file = files[0]
        ext = str(os.path.splitext(file)[1].lower())
        settings.maybePrint('ext: '+str(ext))
        if ext == ".mp4":
            successful = upload("video", path=content, text=text) 
        else:
            successful = upload("gallery", path=content, text=text)
        if successful:
            Google.move_file(google_file)
        else:
            return False
        return True
    except Exception as e:
        settings.maybePrint(e)
        return False
    
# upload a file or gallery
# send a message to [recent, all, user] w/ a preview image
def release_scene(methodChoice="random", file=None):
    try:
        print("Releasing Scene")
        response = download("scene", methodChoice=methodChoice, file=file)
        if response == None:
            print("Error: Failure Releasing Scene")
            return False
        # settings.maybePrint("Scene: {}".format(response))
        content = response[0]
        preview = response[1]
        data = response[2]
        google_folder = response[3]
        # print("Data:\n{}".format(json.dumps(data, sort_keys=True, indent=4)))
        data = json.loads(json.dumps(data))
        settings.maybePrint("Data: {}".format(data))
        title = None
        message = None
        price = None
        text = None
        performers = None
        keywords = None
        users = None
        title = data["title"]
        message = data["message"]
        price = data["price"]
        text = data["text"]
        performers = data["performers"]
        keywords = data["keywords"]
        if str(keywords) == " " or str(keywords[0]) == " ":
            keywords = []
        users = data["users"]
        if title == None:
            print("Error: Missing Scene Title")
            return False
        if message == None:
            print("Error: Missing Scene Message")
            return False
        if price == None:
            print("Error: Missing Scene Price")
            return False
        if text == None:
            print("Error: Missing Scene Text")
            return False
        print("Scene:")
        print("- Title: {}".format(title)) # name of scene
        print("- Text: {}".format(text)) # text entered into file upload
        print("- Price: {}".format(price)) # price of messages sent
        print("- Message: {}".format(message)) # text sent in messages
        print("- Keywords: {}".format(keywords)) # text sent in messages
        print("- Performers: {}".format(performers)) # text sent in messages
        print("- Preview: {}".format(preview)) # image sent in messages
        print("- Content: {}".format(content)) # the file(s) to upload
        print("- Users: {}".format(users)) # the file(s) to upload 
        files = os.listdir(content)
        file = files[0]
        ext = str(os.path.splitext(file)[1].lower())
        settings.maybePrint('ext: '+str(ext))
        successful_upload = False
        if not ext or ext == '.mp4':
            successful_upload = upload("video", path=content, text=text, keywords=keywords, performers=performers)
        elif ext == '.jpg' or ext == '.jpeg' and len(files) > 1:
            successful_upload = upload("gallery", path=content, text=text, keywords=keywords, performers=performers)
        elif ext == '.jpg' or ext == '.jpeg' and len(files) == 1:
            successful_upload = upload("image", path=content, text=text, keywords=keywords, performers=performers) 
        else:
            print("Error: Missing Scene Type")
        if successful_upload:
            if str(users[0]) == "all" or str(users[0]) == str("recent") or str(users[0]) == str("favorites"):
                users = users[0]
            if not users or str(users).lower() == "none":
                print("Warning: Missing User Choice")
            elif str(users) == "all" or str(users) == "recent" or str(users) == "favorites":
                successful_message = OnlySnarf.message(choice=str(users), message=message, image=preview, price=price)
            else:
                for user in users:
                    successful_message = OnlySnarf.message(choice="user", message=message, image=preview, price=price, username=user)
            if successful_message:
                Google.move_file(google_folder)
            else:
                print("Error: Failure Messaging")
                return False
        else:
            print("Error: Failure Uploading")
            return False
        return True
    except Exception as e:
        settings.maybePrint(e)
        return False

def release_video(methodChoice="random", file=None):
    try:
        print("Releasing Video")
        response = download("video", methodChoice=methodChoice, file=file)
        if response == None:
            print("Error: Failure Releasing Video")
            return False
        # settings.maybePrint("Video: {}".format(response))
        text = None
        content = None
        file = None
        keywords = None
        try:
            text = response[0]
            content = response[1]
            file = response[2]
            keywords = response[3].split(" ")
        except Exception as e:
            settings.maybePrint(e)
        if str(keywords) == " " or str(keywords[0]) == " ":
            keywords = []
        ext = str(os.path.splitext(text)[1].lower())
        settings.maybePrint('ext: '+str(ext))
        if ext == '.mp4':
            settings.maybePrint("pruning extension")
            text = os.path.splitext(text)[0]
        if text == None:
            print("Error: Missing Video Title")
            return False
        if content == None:
            print("Error: Missing Video Content")
            return False
        if file == None:
            print("Error: Missing Video File")
            return False
        if keywords == None:
            print("Warning: Missing Video Keywords")
        print("Video:")
        print("- Title: {}".format(text)) # name of scene
        print("- Keywords: {}".format(keywords)) # text sent in messages
        print("- Content: {}".format(content)) # the file(s) to upload
        successful = upload("video", path=content, text=text, keywords=keywords)
        if successful:
            Google.move_file(file)
        else:
            return False
        return True
    except Exception as e:
        settings.maybePrint(e)
        return False
