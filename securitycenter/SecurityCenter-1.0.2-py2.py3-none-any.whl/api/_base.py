from functools import wraps
from ..util import PagedResult


class Module(object):
    """API module that knows how to perform actions.

    :param sc: SecurityCenter connection
    """

    #: sc internal name of module
    _name = ''

    def __init__(self, sc):
        self._sc = sc

    def _request(self, action, input=None, file=None, parse=True, page_class=PagedResult):
        """Make an API call to action under the current module.

        :param action: name of action in module
        :param input: any arguments to be passed to the module::action
        :type input: dict
        :param file: file data to upload
        :type file: file
        :param parse: if False, don't parse response as JSON
        :return: dict containing API response, or ``Response`` if parse is False
        """

        return self._sc._request(self._name, action, input, file, parse=parse, page_class=page_class)


def extract_value(key=Ellipsis, default=Ellipsis):
    """Extract the value of a key from a returned dict.

    Creates a decorator that will get the value of a key from a function
    returning a dictionary.

    Call the function with the ``_key`` argument, or set the ``_key`` key of
    the result dict, to change what value will be extracted.  Set
    ``_key=None`` to return the entire result.  The ``_key`` argument takes
    priority over the ``_key`` key.

    :param key: key to get from return
    :param default: if set, return this if key is not present, otherwise raise KeyError
    :raise KeyError: if key not in dict and no default
    :return: extracted value
    """

    def decorator(f):
        @wraps(f)
        def inner(*args, **kwargs):
            pre_key = kwargs.pop('_key', key)
            res = f(*args, **kwargs)
            post_key = res.pop('_key', None)
            real_key = post_key if pre_key is Ellipsis else pre_key

            if real_key is None:
                return res

            return res.get(real_key) if default is Ellipsis else res.get(real_key, default)

        return inner

    return decorator
