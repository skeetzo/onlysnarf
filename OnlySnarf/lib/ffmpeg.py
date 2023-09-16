import logging
logger = logging.getLogger(__name__)
import ffmpeg
import datetime
import os
##
# from ..util.settings import Settings

##################
##### FFMPEG #####
##################

# all videos in folder into single mp4
def combine(folderPath):
    # if str(Settings.COMBINE) == "False":
    #     print("skipping combine")
    #     return False
    if ".mp4" not in str(folderPath):
        print("unable to combine")
        return False
    combinePath = str(folderPath).replace(".mp4", "_full.mp4")
    try:    
        ffmpeg.input(str(folderPath), format='concat', safe=0).output(combinePath, c='copy').run()
    except Exception as e:
        print(e)
        if "Conversion failed!" in str(e):
            print("combine failure")
            return combinePath                    
    print("Combine Complete")
    return combinePath


# images from gallery
def gifify(path):
    # First convert the images to a video:
    # ffmpeg -f image2 -i image%d.jpg video.avi
    loglevel = "quiet"
    # if Settings.is_debug():
        # loglevel = "debug"
    # p = subprocess.call(['ffmpeg', '-loglevel', str(loglevel), '-y', '-i', str(path), '-c', 'copy', '-c:v', 'libx264', '-c:a', 'aac', '-strict', '2', '-crf', '26', '-b:v', str(bitrate), str(reducedPath)])
    # Then convert the avi to a gif:
    # ffmpeg -i video.avi -pix_fmt rgb24 -loop_output 0 out.gif

# frames for preview gallery
def frames(path):
    try:
        print("capturing frames: {}".format(path))
        try:
            clip = VideoFileClip(str(path))
            print("length: {}".format(clip.duration))
        except FileNotFoundError:
            print("missing file to capture frames")
            return path
    except: pass
    screenshots = []
    # ffmpeg -i test.avi -vcodec png -ss 10 -vframes 1 -an -f rawvideo test.png
    for i in range(10):
        output = path.replace(".mp4", "-{}.png".format(i))
        p = subprocess.call(['ffmpeg', '-loglevel', str(loglevel), '-y', '-ss', str(int(i)*10), '-i', str(path), '-vcodec', 'png', '-vframes', '1', '-an', '-f', 'rawvideo', output])
        screenshots.append(output)
        if int(i)*10 > int(clip.duration): break
    return screenshots

# this requires a similar video and has no real use so remove?
# or change to some other repair method for videos
# def repair(path):
#     if str(Settings.get_repair()) == "False":
#         print("skipping repair")
#         return path
#     if ".mp4" not in str(path):
#         print("unable to repair")
#         return path
#     if not os.path.isfile(str(Settings.WORKING_VIDEO)):
#         print("missing working video")
#         return path
#     repairedPath = str(path).replace(".mp4", "_fixed.mp4")
#     try:
#         print("Repairing: {} <-> {}".format(path, Settings.WORKING_VIDEO))
#         if Settings.is_debug():
#             subprocess.call(['untrunc', str(Settings.WORKING_VIDEO), str(path)]).communicate()
#         else:
#             subprocess.Popen(['untrunc', str(Settings.WORKING_VIDEO), str(path)],stdin=FNULL,stdout=FNULL)
#     except AttributeError:
#         if os.path.isfile(str(path)+"_fixed.mp4"):
#             shutil.move(str(path)+"_fixed.mp4", repairedPath)
#             print("Repair Complete")
#     except:
#         print(sys.exc_info()[0])
#         print("skipping repair")
#         return path
#     print("Repair Successful")
#     return str(repairedPath)

def reduce(path):
    if not Settings.is_reduce():
        print("skipping reduction")
        return path
    if ".mp4" not in str(path):
        print("unable to reduce")
        return path
    reducedPath = str(path).replace(".mp4", "_reduced.mp4")
    try:
        print("reducing: {}".format(path))
        try:
            clip = VideoFileClip(str(path))
            print("length: {}".format(clip.duration))
            bitrate = 1000000000 / int(clip.duration)
            print("bitrate: {}".format(bitrate))
        except FileNotFoundError:
            print("missing file to reduce")
            return path
        loglevel = "quiet"
        if Settings.is_debug():
            loglevel = "debug"
        p = subprocess.call(['ffmpeg', '-loglevel', str(loglevel), '-err_detect', 'ignore_err', '-y', '-i', str(path), '-c', 'copy', '-c:v', 'libx264', '-c:a', 'aac', '-strict', '2', '-crf', '26', '-b:v', str(bitrate), str(reducedPath)])
        # p.communicate()
    except FileNotFoundError:
        print("ignoring fixed video")
        return reduce(str(path).replace(".mp4", "_fixed.mp4"))
    except Exception as e:
        print(e)
        if "Conversion failed!" in str(e):
            print("conversion failure")
            return path                    
    print("Reduction Complete")
    originalSize = os.path.getsize(str(path))
    newSize = os.path.getsize(str(reducedPath))
    print("Original Size: {}kb - {}mb".format(originalSize/1000, originalSize/1000000))
    print("Reduced Size: {}kb - {}mb".format(newSize/1000, newSize/1000000))
    if int(originalSize) < int(newSize):
        print("original size smaller")
        return path
    if int(newSize) == 0:
        print("missing reduced file")
        return path
    return reducedPath


