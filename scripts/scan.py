#!/bin/python3

# https://github.com/dropbox/dropbox-sdk-python/blob/main/example/updown.py

"""Download the contents of your OnlySnarf Downloads folder to local uploads folders.

/OnlySnarf/post         -->     ~/.onlysnarf/uploads/post
/OnlySnarf/message      -->     ~/.onlysnarf/uploads/message

"""

from __future__ import print_function

import os
import six
import sys
import json
import time
import shutil
import random
import datetime
import argparse
import contextlib
import unicodedata
import configparser
from pathlib import Path
from OnlySnarf.util.config import get_config_file_for_path, parse_config, update_default_filepaths
from OnlySnarf.classes.message import Message, Post
from OnlySnarf.classes.file import File

parser = argparse.ArgumentParser(description='Scan ~/.onlysnarf/uploads for uploads')
# parser.add_argument('folder', nargs='?', default='Uploads', help='Folder name in your Dropbox')
parser.add_argument('rootdir', nargs='?', default='~/.onlysnarf/uploads', help='Local directory to upload from')
parser.add_argument('--yes', '-y', action='store_true', help='Answer yes to all questions')
parser.add_argument('--no', '-n', action='store_true', help='Answer no to all questions')
parser.add_argument('--default', '-d', action='store_true', help='Take default answer on all questions')
parser.add_argument('--config', '-c', action='store_true', help='Prefer available configuration files')
parser.add_argument('--random', '-r', action='store_true', help='Upload at random')
parser.add_argument('--oldest', '-o', action='store_true', help='Upload oldest file')
parser.add_argument('--youngest', '-l', action='store_true', help='Upload youngest file')
parser.add_argument('--directory', action='store_true', help='Prefer folders of files')
parser.add_argument('--name', help='Upload filename or folder by name')
parser.add_argument('--file-count', dest="file_count", default=10, help='Number of files to upload')
backupOrDelete = parser.add_mutually_exclusive_group()
backupOrDelete.add_argument('--backup', '-b', action='store_true', help='backup after uploading')
backupOrDelete.add_argument('--delete', action='store_true', help='delete after uploading')
subparsers = parser.add_subparsers(help='Include a sub-command to run a corresponding action:', dest="action", required=True)
parser_config = subparsers.add_parser('post', help='> scan for posts to upload')
parser_config = subparsers.add_parser('message', help='> scan for a message to upload')
parser_config = subparsers.add_parser('test', help='> test processes')

def main():
	"""Main program.

	Parse command line, then iterate over files and directories in 
	Dropbox rootdir and download all files. Skips some temporary files and
	directories, and avoids duplicate uploads by comparing size and
	mtime with the server.
	"""
	args = parser.parse_args()
	if sum([bool(b) for b in (args.yes, args.no, args.default)]) > 1:
		print('At most one of --yes, --no, --default is allowed')
		sys.exit(2)
	rootdir = os.path.expanduser(args.rootdir)
	args.rootdir = rootdir
	print('Local directory:', rootdir)
	if not os.path.exists(rootdir):
		print(rootdir, 'does not exist on your filesystem')
		sys.exit(1)
	elif not os.path.isdir(rootdir):
		print(rootdir, 'is not a folder on your filesystem')
		sys.exit(1)
	scan(vars(args))

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################




# file_count --> change number of files to grab
# directory --> True/False directories only
# config --> True/False configs only
# youngest/oldest/random --> True/False
# name --> '' string match








# def process_upload_config(upload_path, config_path):
# 	parsed_config = {}
# 	# ensure / replace file links in config file with absolute paths 
# 	if config_path:
# 		parsed_config = parse_config(config_path)
# 	else:
# 		# parsed_config = get_config_file_for_path(upload_path)
# 	parsed_config["input"] = update_default_filepaths(parsed_config.get("input", []), config_path if config_path else upload_path)
# 	return parsed_config

# scan /posts for anything

# if configs is specified: only return config files
# otherwise, searches for a file or folder AND then creates a config file at the target location which i actually don't want to do

