import os, shutil, random, sys
import PyInquirer
from PIL import Image
from os import walk
##
from ..lib import remote as Remote
from ..lib.ffmpeg import ffmpeg
from ..util.settings import Settings

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

###############################################################

class File():
    """File class"""

    FILES = None

    def __init__(self):
        """File object represents local image/video file"""

        # the path to the file locally
        self.path = None
        # the file extension
        self.ext = None
        # image|video
        self.type = None
        ##
        # file title reference
        self.title = None
        # [image, gallery, video, performer]
        self.category = None
        # file size
        self.size = None

    ######################################################################################

    def backup(self):
        """Backup file to appropriate destination source"""

        if not File.backup_text(self.get_title()): return
        if Settings.get_destination() == "remote":
            Remote.upload_file(self)
        else:
            # move file to local backup location
            backupPath = os.path.join(Settings.get_local_path(), "posted")
            backupPath = os.path.join(backupPath, self.category, self.get_title())
            shutil.move(self.get_path(), backupPath)

    @staticmethod
    def backup_text(title):
        """
        Print applicable backup text

        Returns
        -------
        bool
            Whether or not the file should be backed up

        """

        if Settings.is_skip_download():
            Settings.warn_print("skipping backup, skipped download")
            return False
        if Settings.is_force_backup():
            Settings.maybe_print("backing up (forced): {}".format(title))
        elif not Settings.is_backup():
            Settings.maybe_print("skipping backup (disabled): {}".format(title))
            return False
        elif Settings.is_debug():
            Settings.maybe_print("skipping backup (debug): {}".format(title))
            return False
        else:
            Settings.maybe_print("backing up: {}".format(title))
        return True

    @staticmethod
    def backup_files(files=[]):
        """
        Backup files provided to appropriate destinations

        Returns
        -------
        bool
            Whether or not the files were backed up successfully

        """

        if not File.backup_text(self.get_title()): return
        if Settings.get_destination() == "remote":
            Remote.upload_files(files)
        else:
            for file in files:
                file.backup()
        return True

    def check_size(self):
        """
        Check file size.

        Returns
        -------
        bool
            Whether or not the file exists by checking size

        """

        if not self.size:
            if not os.path.exists(self.get_path()): return False
            size = os.path.getsize(self.get_path())
        else: size = self.size
        Settings.maybe_print("file size: {}kb - {}mb".format(size/1000, size/1000000))
        global ONE_MEGABYTE
        if size <= ONE_MEGABYTE:
            Settings.warn_print("small file size")
        global ONE_HUNDRED_KILOBYTES
        if size <= ONE_HUNDRED_KILOBYTES:
            Settings.warn_print("tiny file size")
        self.size = size
        if size == 0:
            Settings.err_print("empty file size")
            return False
        return True

    def delete(self):
        """Delete file"""

        if not File.delete_text(self.get_title()): return
        try: 
            os.remove(self.get_path())
            Settings.print('File Deleted: {}'.format(self.get_title()))
        except Exception as e: Settings.dev_print(e)

    @staticmethod
    def delete_text(title):
        """
        Print applicable deletion text
        
        Returns
        -------
        bool
            Whether or not the file should be deleted

        """

        if Settings.is_skip_download():
            Settings.warn_print("skipping delete, skipped download")
            return False
        if not Settings.is_delete():
            Settings.maybe_print("skipping delete (disabled): {}".format(title))
            return False
        elif Settings.is_debug():
            Settings.maybe_print("skipping delete (debug): {}".format(title))
            return False
        else:
            Settings.maybe_print("deleting: {}".format(title))
        return True

    @staticmethod
    def download_text(title):
        """
        Print applicable download text.
        
        Returns
        -------
        bool
            Whether or not the file should be downloaded

        """

        if Settings.is_skip_download():
            Settings.print("Skipping Download (debug)")
            return False
        return True

    ##############################

    def get_ext(self):
        """Get the file's extension"""

        if self.ext: return self.ext
        self.get_title()
        return self.ext

    def get_path(self):
        """
        Get the file's path
        
        Returns
        -------
        str
            The file path

        """

        if not self.path:
            Settings.err_print("missing file path")
            return  ""
        return str(self.path)

    def get_title(self):
        """
        Get the file's title from it's filename
        
        Returns
        -------
        str
            The file's title or filename without extension

        """

        if self.title: return self.title
        path = self.get_path()
        if str(path) == "": 
            Settings.err_print("missing file title")
            return ""
        title, ext = os.path.splitext(path)
        self.ext = ext.replace(".","")
        self.title = "{}{}".format(os.path.basename(title), ext)
        return self.title

    @staticmethod
    def get_tmp():
        """Creates / gets the default temporary download directory"""

        # tmp = os.getcwd()
        # if Settings.get_download_path() != "":
        #     tmp = os.path.join(Settings.get_download_path(), "tmp")
        # else:
        #     tmp = os.path.join(tmp, "tmp")
        # if not os.path.exists(str(tmp)):
        #     os.mkdir(str(tmp))
        # return tmp
        download_path = Settings.get_download_path()
        if not os.path.exists(str(download_path)):
            os.mkdir(str(download_path))
        return download_path

    def get_type(self):
        """
        Gets the file's type as an inner class of either Image or Video
        
        Returns
        -------
        Image|Video
            The file's type as an image or video class

        """

        if self.type: return self.type
        if str(self.get_ext()) in str(MIMETYPES_VIDEOS_LIST):
            self.type = Video()
        elif str(self.get_ext()) in str(MIMETYPES_IMAGES_LIST):
            self.type = Image()
        else: Settings.warn_print("unable to parse file type")
        return self.type

    def prepare(self):
        """
        Prepares the file for uploading.

        Runs the apppropriate file type method and downloads the file locally if necessary.

        Returns
        -------
        bool
            Whether or not the file is prepared

        """

        Settings.maybe_print("preparing: {}".format(self.get_title()))
        # self.get_type().prepare()
        if not self.check_size():
            return False
        return True

    @staticmethod
    def remove_local():
        """
        Delete all local files.

        """

        try:
            # if str(Settings.SKIP_DELETE) == "True":
                # Settings.maybe_print("skipping local remove")
                # return
            # Settings.print('Deleting Local File(s)')
            # delete /tmp
            tmp = File.get_tmp()
            if os.path.exists(tmp):
                shutil.rmtree(tmp)
                Settings.print('Local File(s) Removed')
            else:
                Settings.print('Local Files Not Found')
        except Exception as e:
            Settings.dev_print(e)

    @staticmethod
    def get_files():
        """
        Get files from the runtime category folder.

        Returns
        -------
        list
            The files retrieved

        """

        if File.FILES: return File.FILES
        category = Settings.get_category()
        if not category: category = Settings.select_category()
        if not category: Settings.warn_print("missing category")
        files = File.get_files_by_category(category)
        if Settings.get_title() and str(files) != "unset":
            for file in files:
                if str(Settings.get_title()) == str(file.get_title()):
                    files = [file]
                    break
        File.FILES = files
        return files

    @staticmethod
    def get_files_by_folder(path):
        """
        Get local files from the local folder path.

        Parameters
        ----------
        path : str
            Path to folder to get files of

        Returns
        -------
        list
            The files at the path

        """

        f = []
        for (dirpath, dirnames, filenames) in walk(path):
            f.extend(filenames)
            break
        return f

    def get_folder_by_name(category, parent=None):
        """
        Get local folder by category and parent.

        Parameters
        ----------
        category : str
            The category or folder name to get
        parent : file.Folder
            The local folder's parent to search within

        Returns
        -------
        str
            The folder path of the found folder

        """

        if not parent:
            parent = Settings.get_local_path()
        Settings.maybe_print("parent: {}".format(parent))
        f = []
        for (dirpath, dirnames, filenames) in walk(parent):
            Settings.dev_print("dirpath: {}".format(dirpath))
            for dir_ in dirnames:
                Settings.dev_print("dir: {} = {} :category".format(dir_, category))
                if str(dir_) == str(category):
                    return os.path.join(parent, dir_)
            break
        return None













































































































































































    @staticmethod
    def get_folders_of_folder_by_keywords(categoryFolder):
        """
        Summary line.

        Extended description of function.

        Parameters
        ----------
        arg1 : int
            Description of arg1
        arg2 : str
            Description of arg2

        Returns
        -------
        int
            Description of return value

        """

        Settings.dev_print("getting keywords of folder: {}".format(categoryFolder))
        if categoryFolder == None: return []
        folders = File.get_folders_of_folder(categoryFolder)
        folders_ = []
        for folder in folders:
            if Settings.get_drive_keyword() and str(folder.get_title()) != str(Settings.get_drive_keyword()):
                Settings.dev_print("{} -> not keyword".format(folder.get_title()))
                continue
            elif Settings.get_drive_ignore() and str(folder.get_title()) == str(Settings.get_drive_ignore()):
                Settings.dev_print("{} -> by not keyword".format(folder.get_title()))
                continue
            elif str(folder.get_title()) == str(Settings.get_drive_keyword):
                Settings.dev_print("{} -> by keyword".format(folder.get_title()))
            else:
                Settings.dev_print("{}".format(folder.get_title()))
            folders_.append(folder)
        return folders_

    @staticmethod
    def get_random_file():
        """Get random file from all files"""

        return random.choice(File.get_files())

    @staticmethod
    def get_images_of_folder(folder):
        """
        Summary line.

        Extended description of function.

        Parameters
        ----------
        arg1 : int
            Description of arg1
        arg2 : str
            Description of arg2

        Returns
        -------
        int
            Description of return value

        """

        Settings.dev_print("getting images of folder: {}".format(folder.get_title()))
        if not folder: return []
        imgs = []
        files = []
        valid_images = [".jpg",".gif",".png",".tga",".jpeg"]
        for f in os.listdir(folder.get_path()):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in valid_images:
                continue
            file = File()
            setattr(file, "path", os.path.join(folder.get_path(),f))
            files.append(file)
            Settings.maybe_print("image path: {}".format(os.path.join(folder.get_path(),f)))
        return files

    @staticmethod
    def get_videos_of_folder(folder):
        """
        Summary line.

        Extended description of function.

        Parameters
        ----------
        arg1 : int
            Description of arg1
        arg2 : str
            Description of arg2

        Returns
        -------
        int
            Description of return value

        """

        Settings.dev_print("getting videos of folder: {}".format(folder.get_title()))
        if not folder: return []
        videos = []
        files = []
        valid_videos = [".mp4",".mov"]
        for f in os.listdir(folder.get_path()):
            ext = os.path.splitext(f)[1]
            if ext.lower() not in valid_videos:
                continue
            file = File()
            setattr(file, "path", os.path.join(folder.get_path(),f))
            files.append(file)
            Settings.maybe_print("video path: {}".format(os.path.join(folder.get_path(),f)))
        return files

    @staticmethod
    def get_folders_of_folder(folderPath):
        """
        Summary line.

        Extended description of function.

        Parameters
        ----------
        arg1 : int
            Description of arg1
        arg2 : str
            Description of arg2

        Returns
        -------
        int
            Description of return value

        """

        # os.walk(directory)
        # will yield a tuple for each subdirectory. Ths first entry in the 3-tuple is a directory name, so
        # [x[0] for x in os.walk(directory)]
        # should give you all of the subdirectories, recursively.
        # Note that the second entry in the tuple is the list of child directories of the entry in the first position, so you could use this instead, but it's not likely to save you much.
        # However, you could use it just to give you the immediate child directories:
        Settings.maybe_print("local walk: {}".format(folderPath))
        folders = []
        # Settings.print(os.walk(folderPath))
        for folder in next(os.walk(folderPath))[1]:
            Settings.maybe_print("folder: {}".format(folder))
            fol = Folder()
            setattr(fol, "path", os.path.join(folderPath, folder))
            folders.append(fol)
        return folders

    @staticmethod
    def get_files_by_category(cat, performer=None):
        """
        Summary line.

        Extended description of function.

        Parameters
        ----------
        arg1 : int
            Description of arg1
        arg2 : str
            Description of arg2

        Returns
        -------
        int
            Description of return value

        """

        Settings.maybe_print("loading local files...")
        files = []
        ##
        def parse_categories(category, categoryFolder=None):
            """
            Summary line.

            Extended description of function.

            Parameters
            ----------
            arg1 : int
                Description of arg1
            arg2 : str
                Description of arg2

            Returns
            -------
            int
                Description of return value

            """

            files = []
            # return File.get_files_by_category(cat)
            if "image" in str(category):
                categoryFolder = File.get_folder_by_name(category, parent=categoryFolder)
                for folder in File.get_folders_of_folder_by_keywords(categoryFolder):
                    if not folder: continue
                    for image in File.get_images_of_folder(folder):
                        file = File()
                        setattr(file, "path", imageget_path())
                        setattr(file, "category", folder.get_title())
                        files.append(file)
            elif "video" in str(category):
                categoryFolder = File.get_folder_by_name(category, parent=categoryFolder)
                for folder in File.get_folders_of_folder_by_keywords(categoryFolder):
                    if not folder: continue
                    videos = File.get_videos_of_folder(folder)
                    # if len(videos) > 0:
                        # files.append(folder)
                    for video in videos:
                        file = File()
                        setattr(file, "path", video.get_path())
                        setattr(file, "category", folder.get_title())
                        files.append(file)
            elif "performer" in str(category):
                categoryFolder = File.get_folder_by_name(category, parent=categoryFolder)
                for performer_ in File.get_folders_of_folder_by_keywords(categoryFolder):
                    # for performer in File.get_folders_of_folder(folder):
                    if not performer_: continue
                    p = Folder()
                    setattr(p, "path", performer_.get_path())
                    setattr(p, "category", categoryFolder.get_title())
                    files.append(p)
            # elif "galler" in str(category):
            else:
                categoryFolder = File.get_folder_by_name(category, parent=categoryFolder)
                for folder in File.get_folders_of_folder_by_keywords(categoryFolder):
                    if not folder: continue
                    galleries = File.get_folders_of_folder(folder)
                    if len(galleries) > 0:
                        files.append(folder)
                    for gallery in galleries:
                        file = Folder()
                        setattr(file, "path", galleryget_path())
                        setattr(file, "category", folder.get_title())
                        files.append(file)
            return files
        ##
        if performer:
            categoryFolder = File.get_folder_by_name("performers")
            for performerFolder in File.get_folders_of_folder_by_keywords(categoryFolder):
                if str(performer) == str(performerFolder.get_title()):
                    return parse_categories(cat, categoryFolder=performerFolder)
        return parse_categories(cat)

    @staticmethod
    def select_file(category, performer=None):
        """
        Summary line.

        Extended description of function.

        Parameters
        ----------
        arg1 : int
            Description of arg1
        arg2 : str
            Description of arg2

        Returns
        -------
        int
            Description of return value

        """

        files = File.get_files_by_category(category, performer=performer)
        files_ = []
        for file in files:
            if isinstance(file, str):
                files_.append(PyInquirer.Separator())
                continue
            file.category = category
            file_ = {
                "name": file.get_title(),
                "value": file,
            }
            files_.append(file_)
        if len(files_) == 0:
            Settings.print("Missing Files")
            return
        files_.append({
            "name": 'Back',
            "value": None,
        })
        question = {
            'type': 'list',
            'name': 'file',
            'message': 'File Path:',
            'choices': files_,
            # 'filter': lambda file: file.lower()
        }
        answer = PyInquirer.prompt(question)
        if not answer: return File.select_files()
        file = answer["file"]
        if not Settings.confirm(file.get_path()): return None
        return file

    @staticmethod
    def select_files():
        """
        Summary line.

        Extended description of function.

        Parameters
        ----------
        arg1 : int
            Description of arg1
        arg2 : str
            Description of arg2

        Returns
        -------
        int
            Description of return value

        """

        if not Settings.is_prompt(): return [File.get_random_file()]
        category = Settings.select_category()
        if not category: return File.select_file_upload_method()
        # if not Settings.confirm(category): return File.select_files()
        Settings.print("Select Files or a Folder")
        files = []
        while True:
            file = File.select_file(category)
            if not file: break
            ##
            if "performer" in str(category):
                cat = Settings.select_category([cat for cat in Settings.get_categories() if "performer" not in cat])
                performerName = file.get_title()
                file = File.select_file(cat, performer=performerName)
                if not file: break
                setattr(file, "performer", performerName)
                files.append(file)
                if "galler" in str(cat) or "video" in str(cat): break
            ##
            files.append(file)
            if "galler" in str(category) or "video" in str(category): break
        if str(files[0]) == "unset": return files
        if not Settings.confirm([file.get_title() for file in files]): return File.select_files()
        return files

    @staticmethod
    def select_file_upload_method():
        """
        Menu to select the method to upload a file.

        Returns
        -------
        list
            The appropriately selected files

        """

        if not Settings.prompt("upload files"): 
            return "unset"
        Settings.print("Select an upload source")
        sources = Settings.get_source_options()
        question = {
            'type': 'list',
            'name': 'upload',
            'message': 'Upload:',
            'choices': [src.title() for src in sources]
        }
        upload = PyInquirer.prompt(question)["upload"]


        # everything after this part should be in another function
        # this should just return the string of the upload source


        if str(upload) == "Local":
            return File.select_files()
        elif str(upload) == "Remote":
            return Remote.select_files()
        return File.select_files()















    def upload(self):
        """
        Process ran by a file after it has been uploaded.

        Ensures the file has been backed up and then deleted locally.
        
        Returns
        -------
        bool
            Whether or not the file was properly handled after its upload

        """
        if not self.prepare():
            Settings.err_print("unable to upload file - {}".format(self.get_title()))
            return False
        self.backup()
        self.delete()
        return True

