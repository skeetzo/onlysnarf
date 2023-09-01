import time
import logging
import threading
import concurrent.futures
from selenium.webdriver.common.by import By

from .. import debug_delay_check
from .. import CONFIG

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
        logging.debug("dragging and dropping file...")
        logging.debug("drop target: {}".format(drop_target.get_attribute("innerHTML")))
        # BUG: requires double to register file upload
        file_input = drop_target.parent.execute_script(JS_DROP_FILE, drop_target, 0, 0)
        file_input.send_keys(path)
        file_input = drop_target.parent.execute_script(JS_DROP_FILE, drop_target, 50, 50)
        file_input.send_keys(path)
        debug_delay_check()
        return True
    except Exception as e:
        logging.error(e) 
    return False

##################
##### Upload #####
##################

def upload_files(browser, files):
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

    if CONFIG["skip_download"]: 
        logging.info("skipping upload (download)")
        return True, True
    elif CONFIG["skip_upload"]: 
        logging.info("skipping upload (upload)")
        return True, True
    if len(files) == 0:
        logging.debug("skipping upload (empty file list)")
        return True, True
    if CONFIG["skip_upload"]:
        logging.info("skipping upload (disabled)")
        return True, True
    files = files[:int(CONFIG["upload_max"])]
    logging.info("uploading file(s): {}".format(len(files)))

    prepared_files = []

    def prepare_file(file):
        # add a better check for this w/ the new API
        if not isinstance(file, File):
            _file = File()
            setattr(_file, "path", file)
            file = _file
        if not file.prepare():
            logging.error("unable to upload - {}".format(file.get_title()))
        else:
            prepared_files.append(file)    

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(prepare_file, files)
        
    logging.debug("files prepared: {}".format(len(prepared_files)))
    if len(prepared_files) == 0:
        logging.error("skipping upload (unable to prepare files)")
        return False, True
    enter_file = browser.find_element(By.ID, "attach_file_photo")
    successful = []
    i = 1
    for file in prepared_files:
        logging.info('> {} - {}/{}'.format(file.get_title(), i, len(files)))
        i += 1
        successful.append(drag_and_drop_file(enter_file , file.get_path()))
        time.sleep(1)
    if all(successful):
        if error_window_upload(browser): logging.debug("files uploaded successfully!")
        else: logging.debug("files probably uploaded succesfully!")
        time.sleep(1) # bug prevention
        return True, False
    logging.warning("a file failed to upload!")
    return False, False

def error_window_upload(browser):
    """Closes error window that appears during uploads for 'duplicate' files"""

    try:
        buttons = browser.find_elements(By.CLASS_NAME, "g-btn.m-flat.m-btn-gaps.m-reset-width")
        logging.debug("errors btns: {}".format(len(buttons)))
        if len(buttons) == 0: return True
        for button in buttons:
            if button.get_attribute("innerHTML").strip() == "Close" and button.is_enabled():
                logging.debug("upload error message, closing")
                button.click()
                logging.debug("success: upload error message closed")
                time.sleep(0.5)
                return True
        return False
    except Exception as e:
        Driver.error_checker(e)
    return False

# TODO: used at all?
def fix_filename(file):
    # move file to change its name
    filename = os.path.basename(file.get_path())
    filename = os.path.splitext(filename)[0]
    if "_fixed" in str(filename): return
    logging.debug("fixing filename...")
    filename += "_fixed"
    ext = os.path.splitext(filename)[1].lower()
    logging.debug("{} -> {}.{}".format(os.path.dirname(file.get_path()), filename, ext))
    dst = "{}/{}.{}".format(os.path.dirname(file), filename, ext)
    shutil.move(file.get_path(), dst)
    file.path = dst
    # add file to end of list so it gets retried
    # prepared_files.append(file)
    # if this doesn't force it then it'll loop forever without a stopper