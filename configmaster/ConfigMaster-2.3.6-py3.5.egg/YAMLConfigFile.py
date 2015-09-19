from configmaster import exc

try:
    import yaml
    import yaml.scanner
except ImportError:
    raise exc.FiletypeNotSupportedException(
        "You have not installed the PyYAML library. Install it via `pip install PyYAML`.")

from configmaster.ConfigFile import ConfigFile, NetworkedConfigObject

from configmaster.ConfigGenerator import GenerateConfigFile, GenerateNetworkedConfigFile


def cload_safe(fd):
    """
    Wrapper for the YAML Cloader.
    :param fd: The file descriptor to open.
    :return: The YAML dict.
    """
    return yaml.load(fd, Loader=yaml.CSafeLoader)


def cload_load(fd):
    """
    Wrapper for the YAML Cloader.
    :param fd: The file descriptor to open.
    :return: The YAML dict.
    """
    return yaml.load(fd, Loader=yaml.CLoader)


def yaml_load_hook(load_net: False, **kwargs):
    def actual_load_hook(cfg: ConfigFile):
        """
        This handles automatically opening/creating the YAML configuration files.

        >>> import configmaster.YAMLConfigFile
        >>> cfg = configmaster.YAMLConfigFile.YAMLConfigFile("test.yml") # Accepts a string for input

        >>> fd = open("test.yml") # Accepts a file descriptor too
        >>> cfg2 = configmaster.YAMLConfigFile.YAMLConfigFile(fd)

        ConfigMaster objects accepts either a string for the relative path of the YAML file to load, or a :io.TextIOBase: object to read from.
        If you pass in a string, the file will automatically be created if it doesn't exist. However, if you do not have permission to write to it, a :PermissionError: will be raised.

        To access config objects programmatically, a config object is exposed via the use of cfg.config.
        These config objects can be accessed via cfg.config.attr, without having to resort to looking up objects in a dict.

        >>> # Sample YAML data is abc: [1, 2, 3]
        ... print(cfg.config.abc) # Prints [1, 2, 3]

        ConfigMaster automatically uses YAML's CLoader/CSafeLoader and CDumper for speed performances.

        By default, all loads are safe. You can turn this off by passing safe_load as False.
        However, you must remember that these can construct **ANY ARBITRARY PYTHON OBJECT**. Make sure to verify the data before you unsafe load it.
        """
        # Should we safe load the file using YAML's Safe loader?
        # This is always on by default, for security reasons.
        if cfg.safe_load:
            # Assign 'loader' to the safe YAML CSafeLoader.
            if yaml.__with_libyaml__:
                loader = cload_safe
            else:
                loader = yaml.safe_load
        # Otherwise, use the YAML CLoader.
        else:
            if yaml.__with_libyaml__:
                loader = cload_load
            else:
                loader = yaml.load
        # Setup dumper.
        if yaml.__with_libyaml__:
            cfg.dumper = yaml.CDumper
        else:
            cfg.dumper = yaml.Dumper
        # Load the YAML file.
        try:
            if not load_net:
                data = loader(cfg.fd)
            elif load_net and isinstance(cfg, NetworkedConfigObject):
                data = loader(cfg.request.text)
            else:
                raise exc.LoaderException("No data source to load from.")
        except UnicodeDecodeError as e:
            raise exc.LoaderException("Selected file was not in a valid encoding format.") from e
        except yaml.scanner.ScannerError as e:
            raise exc.LoaderException("Selected file had invalid YAML tokens.") from e
        # Serialize the data into new sets of ConfigKey classes.
        cfg.config.load_from_dict(data)
    return actual_load_hook


def yaml_dump_hook(cfg, text: bool=False):
    """
    Dumps all the data into a YAML file.
    """

    data = cfg.config.dump()
    if not text:
        yaml.dump(data, cfg.fd, Dumper=cfg.dumper, default_flow_style=False)
    else:
        return yaml.dump(data, Dumper=cfg.dumper, default_flow_style=False)



YAMLConfigFile = GenerateConfigFile(load_hook=yaml_load_hook(False), dump_hook=yaml_dump_hook)
NetworkedYAMLConfigFile = GenerateNetworkedConfigFile(load_hook=yaml_load_hook(True),
                                                      normal_class_load_hook=yaml_load_hook(False),
                                                      normal_class_dump_hook=yaml_dump_hook)