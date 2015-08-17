import os
import sys
import warnings

try:
    import requests

    _has_network = True
except ImportError:
    _has_network = False
    warnings.warn("Cannot use networked config support. Install requests to enable it.", ImportWarning)

# Hack for Python3.2 and below
if sys.version_info[1] <= 2:
    FileNotFoundError = IOError

from configmaster import ConfigKey
from configmaster import exc

def networked_dump_hook(*args, **kwargs):
    raise exc.NetworkedFileException("Cannot write to a networked file.")

class ConfigObject(object):
    """
    The abstract base class for a Config object.

    All types of config file extend from this.

    This provides several methods that don't need to be re-implemented in sub classes.

    Notes:
        - This provides an access to the data to load via a self.data attribute.
        - Need to call the load/dump hooks? Get them via load_hook or dump_hook.
    """

    def __init__(self, safe_load: bool=True, load_hook=None, dump_hook=None, **kwargs):
        self.safe_load = safe_load
        self.load_hook = load_hook
        self.dump_hook = dump_hook
        self.config = ConfigKey.ConfigKey(safe_load)
        self.data = None

    def dumps(self) -> str:
        """
        Abstract dump to string method.
        """
        raise NotImplementedError

    def dumpd(self) -> dict:
        """
        Dump config data to a dictionary.
        """
        return self.config.dump()

    def load(self, **kwargs):
        """
        This loads the config file using the hook provided. The ConfigObject object is passed in as argument one.
        """
        return self.load_hook(self, **kwargs)

    def dump(self):
        """
        This dumps the config file using the hook provided. The ConfigObject is passed in as argument one.
        """
        return self.dump_hook(self)

    def initial_populate(self, data):
        """
        Populate a newly created config object with data.

        If it was populated, this returns True. If it wasn't, this returns False.

        It is recommended to run a .dump() and .reload() after running this.
        """
        if self.config.parsed:
            return False
        # Otherwise, create a new ConfigKey.
        self.config.load_from_dict(data)
        return True

    def apply_defaults(self, other_config):
        """
        Applies default values from a different ConfigObject or ConfigKey object to this ConfigObject.

        If there are any values in this object that are also in the default object, it will use the values from this object.
        """
        if isinstance(other_config, self.__class__):
            self.config.load_from_dict(other_config.config, overwrite=False)
        else:
            self.config.load_from_dict(other_config, overwrite=False)


class ConfigFile(ConfigObject):
    """
    The abstract base class for a ConfigFile object. All config files extend from this.

    It automatically provides opening of the file and creating it if it doesn't exist, and provides a basic reload() method to automatically reload the files from disk.
    """

    def __init__(self, fd: str, load_hook=None, dump_hook=None, safe_load: bool=True, json_fix: bool=False, **kwargs):
        super().__init__(safe_load, load_hook=load_hook, dump_hook=dump_hook)
        # Check if fd is a string
        if isinstance(fd, str):
            self.path = fd.replace('/', '.').replace('\\', '.')
            # Open the file.
            try:
                fd = open(fd)
            except FileNotFoundError:
                # Make sure the directory exists.
                if not os.path.exists('/'.join(fd.split('/')[:-1])) and '/' in fd:
                        os.makedirs('/'.join(fd.split('/')[:-1]))
                if not json_fix:
                    # Open it in write mode, and close it.
                    open(fd, 'w').close()
                else:
                    # Open it in write mode, write "{}" to it, and close it.
                    with open(fd, 'w') as f: f.write("{}")
                fd = open(fd, 'r')
        else:
            self.path = fd.name.replace('/', '.').replace('\\', '.')
        self.fd = fd

        def _dump(*args, **kwargs):
            raise exc.FiletypeNotSupportedException("YAML Dumper not loaded - hook not called?")

        self.dumper = _dump

        self.data = self.fd.read()
        self.fd.seek(0)
        self.load(**kwargs)

    def dump(self):
        # RE-open the file in 'w' mode.
        if not self.fd.writable():
            name = self.fd.name
            self.fd.close()
            self.fd = open(name, 'w')

        # Call the dump hook.
        self.dump_hook(self)

        # RE-open the file in 'r' mode.
        name = self.fd.name
        self.fd.close()
        self.fd = open(name, 'r')

    def dumps(self):
        """
        Dump config data to string.

        This uses a StringIO virtual file, to ensure compatibility with dump hooks that use file-based dumping.
        """
        return self.dump_hook(self, True)

    def reload(self):
        """
        Automatically reloads the config file.

        This is just an alias for self.load()."""

        if not self.fd.closed: self.fd.close()

        self.fd = open(self.fd.name, 'r')
        self.load()


class NetworkedConfigObject(ConfigObject):
    """
    An abstract Networked Config object.

    This is commonly used for downloading "default" config files, and applying them to real config files.
    """

    def __init__(self, url: str, normal_class_load_hook, normal_class_dump_hook, load_hook, safe_load: bool=True,
                 **kwargs):
        if _has_network is False:
            raise exc.NetworkedFileException("Requests is not installed.")

        self.url = url
        # Try and get url.
        try:
            self.request = requests.get(self.url)
        except requests.exceptions.ConnectionError as e:
            raise exc.NetworkedFileException("Failed to download file: {}".format(e))

        if self.request.status_code != 200:
            raise exc.NetworkedFileException("Failed to download file: Status code responded was {}".format(self.request.status_code))

        super().__init__(safe_load=safe_load, load_hook=load_hook)

        self.normal_class_hook = (normal_class_load_hook, normal_class_dump_hook)

        self.data = self.request.text

        self.load(**kwargs)

    def dump(self):
        raise exc.NetworkedFileException("Cannot write to a networked file.")

    def initial_populate(self, data):
        raise exc.NetworkedFileException("Cannot write to a networked file.")

    def save_to_file(self, filename: str) -> ConfigFile:
        """
        This converts the NetworkedConfigFile into a normal ConfigFile object.

        This requires the normal class hooks to be provided.
        """
        newclass = ConfigFile(fd=filename, load_hook=self.normal_class_hook[0],
                              dump_hook=self.normal_class_hook[1], safe_load=self.safe_load)
        return newclass