##


































class Remote_File(File):
    def __init__(self):
        File.__init__(self)

    def backup(self):
        if not File.backup_text(self.get_title()): return
        if Settings.get_destination() == "remote":
            Remote.backup_file(self)
        else:
            file = self.download()
            file.backup()
            self.delete()

    def delete(self):
        if not File.delete_text(self.get_title()): return
        try: 
            Remote.delete_file(self)
            Settings.print('File Deleted: {}'.format(self.get_title()))
        except Exception as e: Settings.dev_print(e)

    def download(self):
        if not File.download_text(self.get_title()): return False
        file = Remote.download_file(self)
        if not file: return False
        ### Finish ###
        if not file.check_size():
            Settings.err_print("missing downloaded file")
            return False
        Settings.print("Downloaded: {}".format(file.get_title()))
        return file

##

class Folder(File):
    def __init__(self):
        File.__init__(self)
        self.files = None

    def backup(self):
        if File.backup_text(self.get_title()): return

    def check_size(self):
        for file in self.get_files():
            exists = file.check_size()
            if not exists: return False
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


    def download(self):
        Settings.print("Downloading Folder: {}".format(self.get_title()))
        if len(self.files) == 0:
            file_list = Google.get_files_by_folder_id(self.get_id())
            self.files = []
            for file in file_list:
                file_ = Google_File()
                setattr(file_, "id", file["id"])
                setattr(file_, "file", file)
                self.files.append(file_)
        folder_size = len(self.files)
        Settings.maybe_print("folder size: {}".format(folder_size))
        Settings.maybe_print("upload limit: {}".format(Settings.get_upload_max()))
        if int(folder_size) == 0:
            Settings.err_print("empty folder")
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
            Settings.print("Downloading: {} ({}/{})".format(file.get_title(), i, folder_size))
            file.download()
            i+=1
        Settings.print()
        Settings.print("Downloaded Folder: {}".format(self.get_title()))

    def get_files(self):
        if not self.files and self.path:
            self.files = []
            files = File.get_files_by_folder(self.get_path())
            for file in files:
                file_ = File()
                setattr(file_, "path", os.path.join(self.get_path(), file))
                self.files.append(file_)
                Settings.maybe_print("local file found: {}".format(file_.get_title()))
        if Settings.get_title():
            for file in self.files:
                if str(Settings.get_title()) == str(file.get_title()):
                    self.files = [file]
                    break
        return self.files

    def get_title(self):
        if self.title: return self.title
        path = self.get_path()
        if str(path) == "": 
            Settings.err_print("missing file title")
            return ""
        title = os.path.basename(path)
        self.title = title
        return self.title

    def prepare():
        prepared = False
        for file in self.get_files():
            prepared_ = file.prepare()
            if prepared_: prepared = prepared_
        return prepared

###################################################################################

class Image(File):
    def __init__(self):
        pass

    def prepare(self):
        Settings.maybe_print("preparing image: {}".format(self.get_title()))
        return super()

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
        Settings.maybe_print("preparing video: {}".format(self.get_title()))
        self.reduce()
        self.repair()
        self.watermark()
        return super()

    def reduce(self):
        if not Settings.is_reduce(): 
            Settings.maybe_print("skipping: video reduction")
            return
        path = self.get_path()
        global FIFTY_MEGABYTES
        if (int(os.stat(str(path)).st_size) < FIFTY_MEGABYTES or str(Settings.is_reduce()) == "False"):
            return
        Settings.dev_print("reduce: {}".format(self.get_title()))
        self.path = ffmpeg.reduce(path)
    
    # unnecessary
    def repair(self):
        if not Settings.is_repair():
            Settings.dev_print("skipping: video repair")
            return
        path = self.get_path()
        if Settings.is_repair():
            return
        Settings.dev_print("repair: {}".format(self.get_title()))
        self.path = ffmpeg.repair(path)


