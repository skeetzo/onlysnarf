FFMPEG / Video
---------
combine
gifify
frames
repair
reduce
split
thumbnail_fix
trim
watermark
metadata


Google
---------
download
get_folder_by_id
download_message_image
download_content
download_performer
download_scene

get_file
get_images
get_galleries
get_videos
get_message_image
get_random_image
get_random_gallery
get_random_performer
get_random_video
get_random_scene

download_random_files
random_download
upload_file
upload_gallery
upload_input
---------------
get_

if str(config.VERSION) == "True": return config.version_check()


def download(fileChoice, methodChoice="random", file=None):
    if methodChoice == "random":
        return random_download(fileChoice)
    elif methodChoice == "choose" and file is not None:
        if fileChoice == 'image' or fileChoice == 'video':
            return download_file(file)
        elif fileChoice == 'gallery':
            return download_gallery(file)
        elif fileChoice == 'performer':
            if "folder" in file.get("mimeType"):
                return download_content(file)
            else:          
                return download_file(file)  
#################################################################
        elif fileChoice == 'scene':
            return download_scene(file)
#################################################################
    else:
        print("Error: Unable to Download")
        return None

def download_content(folder):
    if not folder:
        print("Error: Missing Folder")
        return
    checkAuth()
    print('Downloading Content: {}'.format(folder['title']))
    # mkdir /tmp
    content_title = folder['title']
    # download folder
    # file_list = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and (mimeType contains 'image/jpeg' or mimeType contains 'image/jpg' or mimeType contains 'image/png' or (mimeType contains 'video/mp4' or mimeType contains 'video/quicktime'))"}).GetList()
    image_list = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and {}".format(MIMETYPES_IMAGES)}).GetList()
    video_list = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and {}".format(MIMETYPES_VIDEOS)}).GetList()
    file_list = []
    for i in image_list: file_list.append(i)
    for v in video_list: file_list.append(v)
    folder_size = len(file_list)
    settings.maybePrint('Images: {}'.format(len(image_list)))
    settings.maybePrint('Videos: {}'.format(len(video_list)))
    settings.maybePrint('Total: {}'.format(folder_size))
    # settings.maybePrint("Files: {}".format(file_list))
    content = {}
    file = None
    # if it contains only 1 file, I want to download a file
    if int(folder_size) == 1:
        file = file_list[0]
        content = download_file(file)
    # if it contains multiple images, I want to download a gallery
    elif int(len(image_list)) > 1:
        file = content_found
        content = download_gallery(file)
    # if it contains only 1 image, I want to download a file
    elif int(len(image_list)) == 1:
        file = image_list[0]
        content = download_gallery(file)
    # if it contains at least 1 video, I want to download a random file
    elif int(len(video_list)) >= 1:
        file = file_list[0]
        content = download_file(file)
    elif int(folder_size) == 0:
        print("Warning: Missing Files")
    content["file"] = file
    content["keywords"] = content_title
    print('Downloaded: Content')
    return content

# Download Performer
def download_performer(folder):
    if not folder:
        print("Error: Missing Folder")
        return
    checkAuth()
    print('Downloading Performer: {}'.format(folder['title']))
    # mkdir /tmp
    tmp = settings.get_tmp()
    content_folders = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
    content_found = []
    random_content = None
    content_title = None
    for folder in content_folders:
        settings.maybePrint('content: '+folder['title'])
        content_list = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and {}".format(MIMETYPES_ALL)}).GetList()
        # video_list = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and (mimeType contains 'image/jpeg' or mimeType contains 'image/jpg' or mimeType contains 'image/png')"}).GetList()
        # image_list = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'video/mp4'"}).GetList()
        if len(content_list) == 0:
            settings.maybePrint('- skipping empty content: '+folder['title'])
        if len(content_list) > 0:
            settings.maybePrint('- content galleries found: '+folder['title'])
            content_found.append(folder)
    if len(content_found)==0:
        print('Warning: Missing Content Folder')
        return {"file":"","keywords":""}
    content_found = random.choice(content_found)
    content_title = content_found['title']
    settings.maybePrint("Folder: {}".format(content_title))
    content = download_content(content_found)
    print('Downloaded: Performer')
    return content

