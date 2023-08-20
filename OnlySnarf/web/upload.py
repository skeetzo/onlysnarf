
import threading
import concurrent.futures

from ..util.settings import Settings


#####################
### Drag and Drop ###
#####################

def drag_and_drop_file(drop_target, path):
    """
    Drag and drop the provided file path onto the provided element target.


    Parameters
    ----------
    drop_target : WebElement
        The web element to drop the file at path on

    path : str
        The file path to drag onto the web element

    Returns
    -------
    bool
        Whether or not dragging the file was successful

    """

    # https://stackoverflow.com/questions/43382447/python-with-selenium-drag-and-drop-from-file-system-to-webdriver
    JS_DROP_FILE = """
        var target = arguments[0],
            offsetX = arguments[1],
            offsetY = arguments[2],
            document = target.ownerDocument || document,
            window = document.defaultView || window;

        var input = document.createElement('INPUT');
        input.type = 'file';
        input.onchange = function () {
          var rect = target.getBoundingClientRect(),
              x = rect.left + (offsetX || (rect.width >> 1)),
              y = rect.top + (offsetY || (rect.height >> 1)),
              dataTransfer = { files: this.files };

          ['dragenter', 'dragover', 'drop'].forEach(function (name) {
            var evt = document.createEvent('MouseEvent');
            evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);
            evt.dataTransfer = dataTransfer;
            target.dispatchEvent(evt);
          });

          setTimeout(function () { document.body.removeChild(input); }, 25);
        };
        document.body.appendChild(input);
        return input;
    """
    try:
        Settings.maybe_print("dragging and dropping file...")
        Settings.dev_print("drop target: {}".format(drop_target.get_attribute("innerHTML")))
        # BUG: requires double to register file upload
        file_input = drop_target.parent.execute_script(JS_DROP_FILE, drop_target, 0, 0)
        file_input.send_keys(path)
        file_input = drop_target.parent.execute_script(JS_DROP_FILE, drop_target, 50, 50)
        file_input.send_keys(path)
        Settings.debug_delay_check()
        return True
    except Exception as e:
        Settings.err_print(e) 
    return False

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

    if Settings.is_skip_download(): 
        Settings.print("skipping upload (download)")
        return True, True
    elif Settings.is_skip_upload(): 
        Settings.print("skipping upload (upload)")
        return True, True
    if len(files) == 0:
        Settings.maybe_print("skipping upload (empty file list)")
        return True, True
    if Settings.is_skip_upload():
        Settings.print("skipping upload (disabled)")
        return True, True
    files = files[:int(Settings.get_upload_max())]
    Settings.print("uploading file(s): {}".format(len(files)))

    prepared_files = []

    def prepare_file(file):
        # add a better check for this w/ the new API
        if not isinstance(file, File):
            _file = File()
            setattr(_file, "path", file)
            file = _file
        if not file.prepare():
            Settings.err_print("unable to upload - {}".format(file.get_title()))
        else:
            prepared_files.append(file)    

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(prepare_file, files)

    Settings.dev_print("files prepared: {}".format(len(prepared_files)))
    if len(prepared_files) == 0:
        Settings.err_print("skipping upload (unable to prepare files)")
        return False, True

    enter_file = self.browser.find_element(By.ID, "attach_file_photo")
    successful = []

    i = 1
    for file in prepared_files:
        Settings.print('> {} - {}/{}'.format(file.get_title(), i, len(files)))
        i += 1
        successful.append(drag_and_drop_file(enter_file , file.get_path()))
        time.sleep(1)

    if all(successful):
        if self.error_window_upload(): Settings.dev_print("files uploaded successfully!")
        else: Settings.dev_print("files probably uploaded succesfully!")
        time.sleep(1) # bug prevention
        return True, False
        
    Settings.warn_print("a file failed to upload!")
    return False, False




# TODO: used at all?
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
    # prepared_files.append(file)
    # if this doesn't force it then it'll loop forever without a stopper
