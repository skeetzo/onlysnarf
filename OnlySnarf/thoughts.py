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
