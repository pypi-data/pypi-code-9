##
# (c) 2009-2013 Yannick Versley / University of Tuebingen
# (c) 2015 Yannick Versley / University of Heidelberg
##
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License.  You may obtain
# a copy of the License at
##
# http://www.apache.org/licenses/LICENSE-2.0
##
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  See the
# License for the specific language governing permissions and limitations
# under the License.

import sys

__all__ = ['Factory']

config_obj = None


def get_config():
    global config_obj
    if config_obj is None:
        # TODO have some mechanism to load appropriate config file(s)
        config_obj = {}
    return config_obj


class InterpolationDict(dict):
    '''
    a dict subclass that can pull values out of a parent object's
    attributes or some global configuration.
    '''

    def __init__(self, d, parent_obj):
        dict.__init__(self, d)
        self.parent_obj = parent_obj

    def __missing__(self, k):
        if hasattr(self.parent_obj, k):
            return getattr(self.parent_obj, k)
        elif k[0] == '_':
            vals = k.split('.')
            return self.parent_obj.get(vals[0][1:], *vals[1:])
        if k[0] == '$':
            idx = k.index('.')
            return get_config().get(k[1:idx], k[idx + 1:])


class Factory:

    '''
    a configurable object that performs caching of
    computed objects and on-demand loading:

    By providing a *load_xxx* method, a subclass of
    Factory declares something that can be loaded or
    computed. The :method:`get` method then either
    retrieves a value or computes/loads it via the
    corresponding *load_xxx* method.

    Initialization keyword arguments are added as properties of
    the object. Filename patterns can refer to properties
    of the object as ``%(keyname)s`` or similar, which then
    get instantiated by open_by_pat or fname_by_pat.
    '''

    def __init__(self, **properties):
        self.__dict__.update(properties)

    def bind(self, **kwargs):
        '''
        creates a copy of the object without the
        cached results and with the given keyword
        arguments as properties.
        '''
        d = dict(self.__dict__)
        for k in d.keys():
            if k[0] == '_':
                del d[k]
            elif k.startswith('obj_'):
                d[k] = d[k].bind(**kwargs)
        d.update(kwargs)
        return self.__class__(**d)

    def get(self, name, *subkey):
        """
        retrieves a data item, or loads it if it
        is not present.
        """
        if subkey == []:
            return self.get_atomic(name)
        else:
            return self.get_subkey(name, tuple(subkey))

    def val(self, name):
        """
        retrieves a value, substituting actual
        values for ConfigValue templates.
        """
        v = getattr(self, name)
        if hasattr(v, 'retrieve_value'):
            v = v.retrieve_value(self.__dict__)
        return v

    def get_atomic(self, name):
        if not hasattr(self, '_' + name):
            f = getattr(self, 'load_' + name)
            v = f()
            setattr(self, '_' + name, v)
            return v
        else:
            return getattr(self, '_' + name)

    def get_subkey(self, name, subkey):
        if not hasattr(self, '_' + name):
            d = {}
            setattr(self, '_' + name, d)
        else:
            d = getattr(self, '_' + name)
        if subkey in d:
            return d[subkey]
        else:
            f = getattr(self, 'load_' + name)
            v = f(*subkey)
            d[subkey] = v
            return v

    def open_by_pat(self, name, mode='r', **kwargs):
        '''
        opens the file for the pattern given by *name*,
        substituting the object's properties and the
        additional keyword arguments given.
        '''
        fname = self.fname_by_pat(name, **kwargs)
        if mode == 'w':
            print >>sys.stderr, "Write[%s]: %s" % (name, fname)
        else:
            print >>sys.stderr, "Open[%s]: %s" % (name, fname)
        return file(fname, mode)

    def fname_by_pat(self, name, **kwargs):
        # fmt is either a string to interpolate
        # or a ConfigValue
        fmt = getattr(self, name + '_pattern')
        d = InterpolationDict(kwargs, self)
        fname = fmt % d
        return fname


class ContextStack:

    '''
    allows to have "dynamic binding"-like behaviour
    Usage:
    1) with ctx.push('x',10):
        do_something
       adds a new context stack item, with the specified variable
    2) ctx['var']=10
       sets the value to the specified value, which will
       hold until the next context pop
    3) ctx['var']
       gets the value for that context
    4) ctx.pop():
       undoes the effect of ctx.push() if not in a 'with' construct
    '''

    def __init__(self, d_init=None):
        if d_init is None:
            self.d = {}
        else:
            self.d = dict(self.d_init)
        self.c = [[]]

    def push(self, *vars):
        nc = []
        self.c.append(nc)
        for i in xrange(0, len(vars), 2):
            k = vars[i]
            v = vars[i + 1]
            nc.append([k, self.d.get(k, None)])
            self.d[k] = v
        return self

    def __enter__(self):
        pass

    def __exit__(self, x, y, z):
        self.pop()

    def pop(self):
        nc = self.c.pop()
        for k, v in nc[::-1]:
            if v is None:
                del self.d[k]
            else:
                self.d[k] = v

    def __getitem__(self, k):
        return self.d.get(k, None)

    def __setitem__(self, k, v):
        nc = self.c[-1]
        nc.append([k, self.d.get(k, None)])
        self.d[k] = v
