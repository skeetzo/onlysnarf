#!/usr/bin/python
# 9/22/2018 - Skeetzo
# 10/10/2018: args overhaul
# 10/20/2018: usability overhaul
# 1/21/2019: upload fix & hashtagging

###### Process ################################
# download mp4 from Google Drive folder @ id  #
# login to OnlyFans                           #
# upload video to OnlyFans                    #
# publish                                     #
#   move mp4 to Google Drive folder @ id      #
# or                                          #
#   trash Google Drive mp4                    #
###############################################

########################################################################################################
##### Dependencies #####################################################################################
# pip install selenium 
########################################################################################################
import random
import os
import shutil
import datetime
import json
import sys
import pathlib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pprint import pprint
########################################################################################################
##### Globals ##########################################################################################
########################################################################################################
CONFIG_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)),'config.json')
GOOGLE_CREDS = os.path.join(os.path.dirname(os.path.realpath(__file__)),'google_creds.txt')
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
DEBUG = False
IMAGE_UPLOAD_LIMIT = 6
# selenium web browser
BROWSER = None
# backup uploaded content
BACKING_UP = True
# -v -> video
VIDEO_FILE = False
# -g -> gallery
GALLERY_FOLDER = False
# -i -> image
IMAGE_FILE = False
# Twitter hashtags
HASHTAGGING = False
########################################################################################################
##### Args #############################################################################################
########################################################################################################
i = 0
while i < len(sys.argv):
    if '-v' in str(sys.argv[i]):
        VIDEO_FILE = True
    if '-g' in str(sys.argv[i]):
        GALLERY_FOLDER = True
    if '-i' in str(sys.argv[i]):
        IMAGE_FILE = True
    if '-d' in str(sys.argv[i]):
        DEBUG = True
    if '-h' in str(sys.argv[i]):
        HASHTAGGING = True
    i += 1
print('DEBUG='+str(DEBUG))
print('BACKING_UP='+str(BACKING_UP))
# debugging
def maybePrint(text):
    if DEBUG:
        print(text);
########################################################################################################
##### Config ###########################################################################################
########################################################################################################
with open(CONFIG_FILE) as config_file:    
    config = json.load(config_file)
maybePrint('Loaded: Config')
########################################################################################################
##### Authenticate Google ##############################################################################
########################################################################################################
print('Uploading Google Drive content to OnlyFans')
print('Authenticating Google...')
try:
    # Google Drive folder ids and OnlyFans login
    OnlyFans_USERNAME = config['username']        
    OnlyFans_PASSWORD = config['password']   
    OnlyFans_VIDEOS_FOLDER = config['videos_folder']
    OnlyFans_IMAGES_FOLDER = config['images_folder']
    OnlyFans_GALLERIES_FOLDER = config['galleries_folder']
    OnlyFans_POSTED_FOLDER = config['posted_folder']
    # Google Auth
    gauth = GoogleAuth()
    # Try to load saved client credentials
    gauth.LoadCredentialsFile(os.path.join(GOOGLE_CREDS))
    maybePrint('Loaded: Google Credentials')
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile(os.path.join(GOOGLE_CREDS))
    drive = GoogleDrive(gauth)
except:
    print('...Authentication Failure!')
    print('exiting...')
    sys.stdout.flush()
    sys.exit()
