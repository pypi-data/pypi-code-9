
# If a user passes in an argument of another it will try to
# cast the argument to the desired type.
# Not sure if this is a useful or smart thing to have at all, just made
# for fun

from functools import wraps


#########################################################
# _correct_type, _multi_type_fix and _single_type_fix   #
# are all meant to be helper functions, they are  not   #
# meant to be used outside this modole                  #
#########################################################

# cast an object to a type if the
# object passed in is not of the same
# type as the type passed in. This might result
# in a ValueError or TypeError.
def _correct_type(obj, _type):
    if type(obj) != _type:
        obj = _type(obj)
    return obj


# Pairs each object and type as tuples in a list,
# then loops through this list and yield each object,
# if possible, after we have made sure the object 
# has the same type as the type in its tuple.
def _multi_type_fix(obj_seq, type_seq):
    zipped = zip(obj_seq, type_seq)
    for obj, _type in zipped:
        yield _correct_type(obj, _type)

# Loops true a sequence of objects and yield
# each object, if possible, after we have made sure
# the object has the same type as the type passed in
# as an argument.
def _single_type_fix(obj_seq, _type):
    for obj in obj_seq:
        yield _correct_type(obj, _type)


def type_corrector(*types):
    """A decorator that casts the parameters of a function to the types
       used as arguments with this decorator"""
    def wrapper(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            _args = _multi_type_fix(args, types) if len(types) > 1 \
                    else _single_type_fix(args, types[0])
            kwargs_values = _multi_type_fix(kwargs.values(), types) if len(types) > 1 \
                    else _single_type_fix(kwargs.values(), types[0])
           
            zipped = zip(kwargs.keys(), kwargs_values)
            for key, value in zipped:
                kwargs[key] = value
                
            return func(*_args, **kwargs)
        return _wrapper
    return wrapper


