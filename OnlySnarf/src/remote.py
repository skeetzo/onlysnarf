import pysftp, os
import PyInquirer
from .settings import Settings

# https://pysftp.readthedocs.io/en/release_0.2.9/cookbook.html

myHostname = Settings.get_remote_host()
myUsername = Settings.get_remote_username()
myPassword = Settings.get_remote_password()
cnopts = pysftp.CnOpts(knownhosts='known_hosts')

def backup_file(file):
	try:
		print("Backing Up File Remotely")
		with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, cnopts=cnopts) as sftp:
			print("Connection succesfully established ... ")

			# Define the file that you want to upload from your local directorty
			# or absolute "C:\Users\sdkca\Desktop\TUTORIAL2.txt"
			# localFilePath = './TUTORIAL2.txt'
			localFilePath = file.get_path()

			# Define the remote path where the file will be uploaded
			# remoteFilePath = '/var/integraweb-db-backups/TUTORIAL2.txt'
			remoteFilePath = os.path.join(Settings.get_local_path(), "posted")
			remoteFilePath = os.path.join(remoteFilePath, file.category, file.title)

			sftp.put(localFilePath, remoteFilePath)
		# connection closed automatically at the end of the with-block
	except Exception as e:
		print(e)

def backup_files(files):
	try:
		print("Backing Up Files Remotely")
		with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, cnopts=cnopts) as sftp:
			print("Connection succesfully established ... ")

			for file in files:
				# Define the file that you want to upload from your local directorty
				# or absolute "C:\Users\sdkca\Desktop\TUTORIAL2.txt"
				# localFilePath = './TUTORIAL2.txt'
				localFilePath = file.get_path()

				# Define the remote path where the file will be uploaded
				# remoteFilePath = '/var/integraweb-db-backups/TUTORIAL2.txt'
				remoteFilePath = os.path.join(Settings.get_local_path(), "posted")
				remoteFilePath = os.path.join(remoteFilePath, file.category, file.title)

				sftp.put(localFilePath, remoteFilePath)
		# connection closed automatically at the end of the with-block
	except Exception as e:
		print(e)

def delete_file(file):
	try:
		print("Deleting Remote File")
		if not file.remote_path:
			print("Error: File missing remote path")
			return
		with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, cnopts=cnopts) as sftp:
			print("Connection succesfully established ... ")
			pysftp.execute('rm {}'.format(file.remote_path))
	except Exception as e:
		print(e)

# download
def download_file(file):
	try:
		print("Downloading Remote File")
		with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, cnopts=cnopts) as sftp:
			print("Connection succesfully established ... ")

			# Define the file that you want to download from the remote directory
			# remoteFilePath = '/var/integraweb-db-backups/TUTORIAL.txt'
			remoteFilePath = file.get_path()

			# Define the local path where the file will be saved
			# or absolute "C:\Users\sdkca\Desktop\TUTORIAL.txt"
			localFilePath = './TUTORIAL.txt'

			sftp.get(remoteFilePath, localFilePath)
		# connection closed automatically at the end of the with-block
	except Exception as e:
		print(e)

def read_files(category=None, performer=None):
	if Settings.get_remote_host() == "127.0.0.1" or Settings.get_remote_host() == "localhost":
		print("Please set a remote host")
		return []
	try:
		print("Reading Remote Files")
		with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, cnopts=cnopts) as sftp:
			print("Connection succesfully established ... ")

			# Switch to a remote directory
			path = os.path.join(Settings.get_mount_path(), Settings.get_drive_path())
			if category:
				path = os.path.join(path, category)
			if performer:
				path = os.path.join(path, performer)
			sftp.cwd(path)

			# Obtain structure of the remote directory '/var/www/vhosts'
			directory_structure = sftp.listdir_attr()

			from .file import File
			file = File()
			for attr in directory_structure:
				print("{} {}".format(attr.filename, attr))
				# setattr(file, "title", attr.filename)
				# setattr(file, "remote_path", attr)
				files.append(file)
			return files
		# connection closed automatically at the end of the with-block
	except Exception as e:
		print(e)

def select_file(category, performer=None):
	# if not Settings.prompt("file path"): return None
	files = read_files(category=category, performer=performer)
	files_ = []
	for file in files:
		if isinstance(file, str):
			files_.append(PyInquirer.Separator())
			continue
		file.category = category
		file_ = {
			"name": file.get_title(),
			"value": file,
		}
		files_.append(file_)
	if len(files_) == 0:
		print("Missing Files")
		return select_files()
	question = {
		'type': 'list',
		'name': 'file',
		'message': 'File:',
		'choices': files
	}
	answer = PyInquirer.prompt(question)
	file = answer["file"]
	if not Settings.confirm(file.get_title()): return None
	return file

def select_files():
	from .file import File
	category = Settings.select_category()
	if not category: return File.select_file_upload_method()
	print("Select Remote File")
	files = []
	while True:
		file = select_file(category)
		if not file: break
		##
		if "performer" in str(category):
			cat = Settings.select_category([cat for cat in Settings.get_categories() if "performer" not in cat])
			performerName = file.get_title()
			file = select_file(cat, performer=performerName)
			if not file: break
			setattr(file, "performer", performerName)
			files.append(file)
			if "galler" in str(cat) or "video" in str(cat): break
		##
		if isinstance(file, File): files.append(file)
		if not Settings.prompt("another file"): break
	if not Settings.confirm([file.get_path() for file in files]): return []
	return files





# sftp = pysftp.Connection('hostname', username='me', password='secret')
# #
# # ... do sftp operations
# #
# sftp.close()    # close your connection to hostname


# with pysftp.Connection('hostname', username='me', password='secret') as sftp:
#     #
#     # ... do sftp operations
#     #
# # connection closed automatically at the end of the with-block