# this works but doesn't really do what i probably want

# i want it to prefer config files over everything else anyways, because a config file might contain info about the files that are in the same folder as it
# so config files have highest priority no matter what

# then, if no config files are found, i want to upload a random file in a folder or upload a random folder itself

# the files that are in the main 'posts' or 'messages' folder are all meant to be uploaded by themselves (seemingly at random)
# any folders that are in the main posts or messages folder are all meant to be uploaded as whole folders of content (galleries)

# so scan everything from config files, if found one, great, if not, then either use a random file or folder

def get_upload_options(args):
	upload_path = None
	upload_config = {}
	if args["config"]:
		upload_options = scan_for_uploads(args["action"], configs=True, args=args)
		if len(upload_options) > 0:
			upload_path = get_file_or_folder_to_upload(upload_options, options=args)
			upload_config = parse_config(upload_path)
		else:
			print("Warning: unable to find any config files!")
			return None, None
	else:
		upload_options = scan_for_uploads(args["action"], args=args)
		print(upload_options)
		upload_path = get_file_or_folder_to_upload(upload_options, options=args)


	print(f"config: {upload_config}")
	print(f"path: {upload_path}")
	return upload_config, upload_path

def scan(args):
	upload_config, upload_path = get_upload_options(args)
	if not upload_path and not upload_config:
		print("### NO UPLOADS FOUND ###")
		return

	upload_config_path, upload_object = process_upload_object(upload_config, upload_path, args)
	if upload_config_path:
		print(f"upload config path: {upload_config_path}")

	if len(upload_object["input"]) == 0:
		print("Skipping empty upload!")
		return True

	if args["action"] == "post":
		Post.create_post(upload_object).send()
	elif args["action"] == "message":
		Message.create_message(upload_object).send()
	elif args["action"] == "test":
		print("Skipping upload while testing!")
	else:
		return print("Error scanning!")

	if args["backup"]:
		backup_uploaded(upload_object, upload_path, args["action"], config=upload_config_path, debug=True if args["action"] == "test" else False)
	elif args["delete"]:
		remove_uploaded(upload_object, config=upload_config_path, debug=True if args["action"] == "test" else False)
	delete_folder_if_empty(upload_path, debug=True if args["action"] == "test" else False)
	return True

def process_upload_object(upload_config, upload_path, args):
	upload_object = upload_config or {}
	# if no config was found and a path was, check if theres a config in that same area
	if not upload_config and upload_path:
		upload_config = get_config_file_for_path(upload_path)
		if not upload_config:
			upload_object = {}
		else:
			upload_object = parse_config(upload_config)

	if not upload_object and upload_path:
		print("using filename as text...")
		file = File(upload_path)
		upload_object["text"] = file.get_title(with_ext=False)
	
		if args["directory"]:
			upload_object["text"] = "random "+upload_object["text"]
			upload_object["input"] = get_files_in_folder(upload_path, args)
		else:
			upload_object["input"] = [ upload_path ]


	# formatting check
	files = upload_object.get("input", [])
	if not isinstance(files, list):
		files = files.split(",")


	upload_object["input"] = update_default_filepaths(files, upload_path)
	print("Final upload object:")
	print(upload_object)
	return upload_config, upload_object

################################################################################################################################################

def get_files_in_folder(folder_path, args):
	print(f"folder path: {folder_path}")
	return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))][:args["file_count"]]

################################################################################################################################################

# delete / remove uploaded files & config
def remove_uploaded(upload_object, config=None, debug=False):
	if config and debug:
		print(f"skipping config remove: {config}")
	elif config:
		print(f"removing config file: {config}")
		os.remove(config)
	for file in upload_object["input"]:
		if debug:
			print(f"skipping file remove: {file}")
		else:
			print(f"removing uploaded file: {file}")
			os.remove(file)

