# -*- coding: utf-8 -*-
from zope.interface import Interface

class IJsonApiUtils(Interface):
    """
    Utilities to return json from an ajax-request
    """
    def _json_response(self):
        """returns json
        """
