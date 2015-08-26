from . import JSONConfigFile, INIConfigFile, SPyCfg

from .exc import FiletypeNotSupportedException

try:
    from . import YAMLConfigFile
except FiletypeNotSupportedException:
    YAMLConfigFile = lambda x : ImportError("You have not installed the PyYAML library. Install it via `pip install PyYAML`.")
