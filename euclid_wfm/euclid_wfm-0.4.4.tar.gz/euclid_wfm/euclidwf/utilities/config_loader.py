'''
Created on Apr 22, 2015

@author: martin.melchior
'''
import os
from euclidwf.utilities.error_handling import ConfigurationError

def load_config(configfile, configdict={}):
    with open(configfile,'r') as f:
        for line in f:
            line=line.strip()
            if line and not line.startswith("#"):
                itemname, itemvalue = line.split("=")
                itemname=itemname.strip()
                itemvalue=itemvalue.strip()
                if itemvalue in configdict.keys():
                    raise ConfigurationError("Configuration item with name %s already loaded.")
                else:
                    configdict[itemname]=os.path.expandvars(itemvalue)


def load_from_config(config, itemname, fail=True):
    if not itemname in config.keys():
        if fail:
            raise ConfigurationError("Missing config item: %s"%itemname)
        else:
            return None
    else:
        return config[itemname]
