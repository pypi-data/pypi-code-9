


def get_cls_name(obj):
    if is_a_type(obj): # Is a class, not an object
        return obj.__name__
    return obj.__class__.__name__


def is_a_type(obj):
    if obj.__class__ == type:
        return True
    return False
    

def is_type_of(obj, cls, raise_error=False):
    if isinstance(obj, cls):
        return True
    if raise_error:
        raise TypeError("%s is not derived from %s" % (get_cls_name(obj), get_cls_name(cls)))
    return False




