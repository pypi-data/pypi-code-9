# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------------
This module contains the like views of ityou.follow
--------------------------------------------------------------------------------
"""
import json

from Acquisition import aq_inner

from plone import api

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from ..dbapi import DBApi

DB = DBApi()
     
class VotingView(BrowserView):
    """Class to vote
    """

    def __call__(self):
        """Default Template View
        """
        context =  aq_inner(self.context)
        request =  context.REQUEST       
        response = request.RESPONSE
        
        action = request.get('action')
        
        if not action:
            return None        
        elif action == 'vote':
            return self._vote()
        elif action == 'get_votes':
            return self._get_votes()
        
        
    def _vote(self):
        context =  aq_inner(self.context)
        request =  context.REQUEST       

        vote = request.get('vote',0)
        uid  = request.get('uid')
        sid  = request.get('sid')
                
        if vote not in ['-1','1']:
            return 
        
        count_top, count_flop = DB.vote(uid, sid, int(vote))

        return  json.dumps( {'top': count_top, 'flop': count_flop}    ) 
        #TODO/MR#return self.jsonResponse(context, {'top': count_top, 'flop': count_flop} )
    
    
    def _get_votes(self):
        context =  aq_inner(self.context)
        request =  context.REQUEST       
        
        uid  = request.get('uid')
        print "get Votes for UID: %s" % uid
                
        count_top, count_flop = DB.getLikes(uid)

        return json.dumps( {'top': count_top, 'flop': count_flop}    ) 
        #TODO/MR#return self.jsonResponse(context, {'top': count_top, 'flop': count_flop} )
        
        
    def jsonResponse(self, context, data):
        """ Returns Json Data in Callback function
        """
        request = context.REQUEST
        callback = request.get('callback','')        
        request.response.setHeader("Content-type","application/json")

        if callback:
            cb = callback + "(%s);"
            return cb % json.dumps(data)
        else:
            return json.dumps(data)


