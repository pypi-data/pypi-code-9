from . import JSONConfigFile, INIConfigFile, SPyCfg

try:
    from . import YAMLConfigFile
except ImportError:
    YAMLConfigFile = lambda x : ImportError("You have not installed the PyYAML library. Install it via `pip install PyYAML`.")
