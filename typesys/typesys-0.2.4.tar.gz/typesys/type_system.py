import inspect
from functools import wraps


########################################################
# Everything that are meant to be used within this     #
# module only is documented with '#', everything else  #
# is documented with docstrings                        #
########################################################


# This is a class to hold the objects and types for type hints.
# Also need the decorated functions name in order to give better
# debug messages when an TypeError is raised. If the decorated function
# has keyword arguments and instance of this class will  also knows 
# the name of these arguments.
class _TypeChecker(object):
    def __init__(self, objects, types, func_name, arg_names=None):
        self.objects = objects
        self.func_name = func_name
        self.types = types
        self.arg_names = arg_names

    # Checks if an object is of the same type as the type passed in,
    # raises TypeError of not.
    def _check_type(self, obj, _type, arg_num=None, arg_name=None):
        if type(obj) != _type:
            if arg_num is not None:
                raise TypeError('Expected {} as argument number {} in function "{}" '\
                    ', but found {}'.format(_type, arg_num, self.func_name, type(obj)))
            raise TypeError('Expected {} as argument "{}" in function "{}" '\
                ', but found {}'.format(_type, arg_name, self.func_name, type(obj)))

    # Loops through the objects and types and checks that they are the same.
    # This is done when a function has "regular" or default arguements, meaning
    # defined as eiter func(x,y) or func(x=None, y=None)
    def multi_type_check(self):
        # default arguements goes here
        if self.arg_names:
            zipped = zip(self.objects, self.types, self.arg_names)
            for obj, _type, arg_name in zipped:
                self._check_type(obj, _type, arg_name=arg_name)
        # Regular arguments goes here
        else:
            zipped = zip(self.objects, self.types)
            for count, (obj, _type) in enumerate(zipped):
                self._check_type(obj, _type, arg_num=count)
    
    # Loops through the objects and check that it is of one of the types from
    # types.
    # This is used when a function has been defined with an arbitrary number of
    # of arguments (*args) or keyword arguemnts (**kwargs)
    def args_type_check(self):
        # **kwargs goes here
        if self.arg_names:
            data = zip(self.objects, self.arg_names)
            for obj, arg_name in data:
                if type(obj) not in self.types:
                    raise TypeError('Expected one of these types {} as argument '\
                            '"{}" in function {}, but found {}'.format(self.types, arg_name, self.func_name, type(obj)))
        # *args goes here
        for count, obj in enumerate(self.objects):
            if type(obj) not in self.types:
                raise TypeError('Expected one of these types {} as argument '\
                        'number {} in function {}, but found {}'.format(self.types, count, self.func_name, type(obj)))

                                
# cast an object to a type if the
# object passed in is not of the same
# type as the type passed in. This might result
# in a ValueError or TypeError.
def _correct_type(obj, _type):
    if type(obj) != _type:
        obj = _type(obj)
    return obj


# Generates all objects of the desired type
# found in the types sequence
def _multi_type_fix(obj_seq, type_seq):
    zipped = zip(obj_seq, type_seq)
    for obj, _type in zipped:
        yield _correct_type(obj, _type)


# Generates all objects of the desired type
# passed in as _type
def _single_type_fix(obj_seq, _type):
    for obj in obj_seq:
        yield _correct_type(obj, _type)


#####################################
# Below are the actual decorators   #
#####################################


def type_corrector(*types):
    """A decorator that casts the parameters of a function to the types
       used as arguments with this decorator. If the decorated function
       have *args and/or **kwargs as its paramenters the user only need
       to specify one type as arguments to this decorator."""
    def wrapper(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            args_types = types[0:len(types)]
            kw_types = types[len(args):len(args)]
            args = _multi_type_fix(args, args_types) if len(args_types) > 1 \
                    else _single_type_fix(args, types[0])
            kwargs_values = _multi_type_fix(kwargs.values(), kw_types) if len(kw_types) > 1 \
                    else _single_type_fix(kwargs.values(), types[0])
           
            data = zip(kwargs.keys(), kwargs_values)
            for name, value in data:
                kwargs[name] = value
                
            return func(*args, **kwargs)
        return func_wrapper
    return wrapper


def type_hints(*types):
    """Decorator used for type hints. If case of TypeError the code inside the
       decorated function will not be executed, meaning the function will return
       None if it has any return statements.
       Usage:"""
    def wrapper(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            try:
                arg_types = types[0:len(args)]
                kw_types = types[len(args):len(types)]
                args_checker = _TypeChecker(args, arg_types, func.__name__)
                kwargs_checker = _TypeChecker(kwargs.values(), 
                                              kw_types, func.__name__, 
                                              arg_names=kwargs.keys())
                
                if inspect.getargspec(func).args and args:
                    args_checker.multi_type_check()
                if inspect.getargspec(func).defaults:
                    kwargs_checker.multi_type_check()
                if inspect.getargspec(func).varargs:
                    args_checker.args_type_check()
                if inspect.getargspec(func).keywords:
                    kwargs_checker.args_type_check()
                
                return func(*args, **kwargs)
            except TypeError as te:
                print('TypeError: {}'.format(te))
        return func_wrapper
    return wrapper


def return_type(*types):
    """Decorator that makes sure a function returns the correct type. When a function
       is decoratred with this decorator the programmer may specify several return
       types that are valid return types for the decorated function"""
    def wrapper(func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            try:
                ret_val = func(*args, **kwargs)
                if type(ret_val) not in types:
                    raise TypeError('TypeError: {} was expected to return one of these {} '\
                        'but returned {}'.format(func.__name__, types, type(ret_val)))
                else:
                    return ret_val   
            except Exception as e:
                print(e) 
        return func_wrapper
    return wrapper


