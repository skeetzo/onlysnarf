import os, shutil, random, sys
from .ffmpeg import ffmpeg
from . import google as Google
from .settings import Settings
import PyInquirer

ONE_GIGABYTE = 1000000000
ONE_MEGABYTE = 1000000
FIFTY_MEGABYTES = 50000000
ONE_HUNDRED_KILOBYTES = 100000

MIMETYPES_IMAGES = "(mimeType contains 'image/jpeg' or mimeType contains 'image/jpg' or mimeType contains 'image/png')"
MIMETYPES_VIDEOS = "(mimeType contains 'video/mp4' or mimeType contains 'video/quicktime' or mimeType contains 'video/x-ms-wmv' or mimeType contains 'video/x-flv')"
MIMETYPES_ALL = "(mimeType contains 'image/jpeg' or mimeType contains 'image/jpg' or mimeType contains 'image/png' or mimeType contains 'video/mp4' or mimeType contains 'video/quicktime')"

MIMETYPES_IMAGES_LIST = ["image/jpeg","image/jpg","image/png"]
MIMETYPES_VIDEOS_LIST = ["video/mp4","video/quicktime","video/x-ms-wmv","video/x-flv"]
MIMETYPES_ALL_LIST = []
MIMETYPES_ALL_LIST.extend(MIMETYPES_IMAGES_LIST)
MIMETYPES_ALL_LIST.extend(MIMETYPES_VIDEOS_LIST)

def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()

###############################################################

