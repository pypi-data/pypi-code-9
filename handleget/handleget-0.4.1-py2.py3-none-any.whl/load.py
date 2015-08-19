"""
# handleget sourcecode -- please see handleget/readme.md
## src/load.py
This file's is a container for the FileHandler object -- which manages all
transactions between handleget and the users files.

To help manage multi-OS setups paths should be loaded safetly using pathlib and
should be thoroughly errorchecked.

Note that all file outputs should be stored here as general python. That means
properly loading and handling any JSON.
"""
import pathlib
import re
import json
import click
import yaml


def get_rootdir():
    # since it's a file path we need to get the second parent
    rootdir = pathlib.Path(__file__).parents[1]
    return rootdir


def load_config(path):
    """
    Load handleget config yml file

    Handled outside of the FileHandler object because any argument can be
    overwritten by this config -- this means it must be loaded before any other
    object has been initalized.
    """
    # Default Configuration, in case config.yml can't be opened or is corrupt
    default_config = """
    override_flags: No
    verbose: Yes
    strip: Yes
    char_pattern: r"([^a-zA-Z0-9_]*)"
    """
    if path == '':
        conf_path = pathlib.Path(str(get_rootdir()), 'data', 'config.yml')
    else:
        conf_path = pathlib.Path(path)

    if conf_path.is_file() == False:
        click.echo('config invalid, using defaults')
        yaml_string = default_config
    else:
        yaml_string = ""
        with conf_path.open() as f:
            yaml_string = f.read()

    config = yaml.load(yaml_string)
    return config


class FileHandler(object):
    """
    This class manages all transactions between handleget and files.
    """
    def __init__(self, error_handler, verbose=False, rootdir=None):
        """
        Initiate the FileHandler object.

        FileHandler(error_handler, strip_illegial_chars, illegial_characters_pattern)

        Arguments and expected types:
        - error_handler: an ErrorHandler class as defiend in src/error.py
        """
        self.error_handler = error_handler
        self.verbose = verbose
        self.rootdir = get_rootdir()

    def _unpack_services(self, services):
        """
        Services are currently passed into the program as a single string,
        with each service split by a comma.
        """
        return services.split(',')

    def load_services(self, services):
        services_wanted = self._unpack_services(services)
        service_path = pathlib.Path(self.rootdir, 'data', 'services')
        services = []
        for child in service_path.iterdir():
            with child.open() as f:
                try:
                    tmp = yaml.load(f.read())
                    if tmp['name'] in services_wanted:
                        services.append(tmp)
                    elif tmp['shortname'] in services_wanted:
                        services.append(tmp)
                except:
                    self.error_handler.catch_invalid_service('', child.name)
        return services
