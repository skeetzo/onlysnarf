import pysftp, os
from .settings import Settings

# https://pysftp.readthedocs.io/en/release_0.2.9/cookbook.html

myHostname = Settings.get_remote_host()
myUsername = Settings.get_remote_username()
myPassword = Settings.get_remote_password()

def backup_file(file):
	print("Backing Up File Remotely")
	with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
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


def backup_files(files):
	print("Backing Up Files Remotely")
	with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
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

def delete_file(file):
	print("Deleting Remote File")
	if not file.remote_path:
		print("Error: File missing remote path")
		return
	with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
		print("Connection succesfully established ... ")
		pysftp.execute('rm {}'.format(file.remote_path))

# download
def download_file(file):
	print("Downloading Remote File")
	with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
		print("Connection succesfully established ... ")

		# Define the file that you want to download from the remote directory
		# remoteFilePath = '/var/integraweb-db-backups/TUTORIAL.txt'
		remoteFilePath = file.get_path()

		# Define the local path where the file will be saved
		# or absolute "C:\Users\sdkca\Desktop\TUTORIAL.txt"
		localFilePath = './TUTORIAL.txt'

		sftp.get(remoteFilePath, localFilePath)
	# connection closed automatically at the end of the with-block

def read_files():
	print("Reading Remote Files")
	with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword) as sftp:
		print("Connection succesfully established ... ")

		# Switch to a remote directory
		path = os.path.join(Settings.get_mount_path(), Settings.get_drive_path())
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



def select_file():
	# if not Settings.prompt("file path"): return None
	files = read_files()
	question = {
		'type': 'input',
		'name': 'path',
		'message': 'File Path:',
	}
	answer = PyInquirer.prompt(question)
	path = answer["path"]
	if not Settings.confirm(path): return None
	file = File()
	setattr(file, "remote_path", path)
	return file

def select_files():
	if not Settings.prompt("enter files"): return []
	print("Select Remote File Paths")
	files = []
	while True:
		file = select_file()
		if not file: break
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
