__author__ = 'jc'
"""
Shamelessly stolen code from the pyramid_jinja2 package
used to find the name of the module which is calling my module
which is then used to find all of their modules again.
And all this so that I can figure out the imported database object

Please note the included License (pyramid_jinja2_LICENSE.txt) file which is inlcuded as required.
Pyramid_jinja2 authors neither endorse or garantee the use of thier code in this manner.
"""

import inspect
import sys

class _PackageFinder(object):
    inspect = staticmethod(inspect)

    def caller_package(self, excludes=()):
        """A list of excluded patterns, optionally containing a `.` suffix.
        For example, ``'pyramid.'`` would exclude exclude ``'pyramid.config'``
        but not ``'pyramid'``.
        """
        f = None
        for t in self.inspect.stack():
            f = t[0]
            name = f.f_globals.get('__name__')
            if name:
                excluded = False
                for pattern in excludes:
                    if pattern[-1] == '.' and name.startswith(pattern):
                        excluded = True
                        break
                    elif name == pattern:
                        excluded = True
                        break
                if not excluded:
                    break

        if f is None:
            return None

        pname = f.f_globals.get('__name__') or '__main__'
        m = sys.modules[pname]
        f = getattr(m, '__file__', '')
        if (('__init__.py' in f) or ('__init__$py' in f)):  # empty at >>>
            return m

        pname = m.__name__.rsplit('.', 1)[0]

        return sys.modules[pname]


_caller_package = _PackageFinder().caller_package