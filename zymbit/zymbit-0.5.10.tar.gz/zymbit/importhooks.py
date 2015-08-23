import sys

from zymbit.util import get_system


def get_module_path(fullname):
    system = get_system() or 'common'
    return fullname.replace('.compat.', '.{}.'.format(system))


class CompatLoader(object):
    def load_module(self, fullname):
        module_path = get_module_path(fullname)

        module = __import__(module_path)
        for _module_name in module_path.split(".")[1:]:
            module = getattr(module, _module_name)

        return module


class CompatFinder(object):
    def __init__(self, path_entry):
        if not path_entry.endswith('zymbit/compat'):
            raise ImportError()

    def find_module(self, fullname, path=None):
        return CompatLoader()
sys.path_hooks.append(CompatFinder)
