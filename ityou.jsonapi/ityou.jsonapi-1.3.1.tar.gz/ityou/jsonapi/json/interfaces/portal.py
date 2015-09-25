# -*- coding: utf-8 -*-
from zope.interface import Interface

# Version 1.1

class IPortalView(Interface):
    """
    api.portal
    """ 
    def __call__(self):
    
        """
        Get the Command out of Request. 
        Send Response contains Json Data
        
        REQUEST PARAMS:
        
        get()                   -> 'get_portal'
        get_navigation_root()   -> 'get_navigation_root'
        get_tool()              -> 'get_tool' , 'toolname'
        get_localized_time()    -> 'get_localized_time' , 'datetime'
        send_email()            -> 'send_email' , 'recipient' , 'sender' , 'subject' , 'body' 
        show_message()          -> 'show_message' , 'message'
        
        """
               
    def get(self):
        """
        Get the Plone portal object out of thin air.
        return type -> Portal Object

        id = portal.getProperty('id')            
        name = portal.getProperty('name')
        """
        
    def get_navigation_root(self):
        """
        Get the navigation root object for the context.
        return type -> Portal Object
        """
        
    def get_tool(self):
        """
        Get a portal tool in a simple way.
        return -> 	The tool that was found by name
        """
        
    def get_localized_time(self):
        """
        Display a date/time in a user-friendly way.
        return type -> string
        """
        
    def send_email(self):
        """
        Send an email.
        no return
        """
        
    def show_message(self):
        """
        Display a status message.
        no return
        """
        
    def get_registry_record(self):
        """
        Get a record value from a the plone.app.registry
        no return
        
        Not implemented
        """

