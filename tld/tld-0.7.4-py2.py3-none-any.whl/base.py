__title__ = 'tld'
__version__ = '0.8'
__build__ = 0x00000e
__author__ = 'Artur Barseghyan'
__copyright__ = '2013-2015 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('BaseTLDSource',)

class BaseTLDSource(object):
    """
    Base TLD source.
    """
    uid = None
