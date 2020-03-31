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
        if not File.backup_text(self.title): return
        Google.upload_file(file=self)
        print('File Backed Up: {}'.format(self.title))

    @staticmethod
    def backup_text(title):
        if Settings.is_skip_download():
            print("Warning: Unable to Backup, skipped download")
            return False
        if Settings.is_debug():
            print("Skipping Backup (debug): {}".format(title))
            return False
        elif not Settings.is_backup():
            print('Skipping Backup (disabled): {}'.format(title))
            return False
        else:
            print('Backing Up (file): {}'.format(title))
        return True

    @staticmethod
    def backup_files(files=[]):
        if Settings.is_skip_download():
            print("Warning: Unable to Backup, skipped download")
            return
        if Settings.is_debug():
            print("Skipping Backup (debug): {}".format(len(files)))
            return
        elif not Settings.is_backup():
            print('Skipping Backup (disabled): {}'.format(len(files)))
            return
        else:
            print('Backing Up (files): {}'.format(len(files)))
        for file in files:
            file.backup()
        print('Files Backed Up: {}'.format(len(files)))

    def check_size(self):
        if not os.path.exists(self.get_path()): return False
        size = os.path.getsize(self.get_path())
        Settings.maybe_print("File Size: {}kb - {}mb".format(size/1000, size/1000000))
        global ONE_MEGABYTE
        if size <= ONE_MEGABYTE:
            Settings.maybe_print("Warning: Small File Size")
        global ONE_HUNDRED_KILOBYTES
        if size <= ONE_HUNDRED_KILOBYTES:
            Settings.maybe_print("Error: File Size Too Small")
            print("Error: Download Failure")
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
        if not File.delete_text(self.title): return
        try: os.remove(self.get_path())
        except Exception as e: Settings.dev_print(e)

    @staticmethod
    def delete_text(title):
        if Settings.is_skip_download():
            print("Warning: Unable to Delete, skipped download")
            return False
        if Settings.is_debug():
            print("Skipping Delete (Debug): {}".format(title))
            return False
        else:
            print('Deleting: {}'.format(title))
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

    # files are File references
    # file references can be GoogleId references which need to download their source
    # files exist when checked for size
    def prepare(self):
        if not self.check_size():
            return False
        return True

    def set_path(self, path):
        # check if path exists
        if not os.path.exists(path):
            print("Error: File Does Not Exist")
            return False
        self.path = path

    # upload to GDrive
    # Google.upload_input
    def upload(self):
        # basically handled by backup process
        pass

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
            Settings.maybe_print(e)

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
        file = File()
        file.set_path(path)
        return file

    @staticmethod
    def select_files():
        if not Settings.prompt("enter files"): return []
        print("Enter File Paths")
        files = []
        while True:
            file = File.select_file()
            if not file: break
            files.append(file)
            if not Settings.prompt("another file"): break
        if not Settings.confirm([file.get_path() for file in files]): return []
        return files

###################################################################################

class Google_File(File):

    def __init__(self):
        File.__init__(self)
        self.id = None
        self.title = None
        self.file = None
        self.parent = None
        self.mimeType = None

    def backup(self, arg):
        if self.backup_text(): return
        Google.backup_file(self)

    def delete(self, arg):
        if not self.delete_text(): return
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
        if not os.path.isfile(str(self.get_path())):
            print("Error: Missing Downloaded File")
            return False
        self.check_size()
        print("Downloaded: {}".format(self.title))
        return True

    def get_ext(self):
        if self.ext: return self.ext
        title, ext = os.path.splitext(self.get_file()["title"])
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
        return self.file

    @staticmethod
    def get_files():
        if Settings.get_category() == "":
            print("Warning: Missing Category")
            return []
        files = Google.get_files_by_category(Settings.get_category())
        if Settings.get_title():
            for file in files:
                if str(Settings.get_title()) == str(file.get_title()):
                    return [file]
        return files

    @staticmethod
    def get_random_files():
        files = Google_File.get_files()
        return [random.choice(files)]

    def get_mimetype(self):
        if self.mimeType: return self.mimeType
        mimeType = self.get_file()["mimeType"]
        return self.mimeType

    def get_parent(self):
        if self.parent: return self.parent 
        try: 
            if self.id == "": 
                self.parent = get_folder_by_name("posted")
                self.id = self.parent["id"]
            else: 
                self.parent = Google.get_file_parent(self.get_id())
        except Exception as e: Settings.dev_print(e)
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
            Settings.dev_print("filename: {}".format(filename_))
            return filename_
        filename = os.path.join(tmp, "{}{}".format(self.get_title(), self.get_ext()))
        if os.path.isfile(filename):
            filename = counterfy()
        # tmp = File.get_tmp() # i don't think this should be in file over settings
        filename = filename.strip('\'').strip('\"').strip()
        self.path = filename

    def get_title(self):
        ## title would be set when created
        if self.title: return self.title
        title, ext = os.path.splitext(self.get_file()["title"])
        self.ext = ext
        self.title = title
        return self.title

    # files are File references
    # file references can be GoogleId references which need to download their source
    # files exist when checked for size
    def prepare(self):
        if not self.check_size():
            self.download()
        return super()

    @staticmethod
    def select_file(category):
        if not Settings.prompt("google file"): return random.choice(Google_File.get_random_files())
        # this is a list of google files to select from
        files = Google.get_files_by_category(category)
        for file in files:
            file["name"] = file["title"]
            file["value"] = file
            file["short"] = file["id"]
        question = {
            'type': 'list',
            'name': 'file',
            'message': 'Google Files:',
            'choices': files,
            # 'filter': lambda file: file.lower()
        }
        answer = PyInquirer.prompt(question)
        file = answer["file"]
        if not Settings.confirm(file): return Google_File.select_file(category)
        file_ = Google_File()
        setattr(file_, "file", file)
        return file

    @staticmethod
    def select_files():
        if not Settings.prompt("select google files"): return Google_File.get_random_files()
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
            files.append(file)
        if not Settings.confirm(files): return Google_File.select_files()
        return files

##########################################################################################

class Google_Folder(Google_File):
    def __init__(self):
        Google_File.__init__(self)
        self.files = []
        self.id = None
        self.title = None
        self.path = None
        self.parent = None

    def backup(self):
        if File.backup_text(self.title): return
        Google.upload_gallery(files=self.files)

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
        i = 1
        for file in sorted(file_list, key = lambda x: x.get_title()):
            # print_same_line("Downloading: {} ({}/{})".format(file.get_title(), i, folder_size))
            print("Downloading: {} ({}/{})".format(file.get_title(), i, folder_size))
            file.download()
            i+=1
        print()
        print("Downloaded: {}".format(self.get_title()))

###################################################################################

class Image(File):
    def __init__(self):
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
    def watermark(self):
        pass

    # cleanup & label appropriately (digital watermarking?)
    def get_metadata(self):
        pass

    # frames for preview gallery
    def get_frames(self):
        path = self.get_path()
        self.screenshots = ffmpeg.frames(path)

    def reduce(self):
        path = self.get_path()
        global FIFTY_MEGABYTES
        if (int(os.stat(str(path)).st_size) < FIFTY_MEGABYTES or str(Settings.is_reduce()) == "False"):
            return
        Settings.dev_print("reduce: {}".format(self.title))
        self.path = ffmpeg.reduce(path)
    
    # def repair(self):
    #     path = self.get_path()
    #     if Settings.is_repair():
    #         return
    #     Settings.dev_print("repair: {}".format(self.title))
    #     self.path = ffmpeg.repair(path)

