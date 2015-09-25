# -*- coding: utf-8 -*-

"""
Version: 1.2
Geplant:
- Erstellen einer Help View oder für jede View eine Help Methode
- portal catalog methode zum abfrage bestimmter inhalte

"""
import json
from plone import api
from Acquisition import aq_inner
from DateTime import DateTime
from Products.CMFPlone.utils  import getToolByName
from zope.interface import implements

from interfaces import IPortalView, IContentView, IUserView, IGroupView

class PortalView():
    """
    api.portal
    
    View : @@plonejsonapi_portalview
    """ 
    implements(IPortalView)
    
    def __call__(self):
        """
        get from request the command of portal api method.
        sends json data as response.
        """
        ju = JsonApiUtils()
        context   = aq_inner(self.context)  
        request = context.REQUEST
        action  = request.get('action')
        
#        if action == "get_portal":
#            dictdata = self.get(context)
#            return ju._json_response( context, dictdata )
            
        if action == "get_navigation_root":
            dictdata = self.get_navigation_root(context)
            return ju._json_response( context, dictdata )

        elif action == "get_localized_time":
            dictdata = self.get_localized_time(context)
            return ju._json_response( context, dictdata )

        elif action == "send_email":
            dictdata = self.send_email(context)
            return ju._json_response( context, dictdata )

        elif action == "show_message":
            dictdata = self.show_message(context)
            return ju._json_response( context, dictdata )
        
        else:                
            dictdata = {"ERROR":"NO COMMAND FOUND YOU SENT"}
            return ju._json_response( context, dictdata )

# SINNLOS                         
#    def get(self,context):
#        # Nicht getestet
#        """
#        Get the Plone portal object out of thin air.
#        return type -> Portal Object
#        """
#        # CHECK CORRECT OPERATION
#        portal = api.portal.get()
#        physical_path = portal.getPhysicalPath() #Getting physical path
#        portal_id = portal.getId()
#        dictdata = {"id": portal_id, "physical_path": physical_path,}        
#        return dictdata            
        
    def get_navigation_root(self,context):
        # Nicht getestet
        """
        Get the navigation root object for the context.
        return type -> Portal Object
        """
        # CHECK CORRECT OPERATION
        nav_root = api.portal.get_navigation_root(context)
        uuid = api.content.get_uuid(obj=nav_root)
        
        nav_data = {"uuid": uuid}
        return nav_data # return type: portal object # TODO KEINE Rückgabe der UUID des Portal Objekts möglich
        
        
    def get_localized_time(self,context):
        # Nicht getestet
        """
        Display a date/time in a user-friendly way.
        return type -> string
        """
        request = context.REQUEST
        #today = DateTime()
        req_datetime  = request.get('datetime')
        
        localized = api.portal.get_localized_time(datetime=req_datetime)
        localizeddata = { "localized_time": localized}
        
        return localizeddata # returntype: string
        
    def send_email(self,context):
        # Nicht getestet
        """
        Send an email.
        no return
        """
        request = context.REQUEST
        req_recipient = request.get('recipient')
        req_sender  = request.get('sender')
        req_subject  = request.get('subject')
        req_body  = request.get('body')
        
        try:                        
            api.portal.send_email(
                        recipient=req_recipient,
                        sender=req_sender,
                        subject=req_subject,
                        body=req_body,
                        )
            
            return True
                        
        except Exception as e:
            return {'error':str(e)}
            
        
    def show_message(self,context):
        # Nicht getestet
        """
        Display a status message.
        no return
        """
        request = context.REQUEST
        yourmessage = request.get('message')
        
        try:
            api.portal.show_message(message=yourmessage, request=request)
            return True # No Documentation in plone.api 
            
        except Exception as e:
            return {'error': str(e)}
             


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
            