class File():
    FILES = None

    def __init__(self):
        self.path = None
        self.ext = None
        self.type = None
        ##
        self.title = None
        self.category = None # [image, gallery, video, performer]

    ######################################################################################

    # move to backup folder in GDrive
    # Google.move_file
    # Google.move_files
    def backup(self):
        if not File.backup_text(self.get_title()): return
        Google.upload_file(file=self)

    @staticmethod
    def backup_text(title):
        if Settings.is_skip_download():
            Settings.maybe_print("Warning: Skipping Backup, skipped download")
            return False
        if Settings.is_force_backup():
            Settings.maybe_print("Backing Up (forced): {}".format(title))
        elif not Settings.is_backup():
            Settings.maybe_print('Skipping Backup (disabled): {}'.format(title))
            return False
        elif Settings.is_debug():
            Settings.maybe_print("Skipping Backup (debug): {}".format(title))
            return False
        else:
            Settings.maybe_print('Backing Up: {}'.format(title))
        return True

    @staticmethod
    def backup_files(files=[]):
        for file in files:
            file.backup()
        return True

    def check_size(self):
        if not os.path.exists(self.get_path()): return False
        size = os.path.getsize(self.get_path())
        Settings.maybe_print("File Size: {}kb - {}mb".format(size/1000, size/1000000))
        global ONE_MEGABYTE
        if size <= ONE_MEGABYTE:
            Settings.maybe_print("Warning: Small File Size")
        global ONE_HUNDRED_KILOBYTES
        if size <= ONE_HUNDRED_KILOBYTES:
            Settings.maybe_print("Warning: Tiny File Size")
        if size == 0:
            Settings.maybe_print("Error: Empty File Size")
            return False
        return True

    # def combine(self):
    #     if len(self.files) == 0: return
    #     Settings.dev_print("combining files: {}".format(len(self.files)))
    #     Settings.dev_print("combine path: {}".format(combinedPath))
    #     combinedPath = os.path.join(File.get_tmp(), "{}-combined".format(self.title))
    #     for file in files:
    #         shutil.move(file.get_path(), combinedPath)
    #         file.path = "{}/{}".format(combinedPath, self.title)
    #     self.combined = ffmpeg.combine(combinedPath)

    ##############################

    # Deletes online file
    def delete(self):
        if not File.delete_text(self.get_title()): return
        try: 
            os.remove(self.get_path())
            print('File Deleted: {}'.format(self.get_title()))
        except Exception as e: Settings.dev_print(e)

    @staticmethod
    def delete_text(title):
        if Settings.is_skip_download():
            Settings.maybe_print("Warning: Skipping Delete, skipped download")
            return False
        if not Settings.is_delete():
            Settings.maybe_print('Skipping Delete (disabled): {}'.format(title))
            return False
        elif Settings.is_debug():
            Settings.maybe_print("Skipping Delete (debug): {}".format(title))
            return False
        else:
            Settings.maybe_print('Deleting: {}'.format(title))
        return True

    ##############################

    def get_ext(self):
        if self.ext: return self.ext
        self.get_title()

    def get_path(self):
        if not self.path:
            Settings.maybe_print("Error: Missing File Path")
            return  ""
        return self.path

    def get_title(self):
        if str(self.title) != "": return self.title
        path = self.get_path()
        if str(path) == "": 
            Settings.maybe_print("Error: Missing File Title")
            return ""
        title, ext = os.path.splitext(path)
        self.ext = ext
        self.title = title
        return self.title

    # def get_type(self):
    #     if str(self.type) != "": return self.type
    #     if (self.get_ext()) in MIMETYPES_IMAGES_LIST:
    #         self.type = Image()
    #     elif (self.get_ext()) in MIMETYPES_VIDEOS_LIST:
    #         self.type = Video()
    #     setattr(self.type, "path", self.get_path())
    #     return self.type

    @staticmethod
    def get_tmp():
        tmp = os.getcwd()
        if Settings.get_mount_path() != "":
            tmp = os.path.join(Settings.get_mount_path(), "tmp")
        else:
            tmp = os.path.join(tmp, "tmp")
        if not os.path.exists(str(tmp)):
            os.mkdir(str(tmp))
        return tmp

    def get_type(self):
        if self.type: return self.type
        if str(self.get_ext()) in str(MIMETYPES_VIDEOS_LIST):
            self.type = Video()
        elif str(self.get_ext()) in str(MIMETYPES_IMAGES_LIST):
            self.type = Image()
        else: print("Warning: Unable to Parse File Type")
        return self.type

    # files are File references
    # file references can be GoogleId references which need to download their source
    # files exist when checked for size
    def prepare(self):
        self.get_type().prepare()
        if not self.check_size():
            return False
        return True

    # Deletes all local files
    @staticmethod
    def remove_local():
        try:
            # if str(Settings.SKIP_DELETE) == "True":
                # Settings.maybe_print("Skipping Local Remove")
                # return
            # print('Deleting Local File(s)')
            # delete /tmp
            tmp = File.get_tmp()
            if os.path.exists(tmp):
                shutil.rmtree(tmp)
                print('Local File(s) Removed')
            else:
                print('Local Files Not Found')
        except Exception as e:
            Settings.dev_print(e)

    @staticmethod
    def select_file():
        # if not Settings.prompt("file path"): return None
        question = {
            'type': 'input',
            'name': 'path',
            'message': 'File Path:',
        }
        answer = PyInquirer.prompt(question)
        path = answer["path"]
        if not Settings.confirm(path): return None
        if not os.path.exists(path):
            print("Error: File Does Not Exist")
            return True
        file = File()
        setattr(file, "path", path)
        return file

    @staticmethod
    def select_files():
        if not Settings.prompt("enter files"): return []
        print("Enter File Paths")
        files = []
        while True:
            file = File.select_file()
            if not file: break
            if isinstance(file, File): files.append(file)
            if not Settings.prompt("another file"): break
        if not Settings.confirm([file.get_path() for file in files]): return []
        return files

    @staticmethod
    def select_file_upload_method():
        if not Settings.prompt("upload files"): return []
        print("Select an upload source")
        question = {
            'type': 'list',
            'name': 'upload',
            'message': 'Upload:',
            'choices': ["Local", "Google"]
        }
        upload = PyInquirer.prompt(question)["upload"]
        if not Settings.confirm(upload): return File.select_file_upload_method()
        if str(upload) == "Google":
            return Google_File.select_files()
        return File.select_files()

    def upload(self):
        if not self.prepare():  
            print("Error: Unable to Upload File - {}".format(self.get_title()))
            return False
        self.backup()
        self.delete()
        return True

