# -*- coding: utf-8 -*-
""" 
# ==============================================================================
# (c) ITYOU, 2015
# ---------------
# Collection of d3pie charts that are 
# displayed in portlets
# ==============================================================================

"""
import json
from plone import api
from Acquisition import aq_inner

from Products.CMFPlone.utils  import getToolByName
from DateTime import DateTime

from plone.memoize import view

from zope.component.hooks import getSite
from zope.i18nmessageid import MessageFactory

__ = MessageFactory("plone")
from . import portletsMessageFactory as _
from ityou.follow.dbapi import DBApi
from colors import WORKFLOW_COLORS, AVAILABILITY_COLORS, DOCUMENTRATING_COLORS

ERROR_MESSAGE_DATA = { 'error':'No Data available!' }

DB = DBApi()


class DataDigger:
    """ Digging Plone Data and return it in JSON. """
        
    def __call__(self):
        """
        Main call with param 'chart'
        """
        context   = aq_inner(self.context)  
        request = context.REQUEST
                
        self.ptool =         getToolByName(context, "portal_types")
        self.catalog =       getToolByName(context, "portal_catalog")
        self.translate =     getToolByName(context, 'translation_service').translate
            
        data_request = request.get('data')
        chart_type   = request.get('chart')
        selected_context = request.get('selectedcontext')

        # Abfrage auf lokale oder globale Ergebnisse der Suche 
        if selected_context == "global":
            context = api.portal.get()            
        elif selected_context == "local":
            context   = aq_inner(self.context)  
        else:
            context   = aq_inner(self.context) 
            print('no selected_context')
            

        #PORTALTYPES--------------------------------------------------
        if data_request == "portaltypes":
            data = self._portaltypes(context)
            jsondata = self._make_chart_data(context, data, chart_type = chart_type)
                                
        #REVIEWSTATES-------------------------------------------------
        elif data_request == "releasestates":
            data = self._release_states(context)
            jsondata = self._make_chart_data(context, data, chart_type = chart_type)
                
        #DOCUMENTRATING-------------------------------------------------
        elif data_request == "documentrating":
             data = self._documentrating()
             jsondata = self._make_chart_data(context, data, chart_type = chart_type, colorlist = DOCUMENTRATING_COLORS)
            
        #AVAILABILITY-------------------------------------------------
        elif data_request == "availability":
            data = self._availability(context)
            jsondata = self._make_chart_data(context, data, chart_type= chart_type, colorlist = AVAILABILITY_COLORS)

        #Followers-------------------------------------------------
        elif data_request == "followers":
            data = self._followers(context)
            jsondata = data

        else:
            data = ERROR_MESSAGE_DATA
        
        return ju._json_response( context, jsondata )
     

    @view.memoize
    def _portaltypes(self, context): 
        """ Counts plone content objects, grouped by portaltypes
        """                           
        path = '/'.join(context.getPhysicalPath())
        data = {}
        
        for pt in self.ptool:
            count = len(self.catalog({'portal_type': pt, 'path':path, 'show_inactive':True}))
            if count:
                data.update({pt:count})
            
        return data


    @view.memoize
    def _release_states(self, context): 
        """ Counts plone content objects, grouped by release state
        """                
        path = '/'.join(context.getPhysicalPath())
        data = {}
        
        brains = self.catalog({'path':path, 'show_inactive':True})

        state_mapping = self._review_states_titles(context)

        for state,title in state_mapping.items():
                        
            count = len(self.catalog({'path':path, 'review_state':state, 'show_inactive':True}))
            if count:
                data.update({title:count})
            
        return data


    @view.memoize
    def _review_states_titles(self,context):
        """returns a dictionary state:state_title
        """    
        wt = getToolByName(context,'portal_workflow')
        wfs = wt.getWorkflowIds()
        
        state_mapping = {}
        for wf in wfs:
            states = context.portal_workflow[wf].states
            for state in states:
                title = context.portal_workflow[wf].states[state].title
                state_mapping.update({state:title})

        return state_mapping      
        
        
    @view.memoize          
    def _availability(self, context):
        """ check the availability of documents global or in folder. the results are displayed in a pie chart"""
                
        path = '/'.join(context.getPhysicalPath())
        timestamp_now = DateTime()
        
        coming =      len(self.catalog(path= path, effective = {'query': timestamp_now,'range': 'min'})) 
        effective_documents =  len(self.catalog(effectiveRange=DateTime(),path= path,))
        expired_documents =    len(self.catalog(path= path, expires   = {'query': timestamp_now,'range': 'max'})) 
                 
        return {'coming':coming,'effective':effective_documents,'expired':expired_documents}

    @view.memoize          
    def _documentrating(self):
        """ retruns the rating of the documents which the user uploaded"""
        
        sid  = api.user.get_current()
        count_top, count_flop = DB.getAllLikes(sid.id)
        
        return {'Like': count_top, 'Dislike': count_flop}

        
    def ityou_extuserprofile_installed(self): # _followers need this
        try:
            import ityou.extuserprofile        
            return True
        except:
            return False
                
    def _followers(self,context):  
        """retruns list with user infomation like profilepicture,email ...
        
        """
        mt = getToolByName(context,'portal_membership')
        me = mt.getAuthenticatedMember().getId()
                  
        userids = DB.getFollowers(me) # Follower
        
        current_user = mt.getMemberById(me)
        users = []
                
        for userid in userids:
            user_data = self._get_user_data(userid)
            users.append({
                          'id'              : userid,
                          'fullname'        : user_data[2],
                          'email'           : user_data[3],
                          'portrait_large'  : user_data[4], 
                          'profile'         : user_data[0],
                          'portrait'        : user_data[1],
             #             'bar'             : bar,
             #             'recent_time'     : ou[1],
             #             'timeout_online'  : timeout_online,
             #             'time_delta'      : time_delta,
                          })        
        return users
               

    def _get_user_data(self,uid):
        """Return user informations and keep them in cache
           does it work like this ????
        """
        context = aq_inner(self.context)
        mt      = getToolByName(context,'portal_membership')
        user    = mt.getMemberById(uid)

        if user:
            if self.ityou_extuserprofile_installed() == True:
                portrait_url = mt.getPersonalPortrait(uid, size='pico').absolute_url()
                portrait_large_url = mt.getPersonalPortrait(uid, size='large').absolute_url()
            else:
                portrait_url = mt.getPersonalPortrait(uid).absolute_url()
                portrait_large_url = portrait_url

            profile = getSite().absolute_url() + '/author/' + uid
            fullname = user.getProperty('fullname','')
            email = user.getProperty('email','')

            return profile, portrait_url, fullname, email, portrait_large_url
        else:
            logging.warn('User "%s" no longer exists' % uid)


    def _make_chart_data(self, context, data, colorlist= None, chart_type="d3pie"):
        """make
        data = [{key:value}] with the digged content
        kind_of_chart = d3pie, c3pie, 
        colorlist = PORTALTYPES_COLOR[], WORKFLOW_COLORS, AVAILABILITY_COLORS , ...
        """
        
        def translate(key):
            """ Is the translation in Plone? or in our locals?
            """
            tlkey = self.translate(__(key), default = "nothing", context = context)
            if tlkey == key:
                tlkey = self.translate(_(key), default = "nothing", context = context)
            return tlkey
            
        if chart_type == "d3pie": 
            newdata = []
            for key,val in data.items():
                label = translate(key)
                if colorlist == None:
                    newdata.append({'label':label,'value':val})  
                else:      
                    newdata.append({'label':label,'value':val,'color':colorlist[key]}) # TODO Wenn key nicht vorhanden ? 
            return newdata
            
        elif chart_type == "c3pie":
             return data
        
        else:
            return [{"error":"dieses Chart exisitert nicht"}]    

             
class JsonApiUtils():
    """small utilities
    """
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


class MissingTranslations():
    """#ToDo: this terms should be translated
       Dummy Class, should be removed later ...
    """
    expires = _("expired")
    effective = _("effective")
    coming = _("coming")


  
ju = JsonApiUtils()  
