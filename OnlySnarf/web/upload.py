
    ##################
    ##### Upload #####
    ##################

    def upload_files(self, files):
        """
        Upload the files to a post or message.

        Must be on a post or message.

        Parameters
        ----------
        files : list
            The list of files to upload

        Returns
        -------
        bool
            Whether or not the upload was successful

        """

        if str(Settings.is_skip_download()) == "True": 
            Settings.print("skipping upload (download)")
            return True, True
        elif str(Settings.is_skip_upload()) == "True": 
            Settings.print("skipping upload (upload)")
            return True, True
        if len(files) == 0:
            Settings.maybe_print("skipping upload (empty file list)")
            return True, True
        if str(Settings.is_skip_upload()) == "True":
            Settings.print("skipping upload (disabled)")
            return True, True
        files = files[:int(Settings.get_upload_max())]
        Settings.print("uploading file(s): {}".format(len(files)))

        ####

        import threading
        import concurrent.futures

        files_ = []

        def prepare(file):
            # add a better check for this w/ the new API
            if not isinstance(file, File):
                _file = File()
                setattr(_file, "path", file)
                file = _file
            uploadable = file.prepare() # downloads if necessary
            if not uploadable: Settings.err_print("unable to upload - {}".format(file.get_title()))
            else: files_.append(file)    

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            executor.map(prepare, files)

        Settings.dev_print("files prepared: {}".format(len(files_)))
        if len(files_) == 0:
            Settings.err_print("skipping upload (unable to prepare files)")
            return False, True

        ####

        enter_file = self.browser.find_element(By.ID, "attach_file_photo")
        successful = []

        i = 1
        for file in files_:
            Settings.print('> {} - {}/{}'.format(file.get_title(), i, len(files)))
            i += 1
            successful.append(self.drag_and_drop_file(enter_file , file.get_path()))
            time.sleep(1)
            ###
            def fix_filename(file):
                # move file to change its name
                filename = os.path.basename(file.get_path())
                filename = os.path.splitext(filename)[0]
                if "_fixed" in str(filename): return
                Settings.dev_print("fixing filename...")
                filename += "_fixed"
                ext = os.path.splitext(filename)[1].lower()
                Settings.dev_print("{} -> {}.{}".format(os.path.dirname(file.get_path()), filename, ext))
                dst = "{}/{}.{}".format(os.path.dirname(file), filename, ext)
                shutil.move(file.get_path(), dst)
                file.path = dst
                # add file to end of list so it gets retried
                files.append(file)
                # if this doesn't force it then it'll loop forever without a stopper
            ###
        # one last final check
        Settings.debug_delay_check()
        if all(successful):
            if self.error_window_upload(): Settings.dev_print("files uploaded successfully")
            else: Settings.dev_print("files probably uploaded succesfully")
            time.sleep(1) # bug prevention
            return True, False
        Settings.warn_print("a file failed to upload!")
        return False, False