###################################################################################

class Google_File(File):

    def __init__(self):
        File.__init__(self)
        self.id = None
        self.title = None
        self.file = None
        self.parent = None
        self.mimeType = None

    def backup(self):
        if not File.backup_text(self.get_title()): return
        Google.backup_file(self)

    def delete(self):
        if not File.delete_text(self.get_title()): return
        Google.delete(self)

    @staticmethod
    def download_text(title):
        if Settings.is_skip_download():
            print("Skipping Download (debug)")
            return False
        return True

    @staticmethod
    def download_files(files=[]):
        Settings.maybe_print('Download limit: '+str(Settings.get_image_download_limit()))
        random.shuffle(files)
        files = files[:int(Settings.get_image_download_limit())]
        print('Downloading Files: {}'.format(len(files)))
        i = 1
        for file in sorted(files, key = lambda x: x['title']):
            print('Downloading: {}/{}'.format(i, Settings.get_image_download_limit()))
            file.download()
        print("Downloaded: {}".format(len(files)))

    # Download File
    def download(self):
        if not Google_File.download_text(self.title): return False
        successful = Google.download_file(self)
        if not successful: return False
        ### Finish ###
        if not self.check_size():
            print("Error: Missing Downloaded File")
            return False
        print("Downloaded: {}".format(self.title))
        return True

    def get_ext(self):
        if self.ext: return self.ext
        title, ext = os.path.splitext(self.get_file()["title"])
        if str(ext) == "":
            ext = self.get_file()["mimeType"]
            mime, ext = str(ext).split("/")
            ext = "."+str(ext)
        self.ext = ext
        self.title = title
        return self.ext

    def get_id(self):
        if self.id: return self.id
        if self.file: self.id = self.file["id"]
        return self.id

    def get_file(self):
        if self.file: return self.file
        self.file = Google.get_file(self.get_id())
        # if not self.check_size(): self.download()
        return self.file

    @staticmethod
    def get_files():
        if File.FILES: return File.FILES
        category = Settings.get_category()
        if not category: category = Settings.select_category()
        if not category: Settings.dev_print("Warning: Missing Category")
        files = Google_File.get_files_by_category(category)
        if Settings.get_title():
            for file in files:
                if str(Settings.get_title()) == str(file.get_title()):
                    files = [file]
                    break
        File.FILES = files
        return files

    @staticmethod
    def get_files_by_category(cat, performer=None):
        Settings.maybe_print("Loading Google Files...")
        files = []
        ##
        def parse_categories(category, categoryFolder=None):
            files = []
            # return Google_File.get_files_by_category(cat)
            if "image" in str(category):
                if not categoryFolder:
                    categoryFolder = Google.get_folder_by_name(category)
                for folder in Google.get_folders_of_folder_by_keywords(categoryFolder):
                    for image in Google.get_images_of_folder(folder):
                        file = Google_File()
                        setattr(file, "file", image)
                        setattr(file, "parent", folder)
                        files.append(file)
            elif "video" in str(category):
                if not categoryFolder:
                    categoryFolder = Google.get_folder_by_name(category)
                for folder in Google.get_folders_of_folder_by_keywords(categoryFolder):
                    for video in Google.get_videos_of_folder(folder):
                        file = Google_File()
                        setattr(file, "file", video)
                        setattr(file, "parent", folder)
                        files.append(file)
            elif "galler" in str(category):
                if not categoryFolder:
                    categoryFolder = Google.get_folder_by_name(category)
                for folder in Google.get_folders_of_folder_by_keywords(categoryFolder):
                    for gallery in Google.get_folders_of_folder(folder):
                        file = Google_Folder()
                        setattr(file, "file", gallery)
                        setattr(file, "parent", folder)
                        files.append(file)
            elif "performer" in str(category):
                if not categoryFolder:
                    categoryFolder = Google.get_folder_by_name(category)
                for performer in Google.get_folders_of_folder_by_keywords(categoryFolder):
                    # for performer in Google.get_folders_of_folder(folder):
                    p = Google_Folder()
                    setattr(p, "file", performer)
                    setattr(p, "parent", categoryFolder)
                    files.append(p)
            return files
        ##
        if performer:
            categoryFolder = Google.get_folder_by_name("performers")
            for performerFolder in Google.get_folders_of_folder_by_keywords(categoryFolder):
                if str(performer) == str(performerFolder['title']):
                    return parse_categories(cat, categoryFolder=performerFolder)
        return parse_categories(cat)

    @staticmethod
    def get_random_file():
        return random.choice(Google_File.get_files())

    def get_mimetype(self):
        if self.mimeType: return self.mimeType
        self.mimeType = self.get_file()["mimeType"]
        return self.mimeType

    def get_parent(self):
        if self.parent: return self.parent 
        self.parent = Google.get_file_parent(self.get_id())
        return self.parent

    def get_path(self):
        if self.path: return self.path
        # downloads to /tmp/downloads or whatever
        # if exists, adds 1 to end of name
        tmp = File.get_tmp()
        def counterfy():
            filename_ = str(self.get_title())+"{}"+str(self.get_ext())
            counter = 0
            while os.path.isfile(os.path.join(tmp, filename_.format(counter))):
                counter += 1
            filename_ = filename_.format(counter)
            Settings.maybe_print("filename: {}".format(filename_))
            filename_ = os.path.join(tmp, filename_.format(counter))
            return filename_
        filename = os.path.join(tmp, "{}{}".format(self.get_title(), self.get_ext()))
        if os.path.isfile(filename) and not Settings.is_prefer_local():
            filename = counterfy()
        # tmp = File.get_tmp() # i don't think this should be in file over settings
        filename = filename.strip('\'').strip('\"').strip()
        self.path = filename
        Settings.dev_print(self.path)
        return self.path

    def get_title(self):
        ## title would be set when created
        if self.title: return self.title
        title, ext = os.path.splitext(self.get_file()["title"])
        self.ext = ext
        self.title = title.replace(" ","_")
        return self.title

    # files are File references
    # file references can be GoogleId references which need to download their source
    # files exist when checked for size
    def prepare(self):
        if not self.check_size():
            self.download()
        return super()

    @staticmethod
    def select_file(category, performer=None):
        if not Settings.is_prompt(): return Google_File.get_random_file()
        # this is a list of google files to select from
        files = Google_File.get_files_by_category(category, performer=performer)
        files_ = []
        for file in files:
            file.category = category
            file_ = {
                "name": file.file['title'],
                "value": file,
                "short": file.file['id']
            }
            files_.append(file_)
        if len(files_) == 0:
            print("Missing Files")
            return Google_File.select_files()
        question = {
            'type': 'list',
            'name': 'file',
            'message': 'Google Files:',
            'choices': files_,
            # 'filter': lambda file: file.lower()
        }
        file = PyInquirer.prompt(question)["file"]
        if not Settings.confirm(file.get_title()): return Google_File.select_file(category)
        return file

    @staticmethod
    def select_files():
        if not Settings.is_prompt(): return [Google_File.get_random_file()]
        print("Select a folder category")
        question = {
            'type': 'list',
            'name': 'category',
            'message': 'Categories:',
            'choices': Settings.get_categories(),
            'filter': lambda cat: cat.lower()
        }
        answer = PyInquirer.prompt(question)
        category = answer["category"]
        if not Settings.confirm(category): return Google_File.select_files()
        print("Select Google Files or a Folder")
        files = []
        while True:
            file = Google_File.select_file(category)
            if not file: break
            ##
            if "performer" in str(category):
                cat = Settings.select_category([cat for cat in Settings.get_categories() if "performer" not in cat])
                file = Google_File.select_file(cat, performer=file.get_title())
                if not file: break
                files.append(file)
                if "galler" in str(cat) or "video" in str(cat): break
            ##
            files.append(file)
            if "galler" in str(category) or "video" in str(category): break
        if not Settings.confirm([file.file['title'] for file in files]): return Google_File.select_files()
        return files

