#!/bin/python3

# https://github.com/dropbox/dropbox-sdk-python/blob/main/example/updown.py

"""Download the contents of your OnlySnarf Downloads folder to local uploads folders.

/OnlySnarf/post         -->     ~/.onlysnarf/uploads/post
/OnlySnarf/message      -->     ~/.onlysnarf/uploads/message

"""

from __future__ import print_function
# from pathlib import Path

import os
import six
import sys
import json
import time
# import shutil
import random
import datetime
import argparse
import contextlib
import unicodedata
import configparser

from OnlySnarf.util.config import get_config_file_at_path, parse_config, update_default_filepaths
from OnlySnarf.classes.message import Message, Post

rootdir = os.path.expanduser("~/.onlysnarf/uploads")
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
parser.add_argument('--name', help='Upload filename or folder by name')
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
	scan(args)

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

def process_upload_config(upload_path, config_path):
	parsed_config = {}
	# ensure / replace file links in config file with absolute paths 
	if config_path:
		parsed_config = parse_config(config_path)
	else:
		parsed_config = get_config_file_at_path(upload_path)
	parsed_config.input = update_default_filepaths(parsed_config.input, config_path if config_path else upload_path)
	return parsed_config

# scan /posts for anything
def scan(args):
	if args.config:
		upload_options = scan_for_uploads(args.action, configs=True)
		if len(upload_options) > 0:
			config_path = get_file_or_folder_to_upload(upload_options, options=args)
			return process_upload_config(None, config_path)
		else:
			print("Warning: unable to find any config files!")
			return
	upload_options = scan_for_uploads(args.action)
	upload_path = get_file_or_folder_to_upload(upload_options, options=args)
	if not upload_path: return
	upload_config = process_upload_config(upload_path, None)
	print("### FINAL CONFIG ###")
	print(upload_config)
	return print("### DEBUGGING STOP ###")
	if args.action == "post":
		Post.create_post(upload_config).send()
	elif args.action == "message":
		Message.create_message(upload_config).send()

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################



def get_file_or_folder_to_upload(upload_options, options={'random': False,'oldest': False,'youngest': False,'name':False,'file':False,'folder':False}):
	if len(upload_options) == 0:
		print("Warning: no upload options to choose from!")
		return None
	print(f"getting file or folder from upload options: {len(upload_options)}")
	if options.name:
		for filepath in upload_options:
			print(f"filepath: {filepath}")
			if str(filepath) == str(options.name) or str(options.name) in str(filepath):
				return filename
		print("Warning: unable to find matching file or folder!")
		return None
	# don't bother trying to code the exclusivity much, just let younger override older
	elif options.oldest:
		return get_oldest_file_in_files(upload_options)
	elif options.youngest:
		return get_youngest_file_in_files(upload_options)
	# return a random file from whichever files have been selected so far
	elif options.random:
		return random.choice(upload_options)
	for upload_option in upload_options:
		if upload_option: return upload_option
	# print("Warning: unable to find files for upload!")
	# return None


# returns all "options" found which are either folders or files or specifically config files
# configs = True to only return config files
def scan_for_uploads(place="both", configs=False):
	print(f"scanning for {place}...")
	upload_options = []
	if place == "both":
		upload_options.extend(scan_for_uploads("post"))
		upload_options.extend(scan_for_uploads("message"))
		return upload_options
	scanPath = os.path.join(rootdir, place)
	print(scanPath)
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
			if configs and name.endswith('.conf'):
				upload_options.append(parse_config(fullname))
				continue
			if name.startswith('.'):
				print('Skipping dot file:', name)
			elif name.startswith('@') or name.endswith('~'):
				print('Skipping temporary file:', name)
			elif name.endswith('.pyc') or name.endswith('.pyo'):
				print('Skipping generated file:', name)
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
	print(f"oldest file: {datetime.datetime(*time.gmtime(os.path.getmtime(oldest_file))[:6])}")
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
	print(f"youngest file: {datetime.datetime(*time.gmtime(os.path.getmtime(youngest_file))[:6])}")
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




if __name__ == '__main__':
    main()