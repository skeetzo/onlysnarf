# i need to configure a script for sending posts & messages via json snippets left in folders

# - read each directories for json file
# if json file,
# - check json file for proper metadata
# else, use default data
# - post / message via OnlySnarf

import json
import os


# metadata with all the basic config / args for input:
# {
# 	text: "text",
# 	files: [ file/path, file/path]
# 	etc ...
# }