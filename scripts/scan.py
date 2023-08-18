# i need to configure a script for sending posts & messages via json snippets left in folders

import configparser
import json
import os
import shutil
import random
import OnlySnarf

rootdir = os.path.expanduser("~/.onlysnarf/uploads")










#!/bin/python3

# https://github.com/dropbox/dropbox-sdk-python/blob/main/example/updown.py

"""Download the contents of your OnlySnarf Downloads folder to local uploads folders.

/OnlySnarf/post         -->     ~/.onlysnarf/uploads/post
/OnlySnarf/message      -->     ~/.onlysnarf/uploads/message

"""

from __future__ import print_function
from pathlib import Path

import argparse
import contextlib
import datetime
import os
import six
import sys
import time
import unicodedata

parser = argparse.ArgumentParser(description='Scan ~/.onlysnarf/uploads for uploads')

# parser.add_argument('folder', nargs='?', default='Uploads',
#                     help='Folder name in your Dropbox')

parser.add_argument('rootdir', nargs='?', default='~/.onlysnarf/uploads',
                    help='Local directory to upload from')

parser.add_argument('--yes', '-y', action='store_true',
                    help='Answer yes to all questions')

parser.add_argument('--no', '-n', action='store_true',
                    help='Answer no to all questions')

parser.add_argument('--default', '-d', action='store_true',
                    help='Take default answer on all questions')




parser.add_argument('--random', '-r', action='store_true',
                    help='Upload at random')


parser.add_argument('--oldest', '-o', action='store_true',
                    help='Upload oldest file')


parser.add_argument('--youngest', '-l', action='store_true',
                    help='Upload youngest file')

parser.add_argument('--name', '-n', action='store_true',
                    help='Upload filename or folder')



subparsers = parser.add_subparsers(help='Include a sub-command to run a corresponding action:', dest="action", required=True)

parser_config = subparsers.add_parser('post', help='> upload a post')
parser_config = subparsers.add_parser('message', help='> upload a message')




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
    	post(args)
    elif args.action == "message":
    	message(args)


# TODO: finish these
def post(args):
	# scan /posts for anything
	pass
def message(args):
	# scan /messages for anything

	# scan for the upload
	uploads = scan_for_uploads(args.action)

	upload = None

	if args.random:
		upload = random(uploads)
	elif args.oldest:
		upload = get_oldest(uploads)
	elif args.youngest:
		upload = get_youngest(uploads)
	elif args.name:
		for option in uploads:
			if str(option) == args.name:
				upload = option

	config = None
	# check if config exists for dir / filename
	# if the upload has a config file, use it
	config = search_for_config(upload)

	if not config:
		# else create a config file
		create_default_config(upload)
		config = search_for_config(upload)
	# ensure / replace file links in config file with absolute paths 
	update_default_config(upload)

	OnlySnarf.main(config)

# TODO: these

# search through the options for the youngest file or directory by checking metadata
def get_oldest(options):
	pass

def get_youngest(options):
	pass

# search for a config file in or near the provided dir or filename
def search_for_config(path):
	pass







# probably won't be used
def scan_for_configs():
	configs = []
	for dn, dirs, files in os.walk(rootdir):
	    subfolder = dn[len(rootdir):].strip(os.path.sep)
	    for file in files:
		    if file == "config.conf":
		    	fullname = os.path.join(dn, file)
				config_file = configparser.ConfigParser()
		    	config_file.read(fullname)
				config = {}
				# relabels config for cleaner usage
				for section in config_file.sections():
				  for key in config_file[section]:
				    if section == "ARGS":
				      config[key] = config_file[section][key]
				      # print(key, config[key])
				    else:
				      config[section.lower()+"_"+key.lower()] = config_file[section][key].strip("\"")
				      # print(key, config[section.lower()+"_"+key.lower()])
				print(config)
				configs.append(config)
	return configs

def load_config(config_path):
	config_file = configparser.ConfigParser()
	config_file.read(config_path)
	config = {}
	# relabels config for cleaner usage
	for section in config_file.sections():
	  for key in config_file[section]:
	    if section == "ARGS":
	      config[key] = config_file[section][key]
	      # print(key, config[key])
	    else:
	      config[section.lower()+"_"+key.lower()] = config_file[section][key].strip("\"")
	      # print(key, config[section.lower()+"_"+key.lower()])
	print(config)
	return config


# TODO: finish deciding what functions are necessary and flesh them out

def upload_gallery():
	# scan /posts for a folder with images in it
	pass


# copy/paste default config file to target folder
def create_default_config(targetPath):
	shutil.copyfile(OnlySnarf.util.config.get_args_config_file(), targetPath)
	print("created default config at: "+targetPath)
	# TODO: update to return config file path at target path?
	# return 


# update new default config file to appropriately match containing folder (somehow)
def update_default_config():
	pass

# returns all "options" found which are either folders or files
def scan_for_uploads(place="both")

	if place == "both":
		options = []
		options.extend(scan_for_uploads("posts"))
		options.extend(scan_for_uploads("messages"))
		return options

	options = []

	scanPath = os.path.join(rootdir, place)

	for dn, dirs, files in os.walk(scanPath):
        subfolder = dn[len(scanPath):].strip(os.path.sep)

        options.extend(dirs)

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
            options.append(fullname)

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

    options = list(set(options))

    return options


def upload():

	config = scan_for_uploads()

	OnlySnarf.main(config)

	# TODO: finish code flow for scanning to upload posts & messages

	# individual file in the uploads/post/ or uploads/message/ folders      (may or may not contain a config.conf file)
	# individual folder in the uploads/post or the uploads/message folders  (may or may not contain a config.conf file)

	# determine default rule

	# determine specific behavioral rules
	# pick the file or folder of files depending on behaviors such as:
	# 	- oldest first; newest first
	# 	- prefer one folder over another
	# 	- prefer one folder if available
	# 	- check for specific folder or upload nothing

	# if args file is available, load it with load_config()




	