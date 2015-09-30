import giwyn.lib.settings.settings

def open_config_file():
    return open(giwyn.lib.settings.settings.CONFIG_FILE_PATH, "r+")

def close_config_file(f):
    try:
        f.close()
    except:
        print("The file {0} canno't be close".format(f.name))

def clean_config_file(f):
    try:
        f.truncate()
        f.close()
    except:
        print("The file {0} canno't be truncate, and close".format(f.name))

def add_new_path(f, path_to_add):
    try:
        f.write("{0}\n".format(path_to_add))
    except:
        print("The path {0} canno't be added to {1}".format(path_to_add, f.name))

def delete_path_from_config_file(f, path_to_delete):
    try:
        entries = f.readlines()
        f.seek(0)
        for entry in entries:
            if entry != path_to_delete:
                f.write(entry)
        f.truncate()
        f.close()
    except:
        print("Impossible to delete the path {0} from file {1}".format(path_to_delete, f.name))
