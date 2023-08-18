dbx = get_dropbox_client()

folder_path = '' # root folder
all_files = [] # collects all files here
has_more_files = True # because we haven't queried yet
cursor = None # because we haven't queried yet

while has_more_files:
    if cursor is None: # if it is our first time querying
        result = dbx.files_list_folder(folder_path)
    else:
        result = dbx.files_list_folder_continue(cursor)
    all_files.extend(result.entries)
    cursor = result.cursor
    has_more_files = result.has_more
    
print("Number of total files listed: ", len(all_files))
print("All filenames: ", [entry.name for entry in all_files])