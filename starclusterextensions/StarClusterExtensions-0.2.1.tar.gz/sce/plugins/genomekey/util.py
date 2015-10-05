def tobool(x):
    if isinstance(x, bool):
        return x
    elif x == 'True':
        return True
    elif x == 'False':
        return False
    else:
        raise ValueError('Bad bool value: %s' % x)