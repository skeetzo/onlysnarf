
# Downloads random image from Google Drive
def get_random_image():
    checkAuth()
    print('Getting Random Image')
    global PYDRIVE
    random_folders = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'".format(get_folder_by_name("images")['id'])}).GetList()
    images_list = []
    random_image = None
    folder_name = None
    for folder in random_folders:
        if str(settings.VERBOSE) == "True":
            print('checking folder: '+folder['title'],end="")
        images_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and (mimeType contains \'image/jpeg\' or mimeType contains \'image/jpg\' or mimeType contains \'image/png\')"}).GetList()      
        if len(images_list_tmp)>0:
            images_list.append(folder)
            settings.maybePrint(" -> added")
        else:
            settings.maybePrint(" -> empty")
    if len(images_list)==0:
        print('Error: Missing Image File')
        return
    random_image = random.choice(images_list)
    folder_name = random_image['title'];
    print('Random Folder: '+random_image['title'])
    random_image = PYDRIVE.ListFile({'q': "'"+random_image['id']+"' in parents and trashed=false and (mimeType contains \'image/jpeg\' or mimeType contains \'image/jpg\' or mimeType contains \'image/png\')"}).GetList()
    random_image = random.choice(random_image)
    print('Random Image: '+random_image['title'])
    return [random_image, folder_name]

def get_files_of_folder(folderName):
    checkAuth()
    print('Getting: {}'.format(folderName))
    global PYDRIVE
    folders = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'".format(get_folder_by_name(folderName)['id'])}).GetList()
    files = []
    for folder in folders:
        file_list = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and (mimeType contains \'image/jpeg\' or mimeType contains \'image/jpg\' or mimeType contains \'image/png\' or mimeType contains \'video/mp4\')"}).GetList()      
        for file in file_list:
            files.append(image)
    settings.maybePrint("Files Found: {}".format(len(files)))
    return files

def get_folders_of_folder(folderName):
    checkAuth()
    print('Getting: {}'.format(folderName))
    global PYDRIVE
    folders = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'".format(get_folder_by_name(folderName)['id'])}).GetList()
    files = []
    for folder in folders:
        file_list = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and (mimeType contains \'image/jpeg\' or mimeType contains \'image/jpg\' or mimeType contains \'image/png\' or mimeType contains \'video/mp4\')"}).GetList()      
        for file in file_list:
            files.append(image)
    settings.maybePrint("Files Found: {}".format(len(files)))
    return files

def get_random(folderName):
    files_list = get_files_of_folder(folderName)
    if len(files_list) == 0:
        files_list = get_folders_of_folder(folderName)
    rando = random.choice(files_list)
    return rando


# Downloads random gallery from Google Drive
def get_random_gallery():
    checkAuth()
    print('Getting Random Gallery')
    global PYDRIVE
    random_folders = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'".format(get_folder_by_name("galleries")['id'])}).GetList()
    folder_list = []
    random_gallery = None
    folder_name = None
    for folder in random_folders:
        if str(settings.VERBOSE) == "True":
            print('checking galleries: {}'.format(folder['title']),end="")
        gallery_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
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
        gallery_list_tmp_tmp = PYDRIVE.ListFile({'q': "'"+random_gallery_tmp['id']+"' in parents and trashed=false and (mimeType contains \'image/jpeg\' or mimeType contains \'image/jpg\' or mimeType contains \'image/png\')"}).GetList()
        if len(gallery_list_tmp_tmp)>0:
            folder_name = folder['title']
            random_gallery = random_gallery_tmp
            settings.maybePrint(" -> found")
        else:
            settings.maybePrint(" -> empty")
    if not random_gallery:
        print('Error: Missing Gallery Folder')
        return
    print('Random Gallery: '+random_gallery['title'])
    return [random_gallery, folder_name]

# Downloads random performer from Google Drive
def get_random_performer():
    checkAuth()
    print('Getting Random Performer')
    global PYDRIVE
    random_folders = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'".format(get_folder_by_name("performers")['id'])}).GetList()
    performer_list = []
    random_performer = None
    # print('random folders: '+str(random_folders))
    for folder in random_folders:
        random_folder_folder = random.choice(random_folders)
        settings.maybePrint('random performer: '+random_folder_folder['title'])
        performer_content_list = PYDRIVE.ListFile({'q': "'"+random_folder_folder['id']+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
        # print('random folders: '+str(performer_list))
        if len(performer_content_list)==0:
            settings.maybePrint('- skipping empty performer: '+random_folder_folder['title'])
        elif len(performer_content_list)>0:
            settings.maybePrint('- performer found: '+random_folder_folder['title'])
            performer_list.append(random_folder_folder)
    if len(performer_list)==0:
        print('Error: Missing Performer Folder')
        return
    random_performer = random.choice(performer_list)
    print('Random Performer: '+random_performer['title'])
    return random_performer

# Downloads random video from Google Drive
def get_random_video():
    checkAuth()
    print('Getting Random Video')
    global PYDRIVE
    random_folders = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'".format(get_folder_by_name("videos")['id'])}).GetList()
    video_list = []
    random_video = None
    folder_name = None
    for folder in random_folders:
        if str(settings.VERBOSE) == "True":
            print('checking folder: '+folder['title'],end="")
        video_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'video/mp4'"}).GetList()
        if len(video_list_tmp)>0:
            video_list.append(folder)
            settings.maybePrint(" -> added")
        else:
            settings.maybePrint(" -> empty")
    if len(video_list)==0:
        print('Error: Missing Video File')
        return
    random_video = random.choice(video_list)
    folder_name = random_video['title'];
    print('Random Folder: '+random_video['title'])
    random_video = PYDRIVE.ListFile({'q': "'"+random_video['id']+"' in parents and trashed=false and mimeType contains 'video/mp4'"}).GetList()
    random_video = random.choice(random_video)
    print('Random Video: '+random_video['title'])
    return [random_video, folder_name]

# Downloads random scene from Google Drive
def get_random_scene():
    checkAuth()
    print('Getting Random Scene')
    global PYDRIVE
    random_folders = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'".format(get_folder_by_name("scenes")['id'])}).GetList()
    folder_list = []
    random_scene = None
    folder_name = None
    for folder in random_folders:
        if str(settings.VERBOSE) == "True":
            print('checking scenes: '+folder['title'],end="")
        scene_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
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
        return
    print('Random Scene: '+random_scene['title'])
    return [random_scene, folder_name]
