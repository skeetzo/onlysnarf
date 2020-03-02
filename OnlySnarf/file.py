
from .ffmpeg import ffmpeg
from .google import Google


class File:
    def __init__(self):
        self.path = ""
        self.ext = "" 
        self.parent = "" # google parent file id
        self.id = "" # google file id
        self.googleFile = None # google file reference

        self.category = "" # [image, gallery, video, performer]
        self.title = ""
        self.artist = ""
        self.genre = ""
        self.albumArtist = ""
        self.folderName = ""

    # move to backup folder in GDrive
    # Google.move_file
    # Google.move_files
    def backup(self):
        if str(settings.SKIP_DOWNLOAD) == "True":
            print("Warning: Unable to Backup, skipped download")
            return
        if str(settings.FORCE_BACKUP) == "True":
            print("Backing Up (forced): {}".format(self.title))
        elif str(settings.DEBUG) == "True":
            print("Skipping Backup (debug): {}".format(self.title))
            return
        elif str(settings.BACKUP) == "False":
            print('Skipping Backup (disabled): {}'.format(self.title))
            return
        elif str(settings.SKIP_BACKUP) == "True":
            print('Skipping Backup: {}'.format(self.title))
            return
        else:
            print('Backing Up (file): {}'.format(self.title))
        if self.googleFile != None:
            Google.backup_file(self.googleFile)
        if str(self.path) != "":
            Google.upload_file(self)
        print('File Backed Up: {}'.format(self.title))

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
        size = os.path.getsize(self.getPath())
        settings.maybePrint("File Size: {}kb - {}mb".format(size/1000, size/1000000))
        global ONE_MEGABYTE
        if size <= ONE_MEGABYTE:
            settings.maybePrint("Warning: Small File Size")
        global ONE_HUNDRED_KILOBYTES
        if size <= ONE_HUNDRED_KILOBYTES:
            settings.maybePrint("Error: File Size Too Small")
            print("Error: Download Failure")

    @staticmethod
    def combine(files):
        if len(files) == 0: return
        combinedPath = File.get_tmp(files[0])
        for file in files:
            shutil.move(file.path, "{}/{}".format(combinedPath, self.title))
            file.path = "{}/{}".format(combinedPath, self.title)
        self.combined = ffmpeg.combine(combinedPath)

    # Deletes online file
    def delete(self):
        if str(settings.SKIP_DOWNLOAD) == "True":
            print("Warning: Unable to Delete, skipped download")
            return
        if str(settings.FORCE_DELETE) == "True":
            print("Deleting (Forced): {}".format(self.title))
        elif str(settings.DEBUG) == "True":
            print("Skipping Delete (Debug): {}".format(self.title))
            return
        elif str(settings.DELETE_GOOGLE) == "False":
            print('Skipping Delete (Disabled): {}'.format(self.title))
            return
        elif str(settings.SKIP_DELETE_GOOGLE) == "True":
            print('Skipping Delete: {}'.format(self.title))
            return
        else:
            print('Deleting: {}'.format(self.title))
        if self.googleFile != None:
            Google.delete(self.googleFile)
        if str(self.path) != "":
            os.remove(self.path)

    # Download File
    def download(self):
        path = self.getPath()
        if str(path) == "":
            print("Error: Missing File Path")
            return
        if os.path.isfile(str(path)):
            print("Error: File Already Exists")
            return
        if str(settings.SKIP_DOWNLOAD) == "True":
            print("Skipping Download (debug)")
            return
        print("Downloading File: {}".format(self.title))
        # download file
        def method_two():
            if self.googleFile != None:
                self.googleFile.GetContentFile(path)
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

    @staticmethod
    def get_tmp(file):
        # make folder at file.path
        path = "{}/tmp".format(file.path)
        os.mkdir(path)
        return path

    # upload to GDrive
    # Google.upload_input
    def upload(self):
        # basically handled by backup process
        pass


class Image:
    def __init__(File):
        File.__init__(self)
        self.combined = ""

    

class Video:
    def __init__(File):
        File.__init__(self)
        self.screenshots = []
        self.trimmed = ""
        self.split = ""

    #seconds off front or back
    def trim(self):
        path = self.getPath()
        if str(path) == "":
            print("Error: Missing Path")
            return
        self.trimmed = ffmpeg.trim(path) 

    # into segments (60 sec, 5 min, 10 min)
    def split(self):
        path = self.getPath()
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
        path = self.getPath()
        if str(path) == "":
            print("Error: Missing Path")
            return
        self.screenshots = ffmpeg.frames(path)

    def reduce(self):
        path = self.getPath()
        if str(path) == "":
            print("Error: Missing Path")
            return
        self.path = ffmpeg.reduce(path)
    
    def repair(self):
        path = self.getPath()
        if str(path) == "":
            print("Error: Missing Path")
            return
        self.path = ffmpeg.repair(path)


