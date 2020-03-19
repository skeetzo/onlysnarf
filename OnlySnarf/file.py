from OnlySnarf import ffmpeg
from OnlySnarf import google as Google

class Folder:
    def __init__(self):
        self.files = []
        self.id = None
        self.parentID = None
        self.title = ""

    def backup(self):
        if File.backup_text(self.title): return
        Google.upload_gallery(path=self.path)

##########################################################################################

class File:
    def __init__(self):
        self.path = ""
        self.ext = "" 
        ##
        self.title = ""
        self.category = "" # [image, gallery, video, performer]
        self.googleID = None # google file id
        self.folderName = "" # google folder name
        self.parentID = "" # google parent file id

    ##############################

    # move to backup folder in GDrive
    # Google.move_file
    # Google.move_files
    def backup(self):
        if File.backup_text(self.title): return
        if str(self.path) == "":
            print("Error: Missing File Path - {}".format(self.title))
            return False
        Google.upload_file(path=self.path)
        print('File Backed Up: {}'.format(self.title))

    @staticmethod
    def backup_text(title):
        if str(settings.SKIP_DOWNLOAD) == "True":
            print("Warning: Unable to Backup, skipped download")
            return False
        if str(settings.FORCE_BACKUP) == "True":
            print("Backing Up (forced): {}".format(title))
        elif str(settings.DEBUG) == "True":
            print("Skipping Backup (debug): {}".format(title))
            return False
        elif str(settings.BACKUP) == "False":
            print('Skipping Backup (disabled): {}'.format(title))
            return False
        elif str(settings.SKIP_BACKUP) == "True":
            print('Skipping Backup: {}'.format(title))
            return False
        else:
            print('Backing Up (file): {}'.format(title))
        return True

    @staticmethod
    def backup_files(files=[]):
        if str(settings.SKIP_DOWNLOAD) == "True":
            print("Warning: Unable to Backup, skipped download")
            return
        if str(settings.FORCE_BACKUP) == "True":
            print("Backing Up (forced): {}".format(len(files)))
        elif str(settings.DEBUG) == "True":
            print("Skipping Backup (debug): {}".format(len(files)))
            return
        elif str(settings.BACKUP) == "False":
            print('Skipping Backup (disabled): {}'.format(len(files)))
            return
        elif str(settings.SKIP_BACKUP) == "True":
            print('Skipping Backup: {}'.format(len(files)))
            return
        else:
            print('Backing Up (files): {}'.format(len(files)))
        for file in files:
            file.backup()
        print('Files Backed Up: {}'.format(len(files)))

    def check_size(self):
        size = os.path.getsize(self.get_path())
        settings.maybePrint("File Size: {}kb - {}mb".format(size/1000, size/1000000))
        global ONE_MEGABYTE
        if size <= ONE_MEGABYTE:
            settings.maybePrint("Warning: Small File Size")
        global ONE_HUNDRED_KILOBYTES
        if size <= ONE_HUNDRED_KILOBYTES:
            settings.maybePrint("Error: File Size Too Small")
            print("Error: Download Failure")
            return False
        return True

    @staticmethod
    def combine(files):
        if len(files) == 0: return
        combinedPath = File.get_tmp(files[0])
        for file in files:
            shutil.move(file.path, "{}/{}".format(combinedPath, self.title))
            file.path = "{}/{}".format(combinedPath, self.title)
        self.combined = ffmpeg.combine(combinedPath)

    ##############################

    # Deletes online file
    def delete(self):
        if File.delete_text(self.title): return
        if str(self.path) == "":
            print("Error: Missing File Path - {}".format(self.title))
            return False
        os.remove(self.path)

    @staticmethod
    def delete_text(title):
        if str(settings.SKIP_DOWNLOAD) == "True":
            print("Warning: Unable to Delete, skipped download")
            return False
        if str(settings.FORCE_DELETE) == "True":
            print("Deleting (Forced): {}".format(title))
        elif str(settings.DEBUG) == "True":
            print("Skipping Delete (Debug): {}".format(title))
            return False
        elif str(settings.DELETE_GOOGLE) == "False":
            print('Skipping Delete (Disabled): {}'.format(title))
            return False
        elif str(settings.SKIP_DELETE_GOOGLE) == "True":
            print('Skipping Delete: {}'.format(title))
            return False
        else:
            print('Deleting: {}'.format(title))
        return True

    ##############################

    # "filename (1).ext"
    def get_path(self):
        prefix, ext = os.path.splitext(self.title)
        settings.devPrint("filename: {}|{}".format(prefix, ext))
        filename = str(prefix)+"{}."+str(ext)
        counter = 0
        while os.path.isfile(filename.format(counter)):
            counter += 1
        filename = filename.format(counter)
        settings.devPrint("filename: {}".format(filename))
        return filename

    @staticmethod
    def get_tmp(file):
        # make folder at file.path
        path = "{}/tmp".format(file.path)
        os.mkdir(path)
        return path

    # files are File references
    # file references can be GoogleId references which need to download their source
    # files exist when checked for size
    def prepare(self):
        if not self.check_size():
            return False
        return True

    # upload to GDrive
    # Google.upload_input
    def upload(self):
        # basically handled by backup process
        pass

