


def get_cls_name(obj):
    if obj.__class__ == type: # Is a class, not an object
        return obj.__name__
    return obj.__class__.__name__


def is_type_of(obj, cls, raise_error=False):
    if isinstance(obj, cls):
        return True
    if raise_error:
        raise TypeError("%s is derived from %s" % (get_cls_name(obj), get_cls_name(cls)))
    return False




