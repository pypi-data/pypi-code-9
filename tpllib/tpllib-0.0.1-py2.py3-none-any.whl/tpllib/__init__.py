"""
A library with jupyter nbconvert templates
"""

__version__ = '0.0.1'


class LazyTPL(object):

    def __getattr__(self, name):
        pass

        with open('{}.tpl'.format(name)) as f : 
            return f.read()




templates = LazyTPL()
