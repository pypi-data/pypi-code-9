#!/usr/bin/env python
# -*- coding: utf-8 -*-

from vgmdb_wrapper.utils import *

class Link( JsonToClass ):
    def __init__( self, link ):
        url = generate_url( link )
        data = request_api( url, {'format':'json'} )
        self._set_dict_val( data )

class Album( Link ):
    def __init__( self, id ):
        link = 'album/' + str( id )
        InfoBase.__init__( self, link )

class Artist( Link ):
    def __init__( self, id ):
        link = 'artist/' + str( id )
        InfoBase.__init__( self, link )

class Org( Link ):
    def __init__( self, id ):
        link = 'org/' + str( id )
        InfoBase.__init__( self, link )

class Event( Link ):
    def __init__( self, id ):
        link = 'event/' + str( id )
        InfoBase.__init__( self, link )

class Product( Link ):
    def __init__( self, id ):
        link = 'product/' + str( id )
        InfoBase.__init__( self, link )
