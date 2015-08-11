from os.path import expanduser, join


def port_path():
    return join(expanduser("~"), ".asdb_port")
