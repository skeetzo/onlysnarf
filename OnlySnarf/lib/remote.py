import pysftp, os
import PyInquirer
import random
##
from ..util.settings import Settings


def auth():
	
	global HOSTNAME
	global USERNAME
	global PASSWORD
	global PORT

	# https://pysftp.readthedocs.io/en/release_0.2.9/cookbook.html
	HOSTNAME = str(Settings.get_remote_host())
	USERNAME = str(Settings.get_remote_username())
	PASSWORD = str(Settings.get_remote_password())
	PORT = int(Settings.get_remote_port())
	cnopts = pysftp.CnOpts(knownhosts='known_hosts')
	# cnopts = pysftp.CnOpts(knownhosts='/home/skeetzo/.ssh/known_hosts')
	cnopts.hostkeys = None

	if HOSTNAME == "":
		print("Error: Missing remote host")
		return False
	if USERNAME == "":
		print("Error: Missing remote username")
		return False
	if PASSWORD == "":
		print("Error: Missing remote password")
		return False
	if PORT == "":
		print("Error: Missing remote port")
		return False
	return True

def backup_file(file):
	print("Backing Up File Remotely")
	if not auth(): return
	try:
		with pysftp.Connection(host=HOSTNAME, username=USERNAME, password=PASSWORD, cnopts=cnopts, port=PORT) as sftp:
			Settings.maybe_print("connection succesfully established ... ")

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
		Settings.dev_print(e)

def backup_files(files):
	print("Backing Up Files Remotely")
	if not auth(): return
	try:
		with pysftp.Connection(host=HOSTNAME, username=USERNAME, password=PASSWORD, cnopts=cnopts, port=PORT) as sftp:
			Settings.maybe_print("connection succesfully established ... ")

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
		Settings.dev_print(e)

def upload_file(file):
	print("Uploading Remote File")
	if not auth(): return
	try:
		with pysftp.Connection(host=HOSTNAME, username=USERNAME, password=PASSWORD, cnopts=cnopts, port=PORT) as sftp:
			Settings.maybe_print("connection succesfully established ... ")

			# Define the file that you want to download from the remote directory
			# remoteFilePath = '/var/integraweb-db-backups/TUTORIAL.txt'
			remoteFilePath = file.get_path()

			# Define the local path where the file will be saved
			# or absolute "C:\Users\sdkca\Desktop\TUTORIAL.txt"
			# os.path.join(Settings.get_root_path(), Settings.get_username(), file.category, file.get_title())
			localFilePath = file.get_path()

			sftp.put(localFilePath, remoteFilePath)
		# connection closed automatically at the end of the with-block
	except Exception as e:
		Settings.dev_print(e)

def upload_files(files):
	print("Uploading Remote Files")
	if not auth(): return
	try:
		with pysftp.Connection(host=HOSTNAME, username=USERNAME, password=PASSWORD, cnopts=cnopts, port=PORT) as sftp:
			Settings.maybe_print("connection succesfully established ... ")
			for file in files:
				remoteFilePath = file.get_path()
				localFilePath = file.get_path()
				sftp.put(localFilePath, remoteFilePath)
	except Exception as e:
		Settings.dev_print(e)

def delete_file(file):
	print("Deleting Remote File")
	if not auth(): return
	try:
		if not file.remote_path:
			print("Error: File missing remote path")
			return
		with pysftp.Connection(host=HOSTNAME, username=USERNAME, password=PASSWORD, cnopts=cnopts, port=PORT) as sftp:
			Settings.maybe_print("connection succesfully established ... ")
			sftp.execute('rm {}'.format(file.remote_path))
	except Exception as e:
		Settings.dev_print(e)

# download
def download_file(file):
	print("Downloading Remote File")
	if not auth(): return
	try:
		with pysftp.Connection(host=HOSTNAME, username=USERNAME, password=PASSWORD, cnopts=cnopts, port=PORT) as sftp:
			Settings.maybe_print("connection succesfully established ... ")

			# Define the file that you want to download from the remote directory
			# remoteFilePath = '/var/integraweb-db-backups/TUTORIAL.txt'
			remoteFilePath = file.get_path()

			# Define the local path where the file will be saved
			# or absolute "C:\Users\sdkca\Desktop\TUTORIAL.txt"
			# os.path.join(Settings.get_root_path(), Settings.get_username(), file.category, file.get_title())
			localFilePath = file.get_path()

			sftp.get(remoteFilePath, localFilePath)
			file = File()
			setattr(file, "path", localFilePath)
			return file
		# connection closed automatically at the end of the with-block
	except Exception as e:
		Settings.dev_print(e)

def prepare_dir(sftp=None):
	if not sftp: return
	if not Settings.is_create_missing():
		print("Warning: Not creating missing remote category directories")
		return
	Settings.maybe_print("creating missing remote folders")
	for cat in Settings.get_categories():
		sftp.mkdir(os.path.join(Settings.get_root_path(), Settings.get_username(), cat))

def get_files(category=None, performer=None):
	print("Reading Remote Files")
	if not auth(): return
	if Settings.get_remote_host() == "127.0.0.1" or Settings.get_remote_host() == "localhost":
		print("Please set a remote host")
		return []
	try:
		with pysftp.Connection(host=HOSTNAME, username=USERNAME, password=PASSWORD, cnopts=cnopts, port=PORT) as sftp:
			Settings.maybe_print("connection succesfully established ... ")

			# Switch to a remote directory
			path = os.path.join(Settings.get_root_path(), Settings.get_username())
			if category:
				path = os.path.join(path, category)
			if performer:
				path = os.path.join(path, performer)
			Settings.dev_print("remote file path: {}".format(path))
			try:
				sftp.cwd(path)
			except Exception as e:
				Settings.dev_print(e)
				if "No such file" in str(e):
					prepare_dir(sftp)
					try:
						sftp.cwd(path)
					except Exception as e:
						Settings.dev_print(e)
						return []

			directory_structure = sftp.listdir_attr()

			from .file import Remote_File
			file = Remote_File()
			files = []
			for attr in directory_structure:
				Settings.dev_print("{} {}".format(attr.filename, attr))
				setattr(file, "title", attr.filename)
				setattr(file, "size", sftp.stat(os.path.join(path, attr.filename)).st_size)
				setattr(file, "path", os.path.join(path, attr.filename))
				files.append(file)
				#Settings.print(os.path.join(path, attr.filename))
				#Settings.print(sftp.stat(os.path.join(path, attr.filename)).st_size)
			return files
		# connection closed automatically at the end of the with-block
	except Exception as e:
		Settings.dev_print(e)
		return []

def get_random_file(category=None, performer=None):
	if not category: category = Settings.get_category()
	if not category:
		print("Error: Missing category")
		return None
	return random.choice(get_files(category=category, performer=performer))

def select_file(category, performer=None):
	files = get_files(category=category, performer=performer)
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
		print("Warning: Missing Files")
		return select_files()
	question = {
		'type': 'list',
		'name': 'file',
		'message': 'File:',
		'choices': files_
	}
	answer = PyInquirer.prompt(question)
	file = answer["file"]
	if not Settings.confirm(file.get_title()): return None
	return file

def select_files():
	if not Settings.is_prompt(): return [get_random_file()]
	from .file import File, Remote_File
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
		if isinstance(file, Remote_File): files.append(file)
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
