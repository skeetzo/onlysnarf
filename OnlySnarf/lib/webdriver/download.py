# TODO: finish these references

import time
import logging
logger = logging.getLogger(__name__)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from .. import CONFIG, DEFAULT, print_same_line

def download_content(self):
    """Downloads all content (images and video) from the user's profile page"""

    logger.info("downloading content...")
    def scroll_to_bottom():
        try:
            # go to profile page and scroll to bottom
            self.go_to_profile()
            # count number of content elements to scroll to bottom
            num = self.browser.find_element(By.CLASS_NAME, "b-profile__sections__count").get_attribute("innerHTML")
            num = num.replace("K","00").replace(".","")
            logger.debug("content count: {}".format(num))
            for n in range(int(int(int(num)/5)+1)):
                print_same_line("({}/{}) scrolling...".format(n,int(int(int(num)/5)+1)))
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
            logger.info("")
        except Exception as e:
            logger.info(e)
            logger.error("failed to find content to scroll")
    scroll_to_bottom()
    imagesDownloaded = self.download_images()
    videosDownloaded = self.download_videos()
    logger.info("downloaded content")
    logger.info("count: {}".format(len(imagesDownloaded)+len(videosDownloaded)))

def download_images(self, destination=None):
    """Downloads all images on the page"""

    downloaded = []
    downloadMe = []
    try:
        images_ = self.browser.find_elements(By.TAG_NAME, "img")
        images = []

        for image in images_:
            # print(image)
            # print(image.get_attribute("src"))
            if "thumbs.onlyfans.com" not in str(image.get_attribute("src")):
                # print(image.get_attribute("src"))
                images.append(image)

        end = len(images)
        if len(images) == 0:
            logger.warning("no images found!")
            return downloaded
        if not destination: destination = os.path.join(DEFAULT.DOWNLOAD_PATH, "images")
        Path(destination).mkdir(parents=True, exist_ok=True)
        i=0
        for j in range(end):
            try:
                images_ = self.browser.find_elements(By.TAG_NAME, "img")
                images = []

                for image in images_:
                    if "thumbs.onlyfans.com" not in str(image.get_attribute("src")):
                        # print(image.get_attribute("src"))
                        images.append(image)

                # click on each image
                # download each image via class "pswp__img"
                successful = self.move_to_then_click_element(images[j])

                while not successful:
                    driver.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)
                    successful = self.move_to_then_click_element(images[j])

                time.sleep(1)
                hdImages = self.browser.find_elements(By.CLASS_NAME, "pswp__img")
                for image in hdImages:
                    downloadMe.append(image.get_attribute("src"))
                # print(len(downloadMe))
            except Exception as err:
                logger.info("")            
                logger.warning(err)
            finally:
                ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
                i+=1
        logger.info("")
    except Exception as err:
        logger.error(err)

    # print(downloadMe)
    downloadMe = list(set(downloadMe)) # remove duplicates
    # print(downloadMe)

    i=1
    for src in downloadMe:
        # src = ""
        try:
            # if Driver.DOWNLOADING_MAX and i > Driver.DOWNLOAD_MAX_IMAGES: break
            # src = str(image.get_attribute("src"))
            # print(src)
            if not src or src == "" or src == "None" or "/thumbs/" in src or "_frame_" in src or "http" not in src: continue
            print_same_line("downloading image: {}/{}".format(i, len(images)))
            # logger.info("Image: {}".format(src[:src.find(".jpg")+4]))
            # logger.debug("image src: {}".format(src))
                # while os.path.isfile("{}/{}.jpg".format(destination, i)):
                    # i+=1

            # TODO: maybe open image in new tab then download it

            wget.download(src, "{}/{}.jpg".format(destination, i), False)
            downloaded.append(i)
        except Exception as err:
            logger.info("")            
            logger.error(err)
            logger.warning("skipped image: "+src)
        finally:
            i+=1

    return downloaded

def download_messages(self, user="all", destination=None):
    """
    Downloads all content in messages with the user

    Parameters
    ----------
    user : str or classes.User
        The user to download message content from

    """

    logger.info("downloading messages: {}".format(user))
    try:
        if str(user) == "all":
            # from OnlySnarf.classes.user import User
            from ..classes.user import User
            user = random.choice(User.get_all_users())
        self.message_user(user.username)
        time.sleep(1)
        contentCount = 0
        while True:
            self.browser.execute_script("document.querySelector('div[id=chatslist]').scrollTop=1e100")
            time.sleep(1)
            self.browser.execute_script("document.querySelector('div[id=chatslist]').scrollTop=1e100")
            time.sleep(1)
            self.browser.execute_script("document.querySelector('div[id=chatslist]').scrollTop=1e100")
            time.sleep(1)
            images = self.browser.find_elements(By.TAG_NAME, "img")
            videos = self.browser.find_elements(By.TAG_NAME, "video")
            # logger.info((len(images)+len(videos)))
            if contentCount == len(images)+len(videos): break
            contentCount = len(images)+len(videos)
        # download all images and videos

        # TODO: download into correct user folders by username
        imagesDownloaded = self.download_images()
        videosDownloaded = self.download_videos()

        logger.info("downloaded messages")
        logger.info("count: {}".format(len(imagesDownloaded)+len(videosDownloaded)))
    except Exception as e:
        logger.error(e)

def download_videos(self, destination=None):
    """Downloads all videos on the page"""

    downloaded = []
    downloadMe = []
    try:
        # find all video elements on page
        # videos = self.browser.find_elements(By.TAG_NAME, "video")
        # videos = self.browser.find_elements(By.CLASS_NAME, "m-video-item")
        playButtons = self.browser.find_elements(By.CLASS_NAME, "b-photos__item__play-btn")
        end = len(playButtons)

        if len(playButtons) == 0:
            logger.warning("no videos found!")
            return downloaded
        if not destination: destination = os.path.join(DEFAULT.DOWNLOAD_PATH, "videos")
        Path(destination).mkdir(parents=True, exist_ok=True)
        i=0
        for j in range(end):
            src = ""
            playButtons = self.browser.find_elements(By.CLASS_NAME, "b-photos__item__play-btn")

            try:
                # click on play button
                # find new and only video ele on page
                self.move_to_then_click_element(playButtons[i])

                time.sleep(2)

                video = self.browser.find_element(By.CLASS_NAME, "vjs-tech")
                # try:
                # except Exception as e:
                    # pass
                    # try:
                        # video = self.browser.find_element(By.TAG_NAME, "video")
                    # except Exception as e:
                        # pass

                # if not video: continue

                # if Driver.DOWNLOADING_MAX and i > Driver.DOWNLOAD_MAX_VIDEOS: break
                src = str(video.get_attribute("src"))
                if not src or src == "" or src == "None" or "http" not in src: continue
                downloadMe.append(src)
            except Exception as e:
                logger.warning(e)
            finally:
                # self.browser.switch_to.default_content()
                ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
                i+=1

        downloadMe = list(set(downloadMe)) # remove duplicates

        i=1
        for src in downloadMe:
            try:
                print_same_line("downloading video: {}/{}".format(i, end))
                # logger.info("Video: {}".format(src[:src.find(".mp4")+4]))
                # logger.debug("video src: {}".format(src))
                # while os.path.isfile("{}/{}.mp4".format(destination, i)):
                    # i+=1
                wget.download(src, "{}/{}.mp4".format(destination, i), False)
                downloaded.append(i)
            except Exception as e:
                logger.info("")            
                logger.error(e)
                logger.warning("skipped video: "+src)
            finally:
                ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()
                i+=1
        logger.info("")
    except Exception as e:
        logger.error(e)
    return downloaded