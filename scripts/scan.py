# i need to configure a script for sending posts & messages via json snippets left in folders

import json
import os

# metadata with all the basic config / args for input:
# {
# 	text: "text",
# 	files: [ file/path, file/path]
# 	etc ...
# }


# - read each directories for json file or otherwise recognized config file
# if json file,
# - load as upload.conf
# - check json file for proper args
# else, use defaults

# finally:
# - post / message via OnlySnarf
# - (message if a user is specified)

import configparser


def scan_for_configs():

	config_file = configparser.ConfigParser()

	rootdir = os.path.expanduser("~/.onlysnarf/uploads")
	for dn, dirs, files in os.walk(rootdir):
	    subfolder = dn[len(rootdir):].strip(os.path.sep)

	    for file in files:
		    if file == "config.conf":
		    	fullname = os.path.join(dn, file)
		    	config_file.read(fullname)

		    	# TODO: make this less complicated? or match same global config [ARGS] setup

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


def scan_for_uploads():
	pass

	# TODO:
	# walk the /uploads/* directory and find something to upload
	# determine default rules
	# prepare default args 
	# determine specific behavioral rules
	# create a version of the scan_for_configs function that scans the directory of something specific to upload to check for args before using default args

	# TODO: figure out how to update this to properly receive {} as args / config and also to actually actually actually appear to be a "rest api" if thats relevant
	from OnlySnarf import Snarf 
	Snarf()


