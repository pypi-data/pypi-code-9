__version__ = '0.3.55555'
__all__ = ['countdown', 'decorators', 'system', 'tables', 'ipy']
try:
    from . import *
except ImportError:
    pass  # imports will fail during dependency collection
