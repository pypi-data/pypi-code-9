#!/usr/bin/env python
from __future__ import print_function
import itertools
import json

try:
    import requests
except ImportError:
    print("pip install requests")
    raise

###############################################################################
# Exceptions
###############################################################################
class ClientError(Exception):

    pass


###############################################################################
# Clients
###############################################################################

class RestJSON:
    headers = {"Content-Type":"application/json; charset=UTF-8"}
    history = []

    def __init__(self, baseurl, proxies=None, method_hooks={}):
        self.baseurl = baseurl
        self.session = requests.session()
        self.session.proxies = proxies
        self.method_hooks = method_hooks
        self.session.hooks["response"].append(self.__add_history)

    def _gen_hooked_request(self, method, target):
        _func =self.__class__.__dict__['_' + method](self, target)
        _hooks = self.method_hooks.get(method) or ()
        def _hooked(*args, **kwargs):
            for hook in _hooks:
                hook()
            return _func(*args, **kwargs)
        return _hooked

    def __getattr__(self, name):
        if name in self.__class__.__dict__:
            return self.__class__.__dict__[name]
        method, endpoint = name.split('_',1)
        endpoint = '/'.join(endpoint.split('_'))
        target = self.baseurl + '/' +  endpoint
        return self._gen_hooked_request(method, target)

    def _get(self, target):
        def _func(*args,**kwargs):
            args = '/'.join(str(a) for a in args)
            url = target + '/' + args 
            if kwargs:
                url += '?' + '&'.join("%s=%s" % i for i in kwargs.items())
            return self.session.get(url)
        return _func

    def _post(self, target):
        url = target
        def _func(jdict):
            return self.session.post(target, data=json.dumps(jdict), 
                                 headers=self.headers)
        return _func
    
    def _put(self, target):
        url = target
        def _func(jdict):
            return self.session.put(target, data=json.dumps(jdict), 
                                headers=self.headers)
        return _func
    
    def _delete(self, target):
        def _func(*args,**kwargs):
            args = '/'.join(str(a) for a in args)
            url = target + '/' + args 
            return self.session.delete(url)
        return _func

    def __add_history(self, response, *args, **kwargs):
        self.history.append(response)

    
