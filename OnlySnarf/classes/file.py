import os, shutil, random, sys
from os import walk
##
from ..lib.ffmpeg import ffmpeg
from ..util.settings import Settings

###############################################################

class File():
    """File class for manipulating files."""

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

    def __init__(self):
        """File object represents local image/video file"""

        # the path to the file locally
        self.path = ""
        # the file extension
        self.ext = ""
        # image|video, default image
        self.type = "image"
        ##
        # file title reference
        self.title = ""
        # file size
        self.size = 0

    ######################################################################################

    def check_size(self):
        """
        Check file size.

        Returns
        -------
        bool
            Whether or not the file exists by checking size

        """

        size = self.size
        if not size and not os.path.exists(self.get_path()):
            return False
        if size: return True
        size = os.path.getsize(self.get_path())
        Settings.maybe_print("file size: {}kb - {}mb".format(size/1000, size/1000000))
        if size <= File.ONE_HUNDRED_KILOBYTES:
            Settings.warn_print("tiny file size")
        elif size <= File.ONE_MEGABYTE:
            Settings.warn_print("small file size")
        elif size > 0:
            Settings.maybe_print("normal file size")
        else:
            Settings.err_print("empty file size")
            return False
        self.size = size
        return True

    ##############################

    def get_ext(self):
        """Get the file's extension"""

        if self.ext != "": return self.ext
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

        if self.path == "":
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

        if self.title != "": return self.title
        path = self.get_path()
        if str(path) == "": 
            Settings.err_print("missing file title!")
            return ""
        title, ext = os.path.splitext(path)
        self.ext = ext.replace(".","")
        self.title = "{}{}".format(os.path.basename(title), ext)
        return self.title

    @staticmethod
    def get_tmp():
        """Creates / gets the default temporary download directory"""

        download_path = Settings.get_download_path()
        if not os.path.exists(download_path):
            os.mkdir(download_path)
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
        if str(self.get_ext()) in str(File.MIMETYPES_VIDEOS_LIST):
            self.type = Video()
        elif str(self.get_ext()) in str(File.MIMETYPES_IMAGES_LIST):
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

        Settings.maybe_print("preparing file: {}".format(self.get_title()))
        # self.get_type().prepare()
        return self.check_size()

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

    def get_random_file(self):
        """Get random file from all files"""

        return random.choice(self.get_files())

    @staticmethod
    def get_images_of_folder(folder):
        """
        Get images of folder.

        Parameters
        ----------
        folder : str
            The folder path to get images from

        Returns
        -------
        list
            The discovered image files

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
        Get videos of folder.

        Parameters
        ----------
        folder : str
            The folder path to get videos from

        Returns
        -------
        list
            The discovered video files

        """

        Settings.dev_print("getting videos of folder: {}".format(folder.get_title()))
        if not folder: return []
        videos = []
        files = []

        ## TODO: change this to mimetypes

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
        Get folders of folder.

        Parameters
        ----------
        folderPath : str
            The folder path to get folders from

        Returns
        -------
        list
            The discovered folders

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
    def remove_local():
        """
        Delete all local files.

        """

        try:
            Settings.maybe_print('deleting local files...')
            # delete /tmp
            tmp = File.get_tmp()
            if os.path.exists(tmp):
                shutil.rmtree(tmp)
                Settings.maybe_print('local files removed!')
            else:
                Settings.maybe_print('no local files found!')
        except Exception as e:
            Settings.dev_print(e)

    # def upload(self):
    #     """
    #     Process ran by a file after it has been uploaded.

    #     Ensures the file has been backed up and then deleted locally.
        
    #     Returns
    #     -------
    #     bool
    #         Whether or not the file was properly handled after its upload

    #     """
    #     if not self.prepare():
    #         Settings.err_print("unable to upload file - {}".format(self.get_title()))
    #         return False
    #     return True

######################################################################################################################
######################################################################################################################
######################################################################################################################

class Folder(File):
    def __init__(self):
        File.__init__(self)
        self.files = None

    def check_size(self):
        """
        Check the size of the files in the folder to check if the folder exists.

        Returns
        -------
        bool
            Whether or not the folder exists

        """

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

    def get_files(self):
        """
        Get files from the folder.


        Returns
        -------
        list
            The discovered files

        """

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
        """
        Get the title of the folder.

        Returns
        -------
        str
            The folder's title

        """

        if self.title: return self.title
        path = self.get_path()
        if str(path) == "": 
            Settings.err_print("missing file title")
            return ""
        title = os.path.basename(path)
        self.title = title
        return self.title

    def prepare():
        """
        Prepare the files in the folder for handling.

        Returns
        -------
        bool
            Whether or not the folder has been prepared successfully

        """

        Settings.maybe_print("preparing folder: {}".format(self.get_title()))
        prepared = False
        for file in self.get_files():
            prepared_ = file.prepare()
            if prepared_: prepared = prepared_
        return prepared

######################################################################################################################
######################################################################################################################
######################################################################################################################

class Image(File):
    def __init__(self):
        pass

    def prepare(self):
        """
        Prepare the image.

        Returns
        -------
        bool
            Whether or not the image has been prepared

        """

        Settings.maybe_print("preparing image: {}".format(self.get_title()))
        return super().prepare()

######################################################################################################################
######################################################################################################################
######################################################################################################################

class Video(File):
    def __init__(self):
        self.screenshots = []
        self.trimmed = ""
        self.split = ""

    #seconds off front or back
    def trim(self):
        """Trim the video file."""

        path = self.get_path()
        self.trimmed = ffmpeg.trim(path) 

    # into segments (60 sec, 5 min, 10 min)
    def split(self):
        """Split the video file."""

        path = self.get_path()
        self.split = ffmpeg.split(path)

    # unnecessary, handled by onlyfans
    # unless this somehow adds like more metadata
    def watermark(self):
        pass

    # cleanup & label appropriately (digital watermarking?)
    # def get_metadata(self):
        # pass

    # frames for preview gallery
    def get_frames(self):
        """Get frames from the video as screenshots."""

        path = self.get_path()
        self.screenshots = ffmpeg.frames(path)

    def prepare(self):
        """
        Prepare the video.

        Returns
        -------
        bool
            Whether or not the video has been prepared

        """

        Settings.maybe_print("preparing video: {}".format(self.get_title()))
        self.reduce()
        self.repair()
        self.watermark()
        return super().prepare()

    def reduce(self):
        """Reduce the video file."""

        if not Settings.is_reduce(): 
            Settings.maybe_print("skipping: video reduction")
            return
        path = self.get_path()
        if (int(os.stat(str(path)).st_size) < File.FIFTY_MEGABYTES or str(Settings.is_reduce()) == "False"):
            return
        Settings.dev_print("reduce: {}".format(self.get_title()))
        self.path = ffmpeg.reduce(path)
    
    # unnecessary
    # def repair(self):
    #     """Repair the video file."""
        
    #     if not Settings.is_repair():
    #         Settings.dev_print("skipping: video repair")
    #         return
    #     path = self.get_path()
    #     if Settings.is_repair():
    #         return
    #     Settings.dev_print("repair: {}".format(self.get_title()))
    #     self.path = ffmpeg.repair(path)