##########################################################################################

class Google_Folder(Google_File):
    def __init__(self):
        Google_File.__init__(self)
        self.files = None

    def backup(self):
        if File.backup_text(self.get_title()): return
        Google.upload_gallery(files=self.files)

    def check_size(self):
        for file in self.get_files():
            exists = file.check_size()
            if not exists: return False
        return True

    def download(self):
        print("Downloading Folder: {}".format(self.get_title()))
        if len(self.files) == 0:
            file_list = Google.get_files_by_folder_id(self.get_id())
            self.files = []
            for file in file_list:
                file_ = Google_File()
                setattr(file_, "id", file["id"])
                setattr(file_, "file", file)
                self.files.append(file_)
        folder_size = len(self.files)
        Settings.maybe_print('Folder size: {}'.format(folder_size))
        Settings.maybe_print('Upload limit: {}'.format(Settings.get_upload_max()))
        if int(folder_size) == 0:
            print('Error: Empty Folder')
            return False
        file_list = self.files
        random.shuffle(file_list)
        file_list = file_list[:int(Settings.get_upload_max())]
        ## video preference
        videos = []
        for file in file_list:
            if str(file.get_mimetype()) in MIMETYPES_VIDEOS_LIST:
                videos.append(file)
        if len(videos) > 0: file_list = [random.choice(videos)]
        ##
        i = 1
        for file in sorted(file_list, key = lambda x: x.get_title()):
            # print_same_line("Downloading: {} ({}/{})".format(file.get_title(), i, folder_size))
            print("Downloading: {} ({}/{})".format(file.get_title(), i, folder_size))
            file.download()
            i+=1
        print()
        print("Downloaded Folder: {}".format(self.get_title()))

    def get_files(self):
        if not self.files:
            self.files = []
            files = Google.get_files_by_folder_id(self.get_id())
            for file in files:
                file_ = Google_File()
                setattr(file_, "file", file)
                self.files.append(file_)
        if Settings.get_title():
            for file in self.files:
                if str(Settings.get_title()) == str(file.get_title()):
                    self.files = [file]
                    break
        return self.files

