from crontab import CronTab
from OnlySnarf.settings import SETTINGS as settings

################
##### Cron #####
################

def delete(comment):
    cron = CronTab(user=str(settings.CRON_USER))
    cron.remove_all(comment=comment)
    cron.write()
    print("Cron Deleted: {}".format(comment))

def deleteAll():
    cron = CronTab(user=str(settings.CRON_USER))
    cron.remove_all()
    cron.write()
    print("Crons Deleted")

# use cron.comment to set cron name and find crons
def disable(comment):
    # find cron by comment
    cron = find(comment)
    cron.enable(False)
    cron.write()
    print("Cron Disabled: {}".format(comment))

def enable(comment):
    # find cron by comment
    cron = find(comment)
    cron.enable()
    cron.write()
    print("Cron Enabled: {}".format(comment))

def create(comment, args=[], minute=None, hour=None):
    print("Creating Cron: {}".format(comment))
    # if find(comment) is not None:
        # print("Warning: Cron Exists")
    cron = CronTab(user=str(settings.CRON_USER))
    cron.remove_all(comment=comment)
    args = [n.strip() for n in args]
    newCron = cron.new(command="onlysnarfpy -cron {} {}".format(comment, " ".join(args)), comment=comment);
    newCron.hour.every(1)
    if minute is not None:
        newCron.minute.on(minute)
    if hour is not None:
        newCron.hour.on(hour)
    cron.write()
    print("Created Cron: {}".format(comment))

def list():
    cron = CronTab(user=str(settings.CRON_USER))
    print("Crons:")
    for job in cron:
        print(job)

def find(comment):
    cron = CronTab(user=str(settings.CRON_USER))
    iter1 = cron.find_comment(str(comment))
    for item in iter1:
        return item
    return False 

def getAll():
    cron = CronTab(user=str(settings.CRON_USER))
    jobs = []
    for job in cron:
        jobs.append(job)
    return jobs

###################
##### Special #####
###################

def uploadRandom(opt):
    # newCron = cron.new(command="onlysnarf -cron {} {}".format(comment, " ".join(args)), comment=comment);
    pass

def uploadLater(type_, path):
    args = ["-type",str(type_),"-method","input","-input",path]
    create("upload-me"+str(path), args)
    pass

# check all scenes folders' data.txt's for "releaseDate"
def checkScenes():
    pass

# sends messages to users that were queued for a specific time
def sendQueuedMessages():
    pass

###############
##### Dev #####
###############

def test():
    create("upload-video", args=["-type","video"])
    # create("upload-balls", [], "30", "11")
    # create("check-scenes")
    # disable("upload-video")
    # enable("upload-video")
    return True


# Cron:

# Message:
# - All, etc

# Upload:
# - Gallery
# - Image
# - Video
# - Performer
# - Scene