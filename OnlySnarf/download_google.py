def download_random(folderName):
    remove_local()
    print("Fetching: {}".format(folderName))




    response = Google.get_random_image()

    response = Google.get_random(folderName)



    # image
    print('Fetching Image')
    response = Google.get_random_image()
    if response == None:
        print("Error: Missing Image Download")
        return
    google_file = response[0]
    folder_name = response[1]
    if google_file == None:
        return
    file_name = google_file['title']
    file_path = Google.download_file(google_file)
    # gallery
    results = Google.download_gallery(google_file)
    gallery_files = results[0]
    file_path = results[1]
    if file_path == None:
        print('Error: Missing Random Gallery')
        return

    # performer
    remove_local()
    print('Fetching Performer')
    google_file = Google.get_random_performer()
    if google_file == None:
        print("Error: Missing Performer")
        return
    performer = google_file['title']
    results = Google.download_performer(google_file)
    if results == None:
        print("Error: Missing Performer Folders")
        return
    gallery_files = results[0]
    file_path = results[1]
    gallery_name = results[2]

    # video
    repair = False
    if str(folder_name) == "gopro":
        repair = True
    file_path = Google.download_file(google_file, REPAIR=repair)

    # scene
    file_name = google_file['title']
    results = Google.download_scene(google_file)
    if results == None:
        print('Error: Empty Download')
        return
    return results

    return [file_name, file_path, google_file, folder_name] # image
    return [file_name, file_path, google_file, gallery_files, folder_name] # gallery
    return [file_path, google_file, performer, gallery_name, google_file] # performer
    return [file_name, file_path, google_file, folder_name] # video
    return results # scene




def download_random_image():
    remove_local()
    print('Fetching Image')
    response = Google.get_random_image()
    if response == None:
        print("Error: Missing Image Download")
        return
    google_file = response[0]
    folder_name = response[1]
    if google_file == None:
        return
    file_name = google_file['title']
    file_path = Google.download_file(google_file)
    if google_file == None:
        print('Error: Missing Random Image')
        return
    if file_path == None:
        print('Error: Empty Download')
        return
    return [file_name, file_path, google_file, folder_name]

def download_random_gallery():
    remove_local()
    print('Fetching Gallery')
    response = Google.get_random_gallery()
    if response == None:
        print("Error: Missing Gallery Download")
        return
    google_file = response[0]
    folder_name = response[1]
    if google_file == None:
        print("Error: Missing Google File")
        return
    file_name = google_file['title']
    results = Google.download_gallery(google_file)
    gallery_files = results[0]
    file_path = results[1]
    if file_path == None:
        print('Error: Missing Random Gallery')
        return
    return [file_name, file_path, google_file, gallery_files, folder_name]

def download_random_performer():
    remove_local()
    print('Fetching Performer')
    google_file = Google.get_random_performer()
    if google_file == None:
        print("Error: Missing Performer")
        return
    performer = google_file['title']
    results = Google.download_performer(google_file)
    if results == None:
        print("Error: Missing Performer Folders")
        return
    gallery_files = results[0]
    file_path = results[1]
    gallery_name = results[2]
    if file_path == None:
        print('Error: Missing Content')
        return
    if gallery_files == None:
        print('Error: Missing Gallery Content')
        return
    if performer == None:
        print('Error: Missing Performer Name')
        return
    if gallery_name == None:
        print('Error: Missing Gallery Name')
        return
    return [file_path, google_file, performer, gallery_name, google_file]

def download_random_video():
    remove_local()
    print('Fetching Video')
    response = Google.get_random_video()
    if response == None:
        print("Error: Missing Video Download")
        return
    google_file = response[0]
    folder_name = response[1]
    if google_file == None:
        return
    file_name = google_file['title']
    repair = False
    if str(folder_name) == "gopro":
        repair = True
    file_path = Google.download_file(google_file, REPAIR=repair)
    if google_file == None:
        print('Error: Missing Random Video')
        return
    if file_path == None:
        print('Error: Empty Download')
        return
    return [file_name, file_path, google_file, folder_name]

def download_random_scene():
    remove_local()
    print('Fetching Scene')
    response = Google.get_random_scene()
    if response == None:
        print("Error: Missing Scene Download")
        return
    google_file = response[0]
    folder_name = response[1]
    if google_file == None:
        print("Error: Missing Google File")
        return
    file_name = google_file['title']
    results = Google.download_scene(google_file)
    if results == None:
        print('Error: Empty Download')
        return
    return results