from crontab import CronTab
from OnlySnarf.settings import SETTINGS as settings
	
def deleteCron(comment):
	cron = findCron(comment)
	cron.remove(cron)  

def deleteAllCrons():
	cron = CronTab(user='root')
	cron.remove_all()  

# use cron.comment to set cron name and find crons
def disableCron(comment):
	# find cron by comment
	cron = findCron(comment)
	if not cron.is_enabled():
	cron.enable(False)

def enableCron(comment):
	# find cron by comment
	cron = findCron(comment)
	if cron.is_enabled():
		print("Warning: Cron already enabled")
		return
	cron.enable()

# i want to be able tocreate crons that will then automatically
# upload a [gallery] from [a random gallery] every day at a time
# so the args need to be able to define what happens when the main gets run
# and this just needs to write a cron that calls onlysnarf with the right args
def createCron(function, args, every="day", atTime="midnight"):
	print("Creating Cron: {}".format(function))
	cron = findCron(function)
	if cron is not None:
		print("Warning: cron already exists")
		return cron
	# add date and timejob.is_valid()  
	# every = "week";"two weeks";"month"
	print("Creating Cron: {}".format(function))
	cron = CronTab(user='root')

	#####
	# args = args.list to string of - in front
	#####
	# "-".join(args)
	args.addToFront(function)

	newCron = cron.new(command="onlysnarf {}".format(args),comment=function);
	
	# figure out date and time and add
	newCron.every().do(job)
	newCron.every(every).at("10:30").do(job)


	if not newCron.is_valid():
		print("Error: Cron not valid")
		return
	#####
	
	for item in cron:  
	    print item
	cron.write()
	print("Created Cron: {}".format(function))

def listCrons():
	cron = CronTab(user='root')
	for job in cron:
	    print job

# cron.find_command("command name")
# cron.find_comment("comment")
# cron.find_time(time schedule)
def findCron(comment):
	cron = CronTab(user='root')
    return cron.find_comment(str(comment)) 

###################
##### Special #####
###################

# greets new subscribers
def greetNewSubcribers():
	pass

# sends messages to users that were queued for a specific time
def sendQueuedMessages():
	pass


# add -scenes to settings to check all scenes data for a scene to release
# check scene data by making a function that checks all the data files and caches it
# for like only 2 or 5 minutes
# the -scenes function runs hourly and checks the folders, forcing the cache to re up date
# so -scenes -force-cache

def checkScenes(comment, function):
	print("Creating Cron: Scenes")
	cron = CronTab(user='root')
	checkScenes = cron.new(command='onlysnarf-menu -scenes');
	checkScenes.hour.every(1)
	for item in cron:  
	    print item
	cron.write()
	print("Created Cron: Scenes")

# create a method to create upload crons that upload standard like an image once a day
# create a method to create upload crons that get input and set cron at specific hour minute every day/week/month

def uploadContent(type=None, minute=None, hour=None):
	print("Creating Cron: Upload")
	if type==None:
		print("Error: Missing Upload Type")
		return
	if minute==None:
		print("Error: Missing Upload Minute")
		return
	if hour==None:
		print("Error: Missing Upload Hour")
		return
	cron = CronTab(user='root')
	createUpload = cron.new(command='onlysnarf-menu -skeetzo -upload {}'.format(type))
	createUpload.minute.on(minute)
	createUpload.hour.on(hour)
	cron.write()
	print("Created Cron: Upload")