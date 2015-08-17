# coding: utf-8

# NOTE: Keep a simple versioning scheme, this program is not that complex
# http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers
# https://pythonhosted.org/setuptools/setuptools.html#specifying-your-project-s-version
__version__ = '0.1.0'

__main_author_name__ = 'Pablo Figue'
__main_author_email__ = 'pfigue posteo de'
__authors__ = (
    '%s <%s>' % (__main_author_name__, __main_author_email__),
)
__license__ = 'MIT'
__program_name__ = 'hex2words'
__short_description__ = 'Hexadecimal ID/Fingerprint to PGP-words list converter'
__url__ = 'https://bitbucket.org/pfigue/hex2words'




def get_platform_id():
    '''Returns a string with the description of the platform.

E.g.:
    Linux-3.8.1-1-mainline; x86_64-64bit; CPython-3.4.3
'''
    import platform
    msg = '{platform}; {arch}; {python_implementation}-{python_version}'
    msg = msg.format(
        platform=platform.system() + '-' + platform.release(),
        arch=platform.machine() + '-' + platform.architecture()[0],
        python_implementation=platform.python_implementation(),
        python_version=platform.python_version(),
    )
    del(platform)
    return msg
