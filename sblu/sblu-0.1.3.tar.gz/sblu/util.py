import os
import stat


class memoize(dict):
    """
    Basic memoizing class, taken from http://wiki.python.org/moin/PythonDecoratorLibrary#Alternate_memoize_as_dict_subclass
    """
    def __init__(self, func):
        self.func = func
        self.memoized = {}

    def __call__(self, *args):
        return self[args]

    def __missing__(self, key):
        result = self[key] = self.func(*key)
        return result


def is_pipe(file_obj):
    return stat.S_ISFIFO(os.fstat(file_obj.fileno()).st_mode)


def add_atom_selection_arguments(parser):
    parser.add_argument("--only-CA", action="store_true", default=False,
                        help="Only use C-alpha atoms.")
    parser.add_argument("--only-backbone", action="store_true", default=False,
                        help="Only use backbone atoms.")
    parser.add_argument("--only-selection", default=None,
                        help="Use ProDy selection to select atoms.")

    return parser


def _is_string_like(obj):
    """
    Check whether obj behaves like a string.
    """
    try:
        obj + ''
    except (TypeError, ValueError):
        return False
    return True

