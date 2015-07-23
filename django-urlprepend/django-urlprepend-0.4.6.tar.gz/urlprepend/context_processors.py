from urlprepend.middleware import is_prepend, current_prepend
from urlprepend import settings as urlprepend_settings

def urlprepend(request):
    prepend_string = current_prepend()
    prepending = is_prepend()
    if prepending:
        return {'is_prepend': True, 'prepend_string' : prepend_string, ("is_prepend_%s" % prepend_string): True }
    else:
        return { "is_prepend": False, 'prepend_string': prepend_string }
