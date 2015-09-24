import os
from okapi.core.summary import Summary


class InternalSettings(object):
    last_breadcrumb = None
    path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    status = True
    summary = Summary()
