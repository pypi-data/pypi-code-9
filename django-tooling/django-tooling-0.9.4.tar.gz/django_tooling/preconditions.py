def checkNotNone(value, paramName=None):
    if value is None:
        raise TypeError("Attribute{} must not be None".format(" '{}'".format(paramName) if paramName else ""))
    return value
