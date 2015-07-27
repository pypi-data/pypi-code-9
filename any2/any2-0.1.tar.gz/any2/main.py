# -*- encoding: utf-8 -*-


def recursive_getattr(obj, attr, default_value=None):
    if hasattr(obj, attr):
        return getattr(obj, attr)

    if '.' not in attr:
        return default_value

    newattr, tail = attr.split('.', 1)

    # we test the attr presence explicitly because it could exist and be None
    # in which case doing
    # new_obj = getattr(obj, newattr, None)
    # if new_obj:
    #     pass
    #
    # would simple lose the info about the presence or absence of the Attr
    # and if the default value is not None then the result will endup False
    if not hasattr(obj, newattr):
        return default_value

    new_obj = getattr(obj, newattr)
    return recursive_getattr(new_obj, tail, default_value)
