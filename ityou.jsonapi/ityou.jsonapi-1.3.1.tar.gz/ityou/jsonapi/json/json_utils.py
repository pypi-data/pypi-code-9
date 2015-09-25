# -*- coding: utf-8 -*-
import json
from zope.interface import implements
from interfaces import IJsonApiUtils

class JsonApiUtils():
    """small utilities
    """
    implements(IJsonApiUtils)

    def _json_response(self, context, data):
        """ Returns Json Data in Callback function
        """
        request  = context.REQUEST
        callback = request.get('callback','')        
        request.response.setHeader("Content-type","application/json")
        if callback:
            cb = callback + "(%s);"
            return cb % json.dumps(data)
        else:
            return json.dumps(data)

