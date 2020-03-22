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