###################################################################################

class Google_File(File):
    def __init__(self):
        self.id = None
        self.parentID = None
        self.folderName = ""
        self.title
        self.file = None

    def backup(self, arg):
        if self.backup_text(): return
        Google.backup_file(path=Google.get_file(self.id))

    def delete(self, arg):
        if self.delete_text(): return
        Google.delete(path=Google.get_file(self.id))

    def download_text(title):
        if str(settings.SKIP_DOWNLOAD) == "True":
            print("Skipping Download (debug)")
            return False
        return True

    @staticmethod
    def download_files(files=[]):
        settings.maybePrint('Download limit: '+str(settings.IMAGE_DOWNLOAD_LIMIT))
        random.shuffle(files)
        files = files[:int(settings.IMAGE_DOWNLOAD_LIMIT)]
        print('Downloading Files: {}'.format(len(files)))
        i = 1
        for file in sorted(files, key = lambda x: x['title']):
            print('Downloading: {}/{}'.format(i, settings.IMAGE_DOWNLOAD_LIMIT))
            file.download()
        print("Downloaded: {}".format(len(files)))

    # Download File
    def download(self):
        if Google_File.download_text(self.title): return False
        path = self.get_path()
        print("Downloading File: {}".format(self.title))
        # download file
        def method_two():
            self.get_file().GetContentFile(path)
            print("Download Complete: Alternative")
        def method_one():
            try:
                with open(str(path), 'w+b') as output:
                    # print("8",end="",flush=True)
                    file_id = self.id
                    request = DRIVE.files().get_media(fileId=self.id)
                    downloader = MediaIoBaseDownload(output, request)
                    # print("=",end="",flush=True)
                    done = False
                    while done is False:
                        # print("=",end="",flush=True)
                        status, done = downloader.next_chunk()
                        if str(settings.VERBOSE) == "True":
                            print("Downloading: %d%%\r" % (status.progress() * 100), end="")
                    # print("D")
                    print("Download Complete: Regular")
            except Exception as e:
                settings.maybePrint(e)
                return False
            return True 
        successful = method_one() or method_two()
        ### Finish ###
        if not os.path.isfile(str(path)):
            print("Error: Missing Downloaded File")
            return
        self.check_size()
        print("Downloaded: {}".format(self.title))

    def get_file(self):
        if self.file: return self.file
        self.file = Google.get_file(self.id)
        return self.file

    # files are File references
    # file references can be GoogleId references which need to download their source
    # files exist when checked for size
    def prepare(self):
        if not self.check_size():
            self.download()
        return super()


###################################################################################

class Image(File):
    def __init__(self):
        File.__init__(self)
        self.combined = ""

###################################################################################

class Video(File):
    def __init__(self):
        File.__init__(self)
        self.screenshots = []
        self.trimmed = ""
        self.split = ""

    #seconds off front or back
    def trim(self):
        path = self.get_path()
        if str(path) == "":
            print("Error: Missing Path")
            return
        self.trimmed = ffmpeg.trim(path) 

    # into segments (60 sec, 5 min, 10 min)
    def split(self):
        path = self.get_path()
        if str(path) == "":
            print("Error: Missing Path")
            return
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
        if str(path) == "":
            print("Error: Missing Path")
            return
        self.screenshots = ffmpeg.frames(path)

    def reduce(self):
        path = self.get_path()
        if str(path) == "":
            print("Error: Missing Path")
            return
        self.path = ffmpeg.reduce(path)
        # global FIFTY_MEGABYTES
        # if int(os.stat(str(input_)).st_size) >= FIFTY_MEGABYTES or settings.FORCE_REDUCTION: # greater than 1GB
        #     input_ = Google.reduce(input_)
        # data = {"path":str(input_),"text":str(settings.TEXT)}
    
    def repair(self):
        path = self.get_path()
        if str(path) == "":
            print("Error: Missing Path")
            return
        self.path = ffmpeg.repair(path)


