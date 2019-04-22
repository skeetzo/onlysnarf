#!/usr/bin/python
# 2/7/2019 - Skeetzo
# 4/22/2019 - Skeetzo
# setup & update script for config
import os
import sys
import json

def createGoogle():
	print("Setting Up Google Creds")
	data = {}
	with open('google_creds.txt', 'w') as outfile:
	    json.dump(data, outfile, indent=4, sort_keys=True)

def createConfig():
	print("Setting up Config")
	data = receiveInputs()
	with open('config.json', 'w') as outfile:
	    json.dump(data, outfile, indent=4, sort_keys=True)

def updateConfig(config):
	print("Updating Config")
	print("(k to keep same)")
	data = receiveInputs()
	for key, value in data.items():
		if value.lower() == "k":
			continue
		config[key] = value
	with open('config.json', 'w') as outfile:
	    json.dump(config, outfile, indent=4, sort_keys=True)

def receiveInputs():
	data = {}
	data['username'] = input('Twitter Username: ')
	data['password'] = input('Twitter Password: ')
	data['images_folder'] = input('Google Drive Folder - Images: ')
	data['galleries_folder'] = input('Google Drive Folder - Galleries: ')
	data['performers_folder'] = input('Google Drive Folder - Performers: ')
	data['scenes_folder'] = input('Google Drive Folder - Scenes: ')
	data['videos_folder'] = input('Google Drive Folder - Videos: ')
	data['posted_folder'] = input('Google Drive Folder - Posted (backup location): ')
	return data

def main():
	CONFIG_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)),'config.json')
	GOOGLE_CREDS = os.path.join(os.path.dirname(os.path.realpath(__file__)),'google_creds.txt')
	try:
		with open(CONFIG_FILE) as config_file:    
			config = json.load(config_file)
		updateConfig(config)
	except FileNotFoundError:
		createConfig()
	finally:
		print('Config Updated')
		sys.exit(0)

if __name__ == "__main__":
	main()