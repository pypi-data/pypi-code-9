import getpass
from configobj import ConfigObj

from path import path


DEFAULTS = {
    "cluspro": {
        "local_path": None
    },
    "ftmap": {
        "local_path": None
    },
    "scc": {
        "hostname": "scc1.bu.edu",
        "username": getpass.getuser()
    }
}


def get_config():
    config = ConfigObj(DEFAULTS)

    config_file = path("~/.sblurc").expand()
    if config_file.exists():
        config.merge(ConfigObj(config_file))
    else:
        config.filename = config_file
        config.write()

    return config
