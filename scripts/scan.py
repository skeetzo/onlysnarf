# i need to configure a script for sending posts & messages via json snippets left in folders

import configparser
import json
import os
import OnlySnarf

def scan_for_configs():
	config_file = configparser.ConfigParser()
	rootdir = os.path.expanduser("~/.onlysnarf/uploads")
	configs = []
	for dn, dirs, files in os.walk(rootdir):
	    subfolder = dn[len(rootdir):].strip(os.path.sep)
	    for file in files:
		    if file == "config.conf":
		    	fullname = os.path.join(dn, file)
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

def upload_at_random():
	pass
def upload_gallery():
	pass
def post():
	pass
def message():
	pass

# copy/paste default config file to target folder
def create_default_config():
	pass

# update new default config file to appropriately match containing folder (somehow)
def update_default_config():
	pass

def scan_for_uploads():
	# walk the /uploads/* directory and find something to upload
	rootdir = os.path.expanduser("~/.onlysnarf/uploads")
	for dn, dirs, files in os.walk(rootdir):
	    subfolder = dn[len(rootdir):].strip(os.path.sep)
	    for file in files:
		    if file == "config.conf":
		    	fullname = os.path.join(dn, file)

	# OnlySnarf.main(config)

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




	