def backup_uploaded(upload_object, upload_path, folder, config=None, debug=False):

	parent = Path(upload_path).parent.absolute()
	print(f"upload path: {upload_path}")
	print(f"parent: {parent}")

	# debug = False

	if config:
		backup_path = f"{parent}/{File(config).get_title()}".replace(f"uploads/{folder}", f"uploads/backup/{folder}")
		if debug:
			print(f"skipping conf backup: {config} --> {backup_path}")
		else:
			print(f"backing up config file: {config} --> {backup_path}")
			Path(Path(backup_path).parent.absolute()).mkdir(parents=True, exist_ok=True)
			os.rename(config, backup_path)

	####################################################
	# does this part even happen with the above? no?
	elif ".conf" in str(upload_path):
		backup_path = f"{parent}/{File(upload_path).get_title()}".replace(f"uploads/{folder}", f"uploads/backup/{folder}")
		if debug:
			print(f"skipping conf file backup: {upload_path} --> {backup_path}")
		else:
			print(f"backing up uploaded config: {upload_path} --> {backup_path}")
			Path(Path(backup_path).parent.absolute()).mkdir(parents=True, exist_ok=True)
			os.rename(upload_path, backup_path)
	####################################################


	for file in upload_object["input"]:
		backup_path = f"{parent}/{File(file).get_title()}".replace(f"uploads/{folder}", f"uploads/backup/{folder}")
		if debug:
			print(f"skipping file backup: {file} --> {backup_path}")
		else:
			print(f"backing up uploaded file: {file} --> {backup_path}")
			Path(Path(backup_path).parent.absolute()).mkdir(parents=True, exist_ok=True)
			os.rename(file, backup_path)

def delete_folder_if_empty(upload_path, debug=False):
	# if folder is now empty, remove it
	# BUG: for whatever reason each method tried sometimes bugs out and does not fetch all files ???
	# METHOD 1
	files_remaining = [name for name in os.listdir(upload_path)]
	# METHOD 2
	# files_remaining = []
	# input_dir = Path(upload_path)
	# for file in input_dir.iterdir():
	# 	files_remaining.append(file)
	# METHOD 3
	# for (dirpath, dirnames, filenames) in os.walk(upload_path, topdown=True):
	#     files_remaining.extend(filenames)

	if len(files_remaining) == 0:
		if debug:
			print("skipping empty directory deletion!")
		else:
			print("deleting empty directory!")
			shutil.rmtree(upload_path)
	else:
		print(f"files remaining: {files_remaining}")

################################################################################################################################################

def get_file_or_folder_to_upload(upload_options, options={'random': False,'oldest': False,'youngest': False,'name':False,'file':False,'folder':False}):
	if len(upload_options) == 0:
		print("Warning: no upload options to choose from!")
		return None
	print(f"getting file or folder from upload options: {len(upload_options)}")
	if options["name"]:
		print(f"searching for: {options['name']}")
		for filepath in upload_options:
			if str(File(filepath).get_title()) == str(options["name"]):
				print("exact match!")
				return filepath
		for filepath in upload_options:
			if str(options["name"]) in str(File(filepath).get_title()):
				print("fuzzy match!")
				return filepath
		print("Warning: unable to find matching file or folder!")
		return None
	# don't bother trying to code the exclusivity much, just let younger override older
	elif options["oldest"]:
		return get_oldest_file_in_files(upload_options)
	elif options["youngest"]:
		return get_youngest_file_in_files(upload_options)
	# return a random file from whichever files have been selected so far
	elif options["random"]:
		return random.choice(upload_options)
	# this option is semi random as the list of files will always be different every time anyways even for the same folder
	for upload_option in upload_options:
		if upload_option: return upload_option
	# this should never happen
	print("Error: failed to find files for upload!")
	return None

