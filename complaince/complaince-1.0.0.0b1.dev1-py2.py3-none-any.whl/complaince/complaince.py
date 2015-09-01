from __future__ import print_function
import sys
def param_check(*param_types, **kwargs):
    '''Decorator wich checks if parameters are of required
    types.

    Parameters:
    param_types - Expected types of inputs to the decorated function
           Each type is provided in a tuple, (multiple allowed types per parameter)
    level - Can decide if the result is a warning or error, default 0
        0 - Warning
        1 - Error
    ret (optional) - verify return type of function is also a tuple
    '''
    if not kwargs:
        level = 0
    else:
        level = kwargs['level']
    try:
        def decorator(func):
            '''
            This function has the information of the actual function
            including name, docstring
            '''
            def checker(*params):
                '''The new function with all the passed params
                '''
                if(not len(params) == len(param_types)):
                    raise Exception("For function: %s, %s parameters required %s, given" \
                            % (func.__name__, str(len(param_types)), str(len(params))))
                #errors = 0
                passed_types = tuple(map(type,params))
                for param_no, param_t in enumerate(passed_types):
                    assert (type(param_types[param_no]) == tuple)
                    if param_t not in param_types[param_no]:
                        msg = param_msg(func.__name__,param_no, param_t,param_types[i])
                        if(level == 0):
                            print("Warning: %s" % msg, file = sys.stderr)
                        if(level == 1):
                            raise TypeError(msg)
                if('ret' in kwargs):
                    assert (tuple == type(kwargs['ret']))
                    result = func(*params)
                    if(type(result) in kwargs['ret']):
                        return result
                    else:
                        msg = ret_msg(func.__name__, type(result), kwargs['ret'])
                        if(level == 0):
                            print("Warning: %s" % msg, file = sys.stderr)
                        if(level == 1):
                            raise TypeError(msg)
                else:
                    return func(*params)
            return checker
        return decorator

    except KeyError as keyerr:
        raise KeyError("%s in not a valid key for the decorator" % keyerr)
    except TypeError as typerr:
        raise TypeError(typerr)
    except AssertionError as err:
        raise AssertionError(err)

def ret_msg(function_name, returned_type, actual_types):
    '''Return error message formatting method
    '''
    type_str = "(%s)" % ','.join([a.__name__ for a in actual_types])
    msg = "Function %s should return one %s but returned %s" \
            % (function_name, type_str, "(%s)" % returned_type.__name__)
    return msg
def param_msg(function_name, param_no, passed_type, actual_types):
    '''Parameter error Message formatting method
    '''
    param_no += 1
    type_str = "(%s)" % ','.join([ a.__name__ for a in actual_types])
    msg = "parameter %s for function %s should be one of %s but got %s " \
            % (param_no, function_name, type_str, "(%s)" % passed_type.__name__)
    return msg

if __name__ == '__main__':
    '''Simple standalone Test case
    '''
    @param_check((int,float),(int,float),level = 0, ret=(int,float))
    def func1(a, b):
        #print(str(a+b))
        return a+b
    print(func1(1,2))
    print(func1(1.1,2))
    print(func1(2.2,2.34))
