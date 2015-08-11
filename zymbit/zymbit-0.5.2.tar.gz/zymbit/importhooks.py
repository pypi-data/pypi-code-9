import sys

from zymbit.util import get_system


class CompatLoader(object):
    def load_module(self, fullname):
        system = get_system()
        system_name = fullname.replace('.compat.', '.{}.'.format(system))

        module = __import__(system_name)
        for _module_name in system_name.split(".")[1:]:
            module = getattr(module, _module_name)

        return module


class CompatFinder(object):
    def __init__(self, path_entry):
        if not path_entry.endswith('zymbit/compat'):
            raise ImportError()

    def find_module(self, fullname, path=None):
        return CompatLoader()
sys.path_hooks.append(CompatFinder)
