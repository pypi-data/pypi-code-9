#!/usr/bin/env python
# -*- coding: utf-8 -*-

import warnings

from vgmdb_wrapper.search import *
from vgmdb_wrapper.information import *

class Client( object ):
    def search( self, query, category=CATEGORY().NONE ):
        return Search( query, category )

    def album( self, id ):
        return Album( id )

    def artist( self, id ):
        return Artist( id )

    def org( self, id ):
        return Org( id )

    def event( self, id ):
        return Event( id )

    def product( self, id ):
        return Product( id )