# returns all "options" found which are either folders or files or specifically config files
# configs = True to only return config files
def scan_for_uploads(place="both", configs=False, args={}):
	print(f"scanning for {place}...")
	upload_options = []
	if place == "both":
		upload_options.extend(scan_for_uploads("post"), args=args)
		upload_options.extend(scan_for_uploads("message"), args=args)
		return upload_options
	scanPath = os.path.join(args["rootdir"], place)
	print(scanPath)
	for dn, dirs, files in os.walk(scanPath):
		subfolder = dn[len(scanPath):].strip(os.path.sep)
		# upload_options.extend(dirs)
		print('Descending into', subfolder, '...')

		if not args["directory"]:
			# First do all the files.
			for name in files:
				fullname = os.path.join(dn, name)
				if not isinstance(name, six.text_type):
					name = name.decode('utf-8')
				nname = unicodedata.normalize('NFC', name)
				if configs and name.endswith('.conf'):
					upload_options.append(fullname)
				if name.startswith('.'):
					print('Skipping dot file:', name)
				elif name.startswith('@') or name.endswith('~'):
					print('Skipping temporary file:', name)
				elif name.endswith('.pyc') or name.endswith('.pyo'):
					print('Skipping generated file:', name)
				if configs: continue
				upload_options.append(fullname)

		# Then choose which subdirectories to traverse.
		keep = []
		for name in dirs:
			if name.startswith('.'):
				print('Skipping dot directory:', name)
			elif name.startswith('@') or name.endswith('~'):
				print('Skipping temporary directory:', name)
			elif name == '__pycache__':
				print('Skipping generated directory:', name)
			elif yesno('Descend into %s' % name, True, args):
				print('Keeping directory:', name)
				keep.append(name)
			else:
				print('OK, skipping directory:', name)

			if args["directory"]:
				upload_options.append(os.path.join(scanPath,subfolder,name))

		dirs[:] = keep
	upload_options = list(set(upload_options))
	return upload_options

################################################################################################################################################

# search through the options for the youngest file or directory by checking metadata
def get_oldest_file_in_files(files):
	print("getting oldest...")
	oldest_file = files[0]
	oldest_date = os.path.getmtime(files[0])
	for file in files:
		mtime = os.path.getmtime(file)
		mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
		if mtime > oldest_date:
			oldest_date = mtime_dt
			oldest_file = file
	print(f"oldest file: {datetime.datetime(*time.gmtime(os.path.getmtime(oldest_file))[:6])}")
	return oldest_file	    

def get_youngest_file_in_files(files):
	print("getting youngest...")
	youngest_file = files[0]
	youngest_date = os.path.getmtime(files[0])
	for file in files:
		mtime = os.path.getmtime(file)
		mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
		if mtime < youngest_date:
			youngest_date = mtime_dt
			youngest_file = file
	print(f"youngest file: {datetime.datetime(*time.gmtime(os.path.getmtime(youngest_file))[:6])}")
	return youngest_file

################################################################################################################################################

def yesno(message, default, args):
    """Handy helper function to ask a yes/no question.

    Command line arguments --yes or --no force the answer;
    --default to force the default answer.

    Otherwise a blank line returns the default, and answering
    y/yes or n/no returns True or False.

    Retry on unrecognized answer.

    Special answers:
    - q or quit exits the program
    - p or pdb invokes the debugger
    """
    if args["default"]:
        print(message + '? [auto]', 'Y' if default else 'N')
        return default
    if args["yes"]:
        print(message + '? [auto] YES')
        return True
    if args["no"]:
        print(message + '? [auto] NO')
        return False
    if default:
        message += '? [Y/n] '
    else:
        message += '? [N/y] '
    while True:
        answer = input(message).strip().lower()
        if not answer:
            return default
        if answer in ('y', 'yes'):
            return True
        if answer in ('n', 'no'):
            return False
        if answer in ('q', 'quit'):
            print('Exit')
            raise SystemExit(0)
        if answer in ('p', 'pdb'):
            import pdb
            pdb.set_trace()
        print('Please answer YES or NO.')

################################################################################################################################################

# TODO: determine usage potential / necessity

# scan for an image file
def scan_for_image():
	pass
# scan for a video file
def scan_for_video():
	pass
# scan for a folder with multiple images in it
def scan_for_gallery():
	pass

if __name__ == '__main__':
    main()