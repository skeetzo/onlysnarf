#!/bin/python3

# https://github.com/dropbox/dropbox-sdk-python/blob/main/example/updown.py

"""Download the contents of your OnlySnarf Downloads folder to local uploads folders.

/OnlySnarf/post         -->     ~/.onlysnarf/uploads/post
/OnlySnarf/message      -->     ~/.onlysnarf/uploads/message

"""

from __future__ import print_function
from pathlib import Path

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

from OnlySnarf.util.config import create_default_config, parse_config, search_for_config
from OnlySnarf.classes.message import Message, Post

rootdir = os.path.expanduser("~/.onlysnarf/uploads")
parser = argparse.ArgumentParser(description='Scan ~/.onlysnarf/uploads for uploads')
# parser.add_argument('folder', nargs='?', default='Uploads', help='Folder name in your Dropbox')
parser.add_argument('rootdir', nargs='?', default='~/.onlysnarf/uploads', help='Local directory to upload from')
parser.add_argument('--yes', '-y', action='store_true', help='Answer yes to all questions')
parser.add_argument('--no', '-n', action='store_true', help='Answer no to all questions')
parser.add_argument('--default', '-d', action='store_true', help='Take default answer on all questions')
parser.add_argument('--random', '-r', action='store_true', help='Upload at random')
parser.add_argument('--oldest', '-o', action='store_true', help='Upload oldest file')
parser.add_argument('--youngest', '-l', action='store_true', help='Upload youngest file')
parser.add_argument('--name', action='store_true', help='Upload filename or folder by name')
subparsers = parser.add_subparsers(help='Include a sub-command to run a corresponding action:', dest="action", required=True)
parser_config = subparsers.add_parser('post', help='> scan for posts to upload')
parser_config = subparsers.add_parser('message', help='> scan for a message to upload')

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
	print('Local directory:', rootdir)
	if not os.path.exists(rootdir):
		print(rootdir, 'does not exist on your filesystem')
		sys.exit(1)
	elif not os.path.isdir(rootdir):
		print(rootdir, 'is not a folder on your filesystem')
		sys.exit(1)

	if args.action == "post":
		scan_posts(args)
	elif args.action == "message":
		scan_messages(args)

# TODO: change to get_config_for_upload_path ?
def get_config_for_upload(upload):
	config = None
	# check if config exists for dir / filename
	# if the upload has a config file, use it
	config = search_for_config(upload)
	print(config)
	if not config:
		# else create a config file
		create_default_config(upload)
		config = search_for_config(upload)
		print(config)
	# load the config as args
	parsed_config = parse_config(config)
	print(parsed_config)

	# ensure / replace file links in config file with absolute paths 
	parsed_config.input = update_default_paths(parsed_config.input, config)
	print(parsed_config)
	
	return parsed_config

def get_file_or_folder_to_upload(uploads, options={'random': False,'oldest': False,'youngest': False,'name':False,'file':False,'folder':False}):
	files = []
	print(f"getting file or folder from upload options: {len(uploads)}")
	if options.name:
		for filepath in uploads:
			print(f"filepath: {filepath}")
			if str(filepath) == str(options.name) or str(options.name) in str(filepath):
				return filename

	# don't bother trying to code the exclusivity much, just let younger override older
	if options.oldest:
		files.append(get_oldest_file_in_files(uploads))
	if options.youngest:
		files.append(get_youngest_file_in_files(uploads))

	# return a random file from whichever files have been selected so far
	if options.random:
		return random.choice(files)

	print("Warning: unable to find matching file or folder!")
	return None






# what the fuck do i want the actual process to be again?

# scan files / folders
# if a config file is found, use that (contains file information in args)

# if not, and getting random, return a random file or folder
# if not random, get a file or folder (based on preference) and based on youngest or oldest





# scan /posts for anything
def scan_posts(args):


	# TODO: i need to change this whole order of operations going on here
	uploads = scan_for_uploads("posts")
	upload = get_file_or_folder_to_upload(uploads, args)



	config = get_config_for_upload(upload)
	Post.create_post(config).send()

# scan /messages for anything
def scan_messages(args):
	# copy from scan_posts
	# Message.create_message(config).send()
	pass

# returns all "options" found which are either folders or files
def scan_for_uploads(place="both"):
	print(f"scanning for {place}...")
	if place == "both":
		upload_options = []
		upload_options.extend(scan_for_uploads("posts"))
		upload_options.extend(scan_for_uploads("messages"))
		return upload_options
	upload_options = []
	scanPath = os.path.join(rootdir, place)
	for dn, dirs, files in os.walk(scanPath):
		subfolder = dn[len(scanPath):].strip(os.path.sep)
		upload_options.extend(dirs)
		print('Descending into', subfolder, '...')
		# First do all the files.
		for name in files:
			fullname = os.path.join(dn, name)
			if not isinstance(name, six.text_type):
				name = name.decode('utf-8')
			nname = unicodedata.normalize('NFC', name)
			if name.startswith('.'):
				print('Skipping dot file:', name)
			elif name.startswith('@') or name.endswith('~'):
				print('Skipping temporary file:', name)
			elif name.endswith('.pyc') or name.endswith('.pyo'):
				print('Skipping generated file:', name)
			elif name.endswith('.conf'):
				print('Skipping config file:', name)
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
		dirs[:] = keep
	upload_options = list(set(upload_options))
	return upload_options

################################################################################################################################################

# search through the options for the youngest file or directory by checking metadata
def get_oldest_file_in_files(files):
	print("getting oldest")
	oldest_file = files[0]
	oldest_date = os.path.getmtime(files[0])
	for file in files:
		mtime = os.path.getmtime(file)
		mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
		print(mtime_dt)
		if mtime_dt > oldest_date:
			oldest_date = mtime_dt
			oldest_file = file
	return oldest_file	    

def get_youngest_file_in_files(files):
	print("getting youngest")
	youngest_file = files[0]
	youngest_date = os.path.getmtime(files[0])
	for file in files:
		mtime = os.path.getmtime(file)
		mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
		print(mtime_dt)
		if mtime_dt < youngest_date:
			youngest_date = mtime_dt
			youngest_file = file
	return youngest_file

################################################################################################################################################
################################################################################################################################################


# scan for an image file
def scan_for_image():
	pass
# scan for a video file
def scan_for_video():
	pass
# scan for a folder with multiple images in it
def scan_for_gallery():
	pass



# # probably won't be used
# def scan_for_configs():
# 	configs = []
# 	for dn, dirs, files in os.walk(rootdir):
# 		subfolder = dn[len(rootdir):].strip(os.path.sep)
# 		for file in files:
# 			if file == "config.conf":
# 				fullname = os.path.join(dn, file)
# 				config_file = configparser.ConfigParser()
# 				config_file.read(fullname)
# 				config = {}
# 				# relabels config for cleaner usage
# 				for section in config_file.sections():
# 				  for key in config_file[section]:
# 					if section == "ARGS":
# 					  config[key] = config_file[section][key]
# 					  # print(key, config[key])
# 					else:
# 					  config[section.lower()+"_"+key.lower()] = config_file[section][key].strip("\"")
# 					  # print(key, config[section.lower()+"_"+key.lower()])
# 				print(config)
# 				configs.append(config)
# 	return configs