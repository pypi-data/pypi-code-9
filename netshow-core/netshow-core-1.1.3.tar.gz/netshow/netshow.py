# pylint: disable=E1102
""" Netshow core module """
import netshowlib.netshowlib as nn
from netshowlib import _version
import os
import sys
import gettext
import pkg_resources

class UnableToFindProviderException(Exception):
    """
    Exception when Provider is not Found
    """
    pass


def run():
    """
    Executes ``run()`` function from netshow plugin identified
    from the provider check.
    """
    # set the LOCPATH to find locale files in the virtualenv instance or
    # system /usr/share/locale location. needed by gettext
    # for translation files.
    os.environ['LOCPATH'] = os.path.join(sys.prefix, 'share', 'locale')
    if os.environ.get('LANGUAGE') == 'C':
        os.environ['LANGUAGE'] = 'en'
    _ostype = nn.provider_check()
    if not _ostype:
        raise UnableToFindProviderException
    import_str = 'netshow.%s.show' % _ostype
    nn.import_module(import_str).run()


def i18n_app(providername):
    """
    import this function at the top of each provider netshow component
    that has cli output  functions. Example

    from netshow.netshow import i18n_app as _
    """
    install_location = pkg_resources.require('netshow-core-lib')[0].location
    translation_loc = os.path.join(install_location, '..', '..', '..', 'share', 'locale')

    _translate = gettext.translation(providername, translation_loc,
                                     fallback=True)

    return _translate.lgettext

def print_version():
    version = _version.get_version()
    version_str = "Netshow Version:\n"
    for _k, _v in version.items():
         version_str += "%s: %s\n" % (_k, _v)
    return version_str