# Download Scene
def download_scene(sceneFolder):
    checkAuth()
    print('Downloading Scene')
    tmp = settings.get_tmp()
    content = None
    preview = None
    folder_list = PYDRIVE.ListFile({'q': "'"+sceneFolder['id']+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
    for folder in folder_list:
        if folder['title'] == "content":
            content = folder
            settings.maybePrint("Content Folder: "+folder['id'])
        elif folder['title'] == "preview":
            preview = folder
            settings.maybePrint("Preview Folder: "+folder['id'])
    data = PYDRIVE.ListFile({'q': "'"+sceneFolder['id']+"' in parents and trashed=false and mimeType contains 'text/plain'"}).GetList()
    if len(data) == 0:
        print("Error: Missing Scene Data")
        return
    data = data[0]
    if data is None:
        print("Error: Missing Scene Data")
        return
    if content is None:
        print("Error: Missing Scene Content Folder")
        return
    if preview is None:
        print("Error: Missing Scene Preview Folder")
        return
    # tries to download as gallery first, then finds first video file
    content_ = None
    try:
        content_ = download_gallery(content)
    except Exception as e:
        print("1:" +str(e))
    if content_ is None:
        try:
            content_ = PYDRIVE.ListFile({'q': "'"+content['id']+"' in parents and trashed=false and mimeType != 'application/vnd.google-apps.folder'"}).GetList()
            content_ = download_file(content_[0])
        except Exception as e:
            print("2: "+str(e))
    content = content_
    if content is None:
        print("Error: Unable to Find Content")
        return
    # move content to tmp/content
    tmp_content = os.path.join(content[1], "content")
    settings.maybePrint("Old Content Path: {}".format(content[1]))
    settings.maybePrint("New Content Path: {}".format(tmp_content))
    os.mkdir(tmp_content)
    for file in os.listdir(content[1]):
        file = os.path.join(content[1], file) 
        settings.maybePrint("Moving: {}".format(file))
        shutil.move(file, tmp_content)
    data.GetContentFile(os.path.join(tmp, "data.json"))
    # read data.json    
    with open(os.path.join(tmp, "data.json"), 'r', encoding='utf-8') as f:
        data = json.load(f)
    settings.maybePrint("data.json: {}".format(data))
    preview = PYDRIVE.ListFile({'q': "'"+preview['id']+"' in parents and trashed=false and {}".format(MIMETYPES_IMAGES)}).GetList()
    if len(preview) == 0:
        print("Error: Missing Scene Preview")
        return
    preview = preview[0]
    preview = download_file(preview)
    if "mp4" in preview:
        preview = thumbnail_fix(preview)
    if data is None:
        print("Error: Missing Scene Data")
        return
    if content is None:
        print("Error: Missing Scene Content")
        return
    if preview is None:
        print("Error: Missing Scene Preview")
        return
    print('Downloaded: Scene')
    return {"path":tmp_content,"preview":preview,"data":data,"content":content}

def get_random_files():
    files = []
    if str(settings.TYPE) == "image" and str(settings.METHOD) == "random":
        files = [Google.get_random_image()]
    elif str(settings.TYPE) == "image":
        files = Google.get_images()
    elif str(settings.TYPE) == "gallery" and str(settings.METHOD) == "random":
        files = Google.get_random_gallery()
    elif str(settings.TYPE) == "gallery":
        files = Google.get_galleries()
    elif str(settings.TYPE) == "video" and str(settings.METHOD) == "random":
        files = Google.get_random_video()
    elif str(settings.TYPE) == "video":
        files = Google.get_videos()
    else: 
        print("Error: Missing Type")
        return False
    # if str(settings.TYPE) == "image" or str(settings.TYPE) == "None": 
    if str(settings.TYPE) == "gallery":
        folders = []
        for file_ in files:
            try:
                if file_.get("mimeType") and file_.get("mimeType") == "application/vnd.google-apps.folder":
                    folders.append(file_)
            except: pass
        file = random.choice(folders)











































































##################
##### Random #####
##################

def random_download(fileChoice):
    print('Random: {}'.format(fileChoice))
    file = None
    file_ = None
    data = None
    keywords = None
    performers = None
    try:
        if fileChoice == 'image':
            file = get_random_image()
            data = download_file(file)
        elif fileChoice == 'gallery':
            file = get_random_gallery()
            data = download_gallery(file)
        elif fileChoice == 'performer':
            file = get_random_performer()
            data = download_performer(file)
            performers = file.get("title").split(" ")
            file_ = data.get("file")
            keywords = data.get("keywords")
        elif fileChoice == 'scene':
            file = get_random_scene()
            return download_scene(file)
        elif fileChoice == 'video':
            file = get_random_video()
            data = download_file(file)
        else:
            return print("Error: Missing File Choice")
        if file == None or data == None:
            print("Error: Missing Random File(s)")
            return {"path":"","file":"","files":[],"keywords":"","performers":[]}
    except Exception as e:
        settings.maybePrint(e)
        return {"path":"","file":"","files":[],"keywords":"","performers":[]}
    return {"path":data.get("path"), "file":file_ or file, "files":data.get("files"), "keywords":keywords or file.get("keywords"), "performers":performers}


# Downloads random image from Google Drive
def get_random_image():
    checkAuth()
    print('Getting Random Image')
    random_folders = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'".format(get_folder_by_name("images")['id'])}).GetList()
    images_list = []
    random_image = None
    folder_name = None
    if random_folders == None:
        print("Error: Unable to Connect to Google Drive")
        return {"file":"","keywords":""}
    for folder in random_folders:
        if str(settings.VERBOSE) == "True":
            print("checking folder: {}".format(folder['title']),end="")
        images_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and {}".format(MIMETYPES_IMAGES)}).GetList()      
        if settings.BYKEYWORD != None and str(settings.BYKEYWORD) != str(folder['title']):
            settings.maybePrint('-> not keyword')
            continue
        elif settings.NOTKEYWORD != None and str(settings.NOTKEYWORD) != str(folder['title']):
            settings.maybePrint('-> by not keyword')
            continue
        if len(images_list_tmp)>0:
            images_list.append(folder)
            settings.maybePrint(" -> added")
        else:
            settings.maybePrint(" -> empty")
    if len(images_list)==0:
        print('Error: Missing Image File')
        return {"file":"","path":""}
    random_image = random.choice(images_list)
    folder_name = random_image['title'];
    print('Random Folder: '+random_image['title'])
    random_image = PYDRIVE.ListFile({'q': "'"+random_image['id']+"' in parents and trashed=false and {}".format(MIMETYPES_IMAGES)}).GetList()
    random_image = random.choice(random_image)
    print('Random Image: '+random_image['title'])
    file = Google_File()
    setattr(file, "file", random_image)
    setattr(file, "keywords", str(folder_name))
    return file

# Downloads random gallery from Google Drive
def get_random_gallery():
    checkAuth()
    print('Getting Random Gallery')
    random_folders = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'".format(get_folder_by_name("galleries")['id'])}).GetList()
    folder_list = []
    random_gallery = None
    folder_name = None
    if random_folders == None:
        print("Error: Unable to Connect to Google Drive")
        return {"file":"","keywords":""}
    for folder in random_folders:
        if str(settings.VERBOSE) == "True":
            print('checking galleries: {}'.format(folder['title']),end="")
        gallery_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
        if settings.BYKEYWORD != None and str(settings.BYKEYWORD) != str(folder['title']):
            settings.maybePrint('-> not keyword')
            continue
        elif settings.NOTKEYWORD != None and str(settings.NOTKEYWORD) != str(folder['title']):
            settings.maybePrint('-> by not keyword')
            continue
        if len(gallery_list_tmp)>0:
            folder_list.append(folder)
            settings.maybePrint(" -> added")
        else:
            settings.maybePrint(" -> empty")
    random.shuffle(folder_list)
    for folder in folder_list:
        if str(settings.VERBOSE) == "True":
            print('checking gallery: {}'.format(folder['title']),end="")
        gallery_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
        random_gallery_tmp = random.choice(gallery_list_tmp)
        gallery_list_tmp_tmp = PYDRIVE.ListFile({'q': "'"+random_gallery_tmp['id']+"' in parents and trashed=false and {}".format(MIMETYPES_IMAGES)}).GetList()
        if len(gallery_list_tmp_tmp)>0:
            settings.maybePrint(" -> found")
            random_gallery = Folder()
            setattr(random_gallery, "files", gallery_list_tmp_tmp)
            setattr(random_gallery, "keywords", folder['title'])
        else:
            settings.maybePrint(" -> empty")
    if not random_gallery:
        print('Error: Missing Gallery Folder')
        return None
        # return {"file":"","keywords":""}
    print('Random Gallery: '+random_gallery['title'])
    return random_gallery

# Downloads random performer from Google Drive
def get_random_performer():
    checkAuth()
    print('Getting Random Performer')
    random_folders = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'".format(get_folder_by_name("performers")['id'])}).GetList()
    performer_list = []
    random_performer = None
    # print('random folders: '+str(random_folders))
    if random_folders == None:
        print("Error: Unable to Connect to Google Drive")
        return {"file":"","keywords":""}
    for folder in random_folders:
        # random_folder_folder = random.choice(random_folders)
        settings.maybePrint('random performer: '+folder['title'])
        performer_content_list = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
        # print('random folders: '+str(performer_list))
        if settings.BYKEYWORD != None and str(settings.BYKEYWORD) != str(folder['title']): 
            settings.maybePrint('- skipping nonkeyword: '+folder['title'])
            continue
        elif settings.NOTKEYWORD != None and str(settings.NOTKEYWORD) != str(folder['title']):
            settings.maybePrint('-> by not keyword')
            continue
        if len(performer_content_list)==0:
            settings.maybePrint('- skipping empty performer: '+folder['title'])
        elif len(performer_content_list)>0:
            settings.maybePrint('- performer found: '+folder['title'])
            performer_list.append(folder)
    if len(performer_list)==0:
        print('Error: Missing Performer Folder')
        return {"file":"","keywords":""}
    random_performer = random.choice(performer_list)
    performer = Google_File()
    setattr(performer, "file", random_performer)
    print('Random Performer: '+performer['title'])
    return performer

# Downloads random video from Google Drive
def get_random_video():
    checkAuth()
    print('Getting Random Video')
    random_folders = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'".format(get_folder_by_name("videos")['id'])}).GetList()
    video_list = []
    random_video = None
    folder_name = None
    if random_folders == None:
        print("Error: Unable to Connect to Google Drive")
        return {"file":"","keywords":""}
    for folder in random_folders:
        if str(settings.VERBOSE) == "True":
            print("checking folder: {}".format(folder['title']),end="")
        video_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and {}".format(MIMETYPES_VIDEOS)}).GetList()
        if settings.BYKEYWORD != None and str(settings.BYKEYWORD) != str(folder['title']):
            settings.maybePrint('-> not keyword')
            continue
        elif settings.NOTKEYWORD != None and str(settings.NOTKEYWORD) != str(folder['title']):
            settings.maybePrint('-> by not keyword')
            continue
        if len(video_list_tmp)>0:
            video_list.append(folder)
            settings.maybePrint(" -> added")
        else:
            settings.maybePrint(" -> empty")
    if len(video_list)==0:
        print('Error: Missing Video File')
        return {"file":"","keywords":""}
    random_video = random.choice(video_list)
    folder_name = random_video['title'];
    print('Random Folder: '+random_video['title'])
    random_video = PYDRIVE.ListFile({'q': "'"+random_video['id']+"' in parents and trashed=false and {}".format(MIMETYPES_VIDEOS)}).GetList()
    random_video = random.choice(random_video)
    print('Random Video: '+random_video['title'])
    video = Google_File()
    setattr(video, "file", random_video)
    setattr(video, "keywords", folder_name)
    return video

# Downloads random scene from Google Drive
def get_random_scene():
    checkAuth()
    print('Getting Random Scene')
    random_folders = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'".format(get_folder_by_name("scenes")['id'])}).GetList()
    folder_list = []
    random_scene = None
    folder_name = None
    if random_folders == None:
        print("Error: Unable to Connect to Google Drive")
        return {"file":"","keywords":""}
    for folder in random_folders:
        if str(settings.VERBOSE) == "True":
            print('checking scenes: '+folder['title'],end="")
        scene_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
        if settings.BYKEYWORD != None and str(settings.BYKEYWORD) != str(folder['title']):
            settings.maybePrint('-> not keyword')
            continue
        elif settings.NOTKEYWORD != None and str(settings.NOTKEYWORD) != str(folder['title']):
            settings.maybePrint('-> by not keyword')
            continue
        if len(scene_list_tmp)>0:
            folder_list.append(folder)
            settings.maybePrint(" -> added")
        else:
            settings.maybePrint(" -> empty")
    random.shuffle(folder_list)
    for folder in folder_list:
        if str(settings.VERBOSE) == "True":
            print('checking scene: '+folder['title'],end="")
        scene_list_tmp_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'text/plain'"}).GetList()
        if len(scene_list_tmp_tmp)>0:
            folder_name = folder['title']
            random_scene = folder
            settings.maybePrint(" -> found")
        else:
            settings.maybePrint(" -> empty")
    if not random_scene:
        print('Error: Missing Scene Folders')
        return {"file":"","keywords":""}
    print('Random Scene: '+random_scene['title'])
    scene = Google_File()
    setattr(scene, "file", random_scene)
    setattr(scene, "keywords", folder_name)
    return scene











































































































































def encounter2b():
    prompt({
        'type': 'list',
        'name': 'weapon',
        'message': 'Pick one',
        'choices': [
            'Use the stick',
            'Grab a large rock',
            'Try and make a run for it',
            'Attack the wolf unarmed'
        ]
    }, style=custom_style_2)
    print('The wolf mauls you. You die. The end.')



class PhoneNumberValidator(Validator):
    def validate(self, document):
        ok = regex.match('^([01]{1})?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\s?((?:#|ext\.?\s?|x\.?\s?){1}(?:\d+)?)?$', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid phone number',
                cursor_position=len(document.text))  # Move cursor to end


print('Hi, welcome to Python Pizza')

questions = [
    {
        'type': 'confirm',
        'name': 'toBeDelivered',
        'message': 'Is this for delivery?',
        'default': False
    },
    {
        'type': 'input',
        'name': 'phone',
        'message': 'What\'s your phone number?',
        'validate': PhoneNumberValidator
    },
    {
        'type': 'list',
        'name': 'size',
        'message': 'What size do you need?',
        'choices': ['Large', 'Medium', 'Small'],
        'filter': lambda val: val.lower()
    },
    {
        'type': 'input',
        'name': 'quantity',
        'message': 'How many do you need?',
        'validate': NumberValidator,
        'filter': lambda val: int(val)
    },
    {
        'type': 'expand',
        'name': 'toppings',
        'message': 'What about the toppings?',
        'choices': [
            {
                'key': 'p',
                'name': 'Pepperoni and cheese',
                'value': 'PepperoniCheese'
            },
            {
                'key': 'a',
                'name': 'All dressed',
                'value': 'alldressed'
            },
            {
                'key': 'w',
                'name': 'Hawaiian',
                'value': 'hawaiian'
            }
        ]
    },
    {
        'type': 'rawlist',
        'name': 'beverage',
        'message': 'You also get a free 2L beverage',
        'choices': ['Pepsi', '7up', 'Coke']
    },
    {
        'type': 'input',
        'name': 'comments',
        'message': 'Any comments on your purchase experience?',
        'default': 'Nope, all good!'
    },
    {
        'type': 'list',
        'name': 'prize',
        'message': 'For leaving a comment, you get a freebie',
        'choices': ['cake', 'fries'],
        'when': lambda answers: answers['comments'] != 'Nope, all good!'
    }
]

answers = prompt(questions, style=custom_style_3)
print('Order receipt:')
pprint(answers)






questions = [
    {
        'type': 'rawlist',
        'name': 'theme',
        'message': 'What do you want to do?',
        'choices': [
            'Order a pizza',
            'Make a reservation',
            Separator(),
            'Ask opening hours',
            'Talk to the receptionist'
        ]
    },
    {
        'type': 'rawlist',
        'name': 'size',
        'message': 'What size do you need',
        'choices': ['Jumbo', 'Large', 'Standard', 'Medium', 'Small', 'Micro'],
        'filter': lambda val: val.lower()
    }
]

answers = prompt(questions, style=custom_style_2)
print_json(answers)




questions = [
    {
        'type': 'input',
        'name': 'first_name',
        'message': 'What\'s your first name',
    }
]

answers = prompt(questions)
print_json(answers)  # use the answers as input for your app


def get_delivery_options(answers):
    options = ['bike', 'car', 'truck']
    if answers['size'] == 'jumbo':
        options.append('helicopter')
    return options


questions = [
    {
        'type': 'list',
        'name': 'theme',
        'message': 'What do you want to do?',
        'choices': [
            'Order a pizza',
            'Make a reservation',
            Separator(),
            'Ask for opening hours',
            {
                'name': 'Contact support',
                'disabled': 'Unavailable at this time'
            },
            'Talk to the receptionist'
        ]
    },
    {
        'type': 'list',
        'name': 'size',
        'message': 'What size do you need?',
        'choices': ['Jumbo', 'Large', 'Standard', 'Medium', 'Small', 'Micro'],
        'filter': lambda val: val.lower()
    },
    {
        'type': 'list',
        'name': 'delivery',
        'message': 'Which vehicle you want to use for delivery?',
        'choices': get_delivery_options,
    },
]

answers = prompt(questions, style=custom_style_2)
pprint(answers)



def get_password_options(answers):
    return {
        'type': 'password',
        'message': 'Enter your Twitter password',
        'name': 'password'
    }



questions = [
    {
        'type': 'checkbox',
        'qmark': '😃',
        'message': 'Select toppings',
        'name': 'toppings',
        'choices': [ 
            Separator('= The Meats ='),
            {
                'name': 'Ham'
            },
            {
                'name': 'Ground Meat'
            },
            {
                'name': 'Bacon'
            },
            Separator('= The Cheeses ='),
            {
                'name': 'Mozzarella',
                'checked': True
            },
            {
                'name': 'Cheddar'
            },
            {
                'name': 'Parmesan'
            }
        ],
        'validate': lambda answer: 'You must choose at least one topping.' \
            if len(answer) == 0 else True
    }
]
questions = [
    {
        'type': 'confirm',
        'message': 'Do you want to continue?',
        'name': 'continue',
        'default': True,
    },
    {
        'type': 'confirm',
        'message': 'Do you want to exit?',
        'name': 'exit',
        'default': False,
    },
]



























###
### Settings
###

settingsItems = sorted([
    [ "Profile", "profileSettings" ],
    [ "Account", "accountSettings" ],
    [ "Notification", "notificationSettings" ],
    [ "Security", "securitySettings" ],
    [ "Other", "otherSettings" ],
    [ "Sync", "sync" ]
])
settingsItems.insert(0,[ "Back", "main", "main"])

# text, path, url, price, get, country, ip, or bool
profileSettingsItems = sorted([
    [ "Cover Image", "coverImage", "path" ],
    [ "Profile Photo", "profilePhoto", "path" ],
    [ "Display Name", "displayName", "text" ],
    [ "Subscription Price", "subscriptionPrice", "price" ],
    [ "About", "about", "text" ],
    [ "Location", "location", "text" ],
    [ "Website URL", "websiteURL", "url" ]
])
profileSettingsItems.insert(0,[ "Back", "main", "main"])

accountSettingsItems = sorted([
    [ "Username", "username", "text" ],
    [ "Email", "email", "text" ],
    [ "Password", "password", "text" ]
])
accountSettingsItems.insert(0,[ "Back", "main"])

notificationSettingsItems = sorted([
    [ "Email Notifications", "emailNotifs", "bool" ],
    [ "New Referral", "emailNotifsNewReferral", "bool" ],
    [ "New Stream", "emailNotifsNewStream", "bool" ],
    [ "New Subscriber", "emailNotifsNewSubscriber", "bool" ],
    [ "New Tip", "emailNotifsNewTip", "bool" ],
    [ "Renewal", "emailNotifsRenewal", "bool" ],
    [ "New Likes Summary", "emailNotifsNewLikes", "bool" ],
    [ "New Posts Summary", "emailNotifsNewPosts", "bool" ],
    [ "New Private Message Summary", "emailNotifsNewPrivMessages", "bool" ],
    [ "Site Notifications", "siteNotifs", "bool" ],
    [ "New Comment", "siteNotifsNewComment", "bool" ],
    [ "New Favorite", "siteNotifsNewFavorite", "bool" ],
    [ "New Discounts", "siteNotifsDiscounts", "bool" ],
    [ "New Subscriber", "siteNotifsNewSubscriber", "bool" ],
    [ "New Tip", "siteNotifsNewTip", "bool" ],
    [ "Toast Notifications", "toastNotifs", "bool" ],
    [ "New Comment", "toastNotifsNewComment", "bool" ],
    [ "New Favorite", "toastNotifsNewFavorite", "bool" ],
    [ "New Subscriber", "toastNotifsNewSubscriber", "bool" ],
    [ "New Tip", "toastNotifsNewTip", "bool" ]
])
notificationSettingsItems.insert(0,[ "Back", "main"])


securitySettingsItems = sorted([
    [ "Fully Private Profile", "fullyPrivate", "bool" ],
    [ "Enable Comments", "enableComments", "bool" ],
    [ "Show Fans Count on your Profile", "showFansCount", "bool" ],
    [ "Show Posts Tips Summary", "showPostsTip", "bool" ],
    [ "Public Friends List", "publicFriendsList", "bool" ],
    [ "IP and Geo Blocking - By Country", "ipCountry", "country" ],
    [ "IP and Geo Blocking - By IP", "ipIP", "ip" ],
    [ "Watermark - Enabled", "watermark", "bool" ],
    [ "Watermark - Photos", "watermarkPhoto", "bool" ],
    [ "Watermark - Videos", "watermarkVideo", "bool" ],
    [ "Watermark - Custom Text", "watermarkText", "text" ]
])
securitySettingsItems.insert(0,[ "Back", "main"])

otherSettingsItems = sorted([
    [ "Live Server", "liveServer", "get" ],
    [ "Live Key", "liveServerKey", "get" ]
])
otherSettingsItems.insert(0,[ "Back", "main"])






































































































parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')

parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

parser.add_argument('-v', metavar="verbose", type=str, 
    help="verbosity level")

parser.add_argument('-n', '--name', dest='names', action='append', 
    help="provides names to greet")
required=True
# number of args
parser.add_argument('chars', type=str, nargs=2, metavar='c',
                    help='starting and ending character')
parser.add_argument('num', type=int, nargs='*')

# limit argument choices
parser.add_argument('--now', dest='format', choices=['std', 'iso', 'unix', 'tz'],
                    help="shows datetime in given format")

for c in ['', '-v', '-v -v', '-vv', '-vv -v', '-v -v --verbose -vvvv']:
    print(parser.parse_args(c.split()))

Namespace(verbose=0)
Namespace(verbose=1)
Namespace(verbose=2)
Namespace(verbose=2)
Namespace(verbose=3)
Namespace(verbose=7)

# Add the arguments
parser.add_argument('-b', '--balls', metavar='path', type=str, help='the path to list')
parser.add_argument('-l', '--long', action='store_true', help='enable the long listing format')
parser.add_argument('-l', '--long', action='store_true', help='enable the long listing format')


# store stores the input value to the Namespace object. (This is the default action.)
# store_const stores a constant value when the corresponding optional arguments are specified.
# store_true stores the Boolean value True when the corresponding optional argument is specified and stores a False elsewhere.
# store_false stores the Boolean value False when the corresponding optional argument is specified and stores True elsewhere.
# append stores a list, appending a value to the list each time the option is provided.
# append_const stores a list appending a constant value to the list each time the option is provided.
# count stores an int that is equal to the times the option has been provided.
# help shows a help text and exits.
# version shows the version of the program and exits.

parser = argparse.ArgumentParser()
parser.version = '1.0'
parser.add_argument('-a', action='store')
parser.add_argument('-b', action='store_const', const=42)
parser.add_argument('-c', action='store_true')
parser.add_argument('-d', action='store_false')
parser.add_argument('-e', action='append')
parser.add_argument('-f', action='append_const', const=42)
parser.add_argument('-g', action='count')
parser.add_argument('-i', action='help')
parser.add_argument('-j', action='version')

args = parser.parse_args()

my_group = parser.add_mutually_exclusive_group(required=True)

my_group.add_argument('-v', '--verbose', action='store_true')
my_group.add_argument('-s', '--silent', action='store_true')

args = parser.parse_args()
print(args.accumulate(args.integers))

 args = parser.parse_args(['--foo', 'BAR'])
>>> vars(args)
{'foo': 'BAR'}

settings = vars(args)



