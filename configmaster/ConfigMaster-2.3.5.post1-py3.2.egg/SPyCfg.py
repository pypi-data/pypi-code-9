# Simple Python Config file parser

import copy

from configmaster.ConfigGenerator import GenerateConfigFile, GenerateNetworkedConfigFile


def construct(data, sandbox=True):
    # Two dicts for locals and globals.

    nloc = copy.copy(locals())
    nglob = copy.copy(globals())

    if sandbox:
        # Delete builtins
        del nglob["__builtins__"]

    # Attempt to execute the config file.
    exec(data, locals=nloc, globals=nglob)

    # Fuck globals!
    del nglob

    ndict = {}

    # Convert locals into a dict structure.
    for key, value in nloc.items():
        ndict[key] = value

    return ndict


def load_hook(is_net: bool=False, **kwargs):
    def actual_load_hook(cfg):

        if 'sandbox' in kwargs:
            sandbox = kwargs['sandbox']
        else:
            sandbox = True

        if not is_net:
            data = construct(cfg.fd.read(), sandbox)
        else:
            data = construct(cfg.request.text, sandbox=True)

        cfg.config.load_from_dict(data)

    return actual_load_hook


JSONConfigFile = GenerateConfigFile(load_hook=load_hook(False), dump_hook=None, json_fix=True)
NetworkedJSONConfigFile = GenerateNetworkedConfigFile(load_hook=load_hook(True),
                                                      normal_class_load_hook=load_hook(False),
                                                      normal_class_dump_hook=None)