###################################################################################

class Image(File):
    def __init__(self):
        pass

    def prepare(self):
        pass

###################################################################################

class Video(File):
    def __init__(self):
        self.screenshots = []
        self.trimmed = ""
        self.split = ""

    #seconds off front or back
    def trim(self):
        path = self.get_path()
        self.trimmed = ffmpeg.trim(path) 

    # into segments (60 sec, 5 min, 10 min)
    def split(self):
        path = self.get_path()
        self.split = ffmpeg.split(path)

    # unnecessary, handled by onlyfans
    # unless this somehow adds like more metadata
    def watermark(self):
        pass

    # cleanup & label appropriately (digital watermarking?)
    def get_metadata(self):
        pass

    # frames for preview gallery
    def get_frames(self):
        path = self.get_path()
        self.screenshots = ffmpeg.frames(path)

    def prepare(self):
        self.reduce()
        self.repair()
        self.watermark()

    def reduce(self):
        if not Settings.is_reduce(): 
            Settings.maybe_print("Skipping: Video Reduction")
            return
        path = self.get_path()
        global FIFTY_MEGABYTES
        if (int(os.stat(str(path)).st_size) < FIFTY_MEGABYTES or str(Settings.is_reduce()) == "False"):
            return
        Settings.dev_print("reduce: {}".format(self.title))
        self.path = ffmpeg.reduce(path)
    
    # unnecessary
    def repair(self):
        if not Settings.is_repair():
            Settings.dev_print("Skipping: Video Repair")
            return
        path = self.get_path()
        if Settings.is_repair():
            return
        Settings.dev_print("repair: {}".format(self.title))
        self.path = ffmpeg.repair(path)

