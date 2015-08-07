#!/usr/bin/env python
# -*- coding: utf-8 -*-

import warnings
from urllib2 import quote
import requests

def generate_url( operate ):
    base = 'http://vgmdb.info/'
    return base + operate

def request_api( url, payload=None ):
    try:
        r = requests.get( url, params=payload )
        r.raise_for_status()
    except Exception, e:
        return {'error':e}
    else:
        return  r.json()

class JsonToClass( object ):
    def _add_instance( self, key, val ):
        d = self._controller( val )
        key = str( key )
        self._set_keys( key )
        self.__dict__[key] = self._controller( val )

    def _controller( self, data ):
        if isinstance( data, dict ):
            return JsonToClass()._set_dict_val( data )
        elif isinstance( data, list ):
            return self._set_list_val( data )
        else:
            return data

    def _set_list_val( self, data ):
        lst = []
        [ lst.append( self._controller( item ) ) for item in data ]
        return lst

    def _set_dict_val( self, data ):
        [ self._add_instance( k, v ) for k, v in data.items() ]
        return self

    def _set_keys( self, key ):
        if not hasattr( self, 'keys' ):
            self.keys = [ key ]
        else:
            self.keys.append( key )
