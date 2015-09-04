
def iteritems(dictlike):
    try:
        return dictlike.iteritems()
    except AttributeError:
        return dictlike.items()
