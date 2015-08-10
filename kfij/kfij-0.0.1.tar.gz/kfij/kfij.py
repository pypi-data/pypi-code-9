import os
from copy import copy
from functools import wraps

def unlocked(func):
    @wraps(func)
    def f(self, *args, **kwargs):
        if getattr(self, '_force', False) or (not getattr(self, '_lock', False)):
            return func(self, *args, **kwargs)
        else:
            raise EnvironmentError('%s is locked' % repr(self))
    return f

def lock(func):
    @wraps(func)
    @unlocked
    def f(self, *args, **kwargs):
        original = copy(getattr(self, '_lock', None))
        output = func(self, *args, **kwargs)
        if original != None:
            self._lock = original
        return output
    return f

class Kfij:
    '''
    Persist objects of an existing class to a file. It is safe to access the same
    instance from multiple threads. It is unsafe to get any more concurrent than that.

    Use the enable_safe_funcs and enable_destructive_funcs to stupidly copy methods
    from the class that you are persisting. The safe functions should not update the
    present object. The destructive functions should update the present object, and
    they rewrite the entire corresponding file every time they are called.

    You probably don't need to rewrite the entire file every time, so you should
    write your own versions of functions that don't need to do this.
    '''
    @unlocked
    def __init__(self, filename, *args, **kwargs):
        '''
        If the filename exists, *args and **kwargs must be empty.

        If the filename exists, the new object is populated with the
        data in the file.

        If *args and **kwargs are set, they get passed to self.factory,
        and the result overwrites the contents of the file.

        Either way, updates to the new object flow to the file.

        :param str filename: File at which to save state
        :raises EnvironmentError: If the file already exists and any *args or **kwargs are set
        '''
        if os.path.exists(filename) and len(args) + len(kwargs) > 0:
            raise EnvironmentError('If the file already exists, no *args or **kwargs may be set.')

        self.cache = self.factory(*args, **kwargs)
        self._fp = open(filename, 'a')

        self._force = True
        if os.path.exists(self._fp.name):
            self.load()
        else:
            self.dump()
        self._force = False

    def readlines(self):
        out = []
        with open(self._fp.name, 'r') as fp:
            for line in fp:
                out.append(line.rstrip('\r\n'))
        return out

    def writelines(self, lines):
        '''
        Write a line to the file

        :param iter lines: Iterable of str lines to be written
        :raises NotImplementedError: If the line contains carriage return or newline
        '''
        for text in lines:
            if not isinstance(text, str) or '\r' in text or '\n' in text:
                raise NotImplementedError('Can\'t handle this sort of value')
            self._fp.write(text + '\n')
        self._fp.flush()

    @staticmethod
    def factory(*args, **kwargs):
        '''
        You must set the factory equal to the class that the present class is mimicing, such as set or list.
        '''
        raise NotImplementedError('You must set the %s.kfij_factory.', self.__class__.__name__)

    def load(self):
        '''
        This must be a static method that takes a file pointer, parses the format created by
        the dump function, and updates the present object with the data from the file. Assume
        that the present object is empty before load is called.
        '''
        raise NotImplementedError('You must set %s.load.', self.__class__.__name__)

    def dump(self):
        '''
        You must set this to the function to a function that serializes the present
        object in a form that the load function can parse.
        '''
        raise NotImplementedError('You must set %s.dump.', self.__class__.__name__)

    @classmethod
    def enable_destructive_funcs(Class, *func_names):
        for func_name in func_names:
            _enable_destructive_func(Class, str(func_name))

    @classmethod
    def enable_safe_funcs(Class, *func_names):
        for func_name in func_names:
            _enable_safe_func(Class, str(func_name))

def _enable_destructive_func(Class, func_name):
    @wraps(getattr(Class.factory, func_name))
    @lock
    def func(self, *args, **kwargs):
        self._fp.close()
        os.remove(self._fp.name)

        output = getattr(self.cache, func_name)(*args, **kwargs)

        self._fp = open(self._fp.name, 'a')
        self.dump()

        return output
    setattr(Class, func_name, func)

def _enable_safe_func(Class, func_name):
    @wraps(getattr(Class.factory, func_name))
    @unlocked
    def func(self, *args, **kwargs):
        return getattr(self.cache, func_name)(*args, **kwargs)
    setattr(Class, func_name, func) 