# into segments (60 sec, 5 min, 10 min)
# segment: minutes
def split(path, segment):
    if not Settings.is_split():
        print("skipping split")
        return path
    if ".mp4" not in str(path):
        print("unable to split")
        return path
    splitPaths = []
    splitPath = str(path).replace(".mp4", "_split$.mp4")
    try:
        print("splitting: {}".format(path))
        try:
            clip = VideoFileClip(str(path))
            print("length: {}".format(clip.duration))
        except FileNotFoundError:
            print("missing file to split")
            return path
        i = 0
        index = 0
        loglevel = "quiet"
        if Settings.is_debug():
            loglevel = "debug"
        while True:
            start = datetime.timedelta(seconds=index)
            end = datetime.timedelta(seconds=int(index)+(60*int(segment)))
            out = splitPath.replace("$",i)
            p = subprocess.call(['ffmpeg', '-loglevel', str(loglevel), '-ss', str(start), '-y', '-i', str(path), '-to', str(end), '-c', 'copy', '-c:v', 'libx264', '-c:a', 'aac', '-strict', '2', str(out)])
            splitPaths.append(out)
            index += 60*int(segment)
            i += 1
        # p.communicate()
    except Exception as e:
        print(e)
        if "Conversion failed!" in str(e):
            print("split failure")
            return splitPaths                    
    print("Split Complete")
    return splitPaths

def thumbnail_fix(path):
    # if str(Settings.THUMBNAILING_PREVIEW) == "False":
    #     print("preview thumbnailing disabled")
    #     return path
    try:
        print("Thumbnailing: {}".format(path))
        loglevel = "quiet"
        if Settings.is_debug():
            loglevel = "debug"
        thumbnail_path = os.path.join(os.path.dirname(str(path)), 'thumbnail.png')
        print("thumbnail path: {}".format(thumbnail_path))
        p = subprocess.call(['ffmpeg', '-loglevel', str(loglevel), '-i', str(path),'-ss', '00:00:00.000', '-vframes', '1', str(thumbnail_path)])
        p.communicate()
        print("Thumbnailing Complete")
        return thumbedPath
    except FileNotFoundError:
        print("ignoring thumbnail")
    except AttributeError:
        print("Thumbnailing: Captured PNG")
    except:
        print(sys.exc_info()[0])
        print("thumbnailing fuckup")    

#seconds off front or back
def trim(path):
    if not Settings.is_trim():
        print("skipping trim")
        return path
    if ".mp4" not in str(path):
        print("unable to trim")
        return path
    reducedPath = str(path).replace(".mp4", "_trimmed.mp4")
    try:
        print("trimming: {}".format(path))
        try:
            clip = VideoFileClip(str(path))
            print("length: {}".format(clip.duration))
        except FileNotFoundError:
            print("missing file to reduce")
            return path
        start = datetime.timedelta(seconds=60)
        end = datetime.timedelta(seconds=clip.duration-60)
        loglevel = "quiet"
        if Settings.is_debug():
            loglevel = "debug"
        p = subprocess.call(['ffmpeg', '-loglevel', str(loglevel), '-ss', str(start), '-y', '-i', str(path), '-to', str(end), '-c', 'copy', '-c:v', 'libx264', '-c:a', 'aac', '-strict', '2', str(reducedPath)])
        # p.communicate()
    except Exception as e:
        print(e)
        if "Conversion failed!" in str(e):
            print("trim failure")
            return path                    
    print("Trim Complete")
    return reducedPath

# unnecessary, handled by onlyfans
def watermark():
    pass
# cleanup & label appropriately (digital watermarking?)
def metadata():
    pass