print('...Authentication Success!') 
sys.stdout.flush()
########################################################################################################
##### FUNCTIONS ########################################################################################
########################################################################################################
FOLDER_NAME = None
# Downloads random video from Google Drive
def get_random_video():
    print('Downloading Random Video')
    random_folders = drive.ListFile({'q': "'"+OnlyFans_VIDEOS_FOLDER+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
    video_list = [];
    random_video = None;
    # print('random folders: '+str(random_folders))
    for folder in random_folders:
        random_folder_folder = random.choice(random_folders)
        maybePrint('random folder: '+random_folder_folder['title'])
        video_list = drive.ListFile({'q': "'"+random_folder_folder['id']+"' in parents and trashed=false and mimeType contains 'video/mp4'"}).GetList()
        # print('random folders: '+str(video_list))
        if len(video_list)==0:
            maybePrint('skipping empty folder: '+random_folder_folder['title'])
        elif len(video_list)>0:
            maybePrint('folder found: '+random_folder_folder['title'])
            global FOLDER_NAME
            FOLDER_NAME = random_folder_folder['title']
            maybePrint('folder name: '+FOLDER_NAME)
            random_video = random.choice(video_list)
            maybePrint('random video: '+random_video['title'])
            return random_video
    if len(video_list)==0:
        print('No video file found!')
        sys.stdout.flush()
        return sys.exit(0)
    random_video = random.choice(video_list)
    print('Random Video: '+random_video['title'])
    return random_video

# Downloads random image from Google Drive
def get_random_image():
    print('Downloading Random Image')
    random_folders = drive.ListFile({'q': "'"+OnlyFans_IMAGES_FOLDER+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
    images_list = [];
    random_image = None;
    for folder in random_folders:
        random_folder_folder = random.choice(random_folders)
        images_list = drive.ListFile({'q': "'"+random_folder_folder['id']+"' in parents and trashed=false and mimeType contains 'image/jpeg'"}).GetList()      
        if len(images_list)==0:
            maybePrint('skipping empty folder: '+random_folder_folder['title'])
        elif len(images_list)>0:
            # print('- folder found: '+images_list['title'])
            global FOLDER_NAME
            FOLDER_NAME = random_folder_folder['title']
            maybePrint('folder name: '+FOLDER_NAME)
            random_image = random.choice(images_list)
            maybePrint('random image: '+random_image['title'])
            return random_image
    if len(images_list)==0:
        print('No image file found!')
        sys.stdout.flush()
        return sys.exit(0)
    random_image = random.choice(images_list)
    print('Random Image: '+random_image['title'])
    return random_image

# Downloads random gallery from Google Drive
def get_random_gallery():
    print('Downloading Random Gallery')
    random_folders = drive.ListFile({'q': "'"+OnlyFans_GALLERIES_FOLDER+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
    gallery_list = [];
    random_gallery = None;
    for folder in random_folders:
        random_folder_folder = random.choice(random_folders)
        gallery_list = drive.ListFile({'q': "'"+random_folder_folder['id']+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
        if len(gallery_list)==0:
            maybePrint('- skipping empty folder: '+random_folder_folder['title'])
        elif len(gallery_list)>0:
            global FOLDER_NAME
            FOLDER_NAME = random_folder_folder['title']
            maybePrint('folder name: '+FOLDER_NAME)
            random_gallery = random.choice(gallery_list)
            maybePrint('random gallery: '+random_gallery['title'])
            return random_gallery
    if len(gallery_list)==0:
        print('No gallery folders found!')
        sys.stdout.flush()
        return sys.exit(0)
    random_gallery = random.choice(gallery_list)
    print('Random Gallery: '+random_gallery['title'])
    return random_gallery
# Downloads random video from Google Drive
def get_random_video():
    print('Downloading Random Video')
    random_folders = drive.ListFile({'q': "'"+OnlyFans_VIDEOS_FOLDER+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
    video_list = [];
    random_video = None;
    # print('random folders: '+str(random_folders))
    for folder in random_folders:
        random_folder_folder = random.choice(random_folders)
        maybePrint('random folder: '+random_folder_folder['title'])
        video_list = drive.ListFile({'q': "'"+random_folder_folder['id']+"' in parents and trashed=false and mimeType contains 'video/mp4'"}).GetList()
        # print('random folders: '+str(video_list))
        if len(video_list)==0:
            maybePrint('- skipping empty folder: '+random_folder_folder['title'])
        elif len(video_list)>0:
            maybePrint('- folder found: '+random_folder_folder['title'])
            global FOLDER_NAME
            FOLDER_NAME = random_folder_folder['title']
            random_video = random.choice(video_list)
            maybePrint('random image: '+random_video['title'])
            return random_video
    if len(video_list)==0:
        print('No video file found!')
        sys.stdout.flush()
        return sys.exit(0)
    random_video = random.choice(video_list)
    print('Random Video: '+random_video['title'])
    return random_video
# Download File
def download_file(file):
    print('Downloading Video...')
    # mkdir /tmp
    path = os.getcwd()
    path += '/tmp'
    tmp = path
    if not os.path.exists(path):
        os.mkdir(path)
    # download file
    path += "/uploadMe"+os.path.splitext(file['title'])[1]
    maybePrint('path: '+path)
    file.GetContentFile(path)
    print('Download Complete')
    return path
# Download Gallery
def download_gallery(folder):
    print('Downloading Gallery...')
    # mkdir /tmp
    path = os.getcwd()
    path += '/tmp'+"/"+str(folder['title'])
    maybePrint('path: '+path)
    if not os.path.exists(path):
        os.makedirs(path)
    # download folder
    file_list = drive.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'image/jpeg'"}).GetList()
    folder_size = len(file_list)
    maybePrint('Folder size: '+str(folder_size))
    maybePrint('Upload limit: '+str(IMAGE_UPLOAD_LIMIT))
    file_list_random = []
    for x in range(IMAGE_UPLOAD_LIMIT):
        random_file = random.choice(file_list)
        file_list.remove(random_file)
        file_list_random.append(random_file)
    i = 1
    for file in sorted(file_list_random, key = lambda x: x['title']):
        print('Downloading {} from GDrive ({}/{})'.format(file['title'], i, folder_size))
        maybePrint('filePath: '+path+"/"+str(file['title']))
        file.GetContentFile(path+"/"+str(file['title']))
        i+=1
    print('Download Complete')
    return path
# Upload to OnlyFans
def log_into_OnlyFans():
    print('Logging into OnlyFans...')
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    # options.setExperimentalOption('useAutomationExtension', false);
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    global BROWSER
    BROWSER = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)
    BROWSER.implicitly_wait(10) # seconds
    BROWSER.set_page_load_timeout(1200)
    BROWSER.get(('https://onlyfans.com'))
    # login via Twitter
    twitter = BROWSER.find_element_by_xpath('//a[@class="btn btn-default btn-block btn-lg btn-twitter"]').click()
    # fill in username
    username = BROWSER.find_element_by_xpath('//input[@id="username_or_email"]').send_keys(OnlyFans_USERNAME)
    # fill in password and hit the login button 
    password = BROWSER.find_element_by_xpath('//input[@id="password"]')
    password.send_keys(OnlyFans_PASSWORD)
    password.send_keys(Keys.ENTER)
    print('Login Success')
    return
# Uploads a file to OnlyFans
def upload_file_to_OnlyFans(fileName, path):
    fileName = os.path.splitext(fileName)[0]
    print('Uploading: '+fileName)
    maybePrint('path: '+path)
    global FOLDER_NAME
    if HASHTAGGING:
        postText = str(fileName)+" #"+" #".join(FOLDER_NAME.split(' '))
    else:
        postText = FOLDER_NAME+" "+fileName
    maybePrint('text: '+postText)
    global BROWSER
    BROWSER.find_element_by_id("new_post_text_input").send_keys(postText)
    BROWSER.find_element_by_id("fileupload_photo").send_keys(path)
    maxUploadCount = 12 # 2 hours
    i = 0
    while True:
        if i == maxUploadCount:
            print('max upload reached, breaking..')
            break
        try:
            WebDriverWait(BROWSER, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="btn btn-xs btn-default send_post_button"]')))
            if DEBUG:
                print('skipping OnlyFans upload')
                return
            send = WebDriverWait(BROWSER, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="btn btn-xs btn-default send_post_button"]'))).click()
            break
        except Exception as e:
            print('uploading...')
            i+=1
    print('File Uploaded Successfully')
    return
# Uploads a folder to OnlyFans
def upload_directory_to_OnlyFans(dirName, path):
    global FOLDER_NAME
    if HASHTAGGING:
        postText = str(dirName)+" #"+" #".join(FOLDER_NAME.split(' '))
    else:    
        postText = str(FOLDER_NAME)+" "+str(dirName)
    print('Uploading: '+postText)
    maybePrint('path: '+path)
    files_path = []
    for file in pathlib.Path(path).iterdir():  
        files_path.append(str(file))
    maybePrint('files: '+str(files_path))
    global BROWSER
    BROWSER.find_element_by_id("new_post_text_input").send_keys(postText)
    for file in files_path:
        maybePrint('uploading: '+str(file))
        BROWSER.find_element_by_id("fileupload_photo").send_keys(file)
        WebDriverWait(BROWSER, 600).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="btn btn-xs btn-default send_post_button"]')))
    if DEBUG:
        print('skipping OnlyFans upload')
        return
    send = WebDriverWait(BROWSER, 600).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="btn btn-xs btn-default send_post_button"]'))).click()
    print('Directory Uploaded Successfully')
    return
# Deletes local file
def remove_file(file):
    print('Deleting Local File(s)')
    # delete /tmp
    tmp = os.getcwd()
    tmp += '/tmp'
    shutil.rmtree(tmp)
    print('Local File(s) Removed')
    return
# Deletes online file
def delete_file(file):
    print('Trashing Google Video')
    if DEBUG:
        print('skipping Google delete')
        return
    file.Trash()
    print('Google Video Trashed')
    return
# Archives posted file
def move_file(file):
    print('Archiving Google Video')
    if DEBUG:
        print('skipping Google archive')
        return
    file['parents'] = [{"kind": "drive#fileLink", "id": OnlyFans_POSTED_FOLDER}]
    file.Upload()
    print('Google Video Archived')
    return
########################################################################################################
###### START ###########################################################################################
########################################################################################################
# FILE_NAME = None
# FILE_PATH = None
# if DEBUG_SKIP_DOWNLOAD:
    # return print('- Skipping Download -')
########################################################################################################
print('1/3 : Fetching Content')
RANDOM_FILE = None
if GALLERY_FOLDER:
    RANDOM_FILE = get_random_gallery()
    FILE_NAME = RANDOM_FILE['title']
    FILE_PATH = download_gallery(RANDOM_FILE)
elif VIDEO_FILE:
    RANDOM_FILE = get_random_video()
    FILE_NAME = RANDOM_FILE['title']
    FILE_PATH = download_file(RANDOM_FILE)
elif IMAGE_FILE:
    RANDOM_FILE = get_random_image()
    FILE_NAME = RANDOM_FILE['title']
    FILE_PATH = download_file(RANDOM_FILE)
else:
    print('Missing Args!')
    sys.stdout.flush()
    sys.exit()
if RANDOM_FILE == None:
    print('Missing Random File / Directory!')
    sys.stdout.flush()
    sys.exit()
sys.stdout.flush()
#################################################
print('2/3 : Accessing OnlyFans')
log_into_OnlyFans()
sys.stdout.flush()
if GALLERY_FOLDER:
    upload_directory_to_OnlyFans(FILE_NAME, FILE_PATH)
elif VIDEO_FILE or IMAGE_FILE:
    upload_file_to_OnlyFans(FILE_NAME, FILE_PATH)
else:
    print('Missing OnlyFans Instructions!')
    sys.stdout.flush()
    sys.exit()
print('Upload Complete')
sys.stdout.flush()
#################################################
print('3/3 : Cleaning Up Files')
remove_file(RANDOM_FILE)
if BACKING_UP:
    move_file(RANDOM_FILE)
else:
    delete_file(RANDOM_FILE)
print('Files Cleaned ')
sys.stdout.flush()
#################################################
print('Google Drive to OnlyFans Upload Complete!')
sys.stdout.flush()