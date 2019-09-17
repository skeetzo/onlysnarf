from crontab import CronTab
from OnlySnarf.settings import SETTINGS as settings
    
def deleteCron(comment):
    cron = findCron(comment)
    cron.remove(cron)  

def deleteAllCrons():
    cron = CronTab(user=str(settings.USER))
    cron.remove_all()  

# use cron.comment to set cron name and find crons
def disableCron(comment):
    # find cron by comment
    cron = findCron(comment)
    cron.enable(False)

def enableCron(comment):
    # find cron by comment
    cron = findCron(comment)
    cron.enable()

def createCron(comment,  minute=None, hour=None):
    print("Creating Cron: {}".format(comment))
    if findCron(comment) is not None:
        print("Warning: Cron Exists")
        return
    cron = CronTab(user=str(settings.USER))
    newCron = cron.new(command='onlysnarf -cron -{}'.format(comment), comment=comment);
    newCron.hour.every(1)
    if minute is not None:
        newCron.minute.on(minute)
    if hour is not None:
        newCron.hour.on(hour)
    cron.write()
    for item in cron:  
        print(item)
    print("Created Cron: {}".format(comment))

def listCrons():
    cron = CronTab(user=str(settings.USER))
    for job in cron:
        print(job)

# cron.find_command("command name")
# cron.find_comment("comment")
# cron.find_time(time schedule)
def findCron(comment):
    cron = CronTab(user=str(settings.USER))
    print(cron.find_comment(str(comment)))
    if str(settings.DEBUG) == "True":
        return None
    return True 

###################
##### Special #####
###################

# sends messages to users that were queued for a specific time
def sendQueuedMessages():
    pass


def test():
    createCron("upload-video")
    createCron("upload-video", "30", "11")
    createCron("check-scenes")