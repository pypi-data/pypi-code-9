#!/usr/bin/env python
# -*- coding: utf-8 -*-

import warnings

from vgmdb_wrapper.utils import *

class CATEGORY( object ):
    def __init__( self ):
        self.NONE    = False
        self.ALBUM   = 'albums'
        self.ARTIST  = 'artists'
        self.ORG     = 'orgs'
        self.PRODUCT = 'products'

class Search( JsonToClass ):
    def __init__( self, query, cate ):
        param = { 'format':'json', 'q':query }
        search_addr = 'search'
        if cate:
            search_addr += '/' + cate
        url = generate_url( search_addr )
        data = request_api( url, param )
        self._set_dict_val( data )
