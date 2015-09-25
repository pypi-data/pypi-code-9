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


        
class UserView():
    """
    api.user
    View: @@plonejsonapi-userview
    """
    implements(IUserView)
    
    def __call__(self):
        
        ju = JsonApiUtils()
        context   = aq_inner(self.context)  
        request = context.REQUEST
        action  = request.get('action')
        
         
        if action == "create_user":
            returndata = self.create(context)
            return ju._json_response( context, returndata )

        elif action == "delete_user":  
            returndata = self.delete(context)
            return ju._json_response( context, returndata )

        elif action == "get_current":
            returndata = self.get_current(context)
            return ju._json_response( context, returndata )

        elif action == "is_anonymous":
            returndata = self.is_anonymous(context)
            return ju._json_response( context, returndata )

        elif action == "get_users":
            returndata = self.get_users(context)
            return ju._json_response( context, returndata )

        elif action == "get_roles":
            returndata = self.get_roles(context)
            return ju._json_response( context, returndata )

        elif action == "get_permissions":
            returndata = self.get_permissions(context)
            return ju._json_response( context, returndata )

        elif action == "grant_roles":
            returndata = self.grant_roles(context)
            return ju._json_response( context, returndata )

        elif action == "revoke_roles":
            returndata = self.revoke_roles(context)
            return ju._json_response( context, returndata )

        elif action == "help":
            returndata = self.revoke_roles(context)
            return ju._json_response( context, returndata )

        else:
            returndata = {"ERROR":"NO COMMAND FOUND YOU SENT"}
            return ju._json_response( context, returndata )
            
  
    def create(self,context):
        # getestet funktioniert
        # Geplant: benutzer name und vorname, portrait, gruppe
        """
        Create a user.
        Returns -> Newly created user
        Return type -> MemberData object
        """
        request = context.REQUEST
        req_email = request.get('email') # required argument
        req_username = request.get('username')
        
        if not (req_email):
            return {'error':'missing argument'}
        
        try:
            user = api.user.create(email=req_email, username=req_username)
            return {'userid':user.getId()}
            
        except Exception as e:
            return {'error':str(e)}
        
        
    def delete(self,context):
        # getestet funktioniert
        # Geplant: Bessere Rückgabewerte
        """
        Delete a user.
        """
        request = context.REQUEST
        
        req_userid = request.get('userid')   # required argument
        
        if not(req_userid):
            return {'error':'missing argument'}
            
        try:
            user = api.user.get(userid= req_userid)
            api.user.delete(user = user)
            return {'sucess':'True'}
            
        except Exception as e:
            return {'error':str(e)}
             
    def get_current(self,context):
        #fertig
        """
        Get the currently logged-in user.
        Returns -> Currently logged-in user
        Return type ->	MemberData object
        """
        try:
            current = api.user.get_current()
            
            return {'currentuser':current.id} # user object
            
        except Exception as e:
            return str(e)
            
    def is_anonymous(self,context):
        #funktioniert
        #geplant: return information verbessern
        """
        Check if the currently logged-in user is anonymous.
        Returns -> True if the current user is anonymous, False otherwise.
        Return type -> bool
        """
        if api.user.is_anonymous():
            return True
        
        return False
        
    def get_users(self,context):
        # gestestet_ funktioniert
        """
        Get all users or all users filtered by group.
        Returns -> All users (optionlly filtered by group)
        Return type -> List of MemberData objects
        """
        request = context.REQUEST
        req_groupname = request.get('groupname') # required argument
        
        if not(req_groupname):
            return {'missing argument':'groupname'}
        try:
            users = api.user.get_users(groupname= req_groupname)
            useridlist = []
            for i in users:
                useridlist.append(i.getId())
                
            return {'group':useridlist} 
            
        except Exception as e:
            return {'error':str(e)}
     
                
    def get_roles(self,context):
        # getestet funktioniert
        """
        Get user's site-wide or local roles.
        """    
        request = context.REQUEST
        req_username = request.get('username')   # required argument
        req_folderuid = request.get('folderuid') 
     
        if not req_username:
            return {'error':'missing argument'}
            
        try:
            folder = api.content.get(UID=req_folderuid)
            roles = api.user.get_roles(username= req_username, obj=folder )
            return {folder.getId():roles} 
            
        except Exception as e:  
            return {'error':str(e)}    
        
     
    def get_permissions(self,context):
        # getestet funktioniert
        """
        Get user's site-wide or local permissions.
        """
        request = context.REQUEST
        req_username = request.get('username') # required argument
        
        if not (req_username):
            return {'missing argument':'username'}
        try:
            permissions = api.user.get_permissions(username=req_username)
            return permissions 
            
        except Exception as e:
            return {'error':str(e)}
            
            
    def grant_roles(self):
        # Nicht getestet
        # ÜBERTRAGUNG UND KONVERTIERUNG DES REQUESTS IN EINE LISTE NICHT MÖGLICH
        """
        Grant roles to a user.
        """
        request = context.REQUEST
        req_username = request.get('username')  # required argument 
        req_roles = request.get('roles')        # required argument #List of Roles ['role1','role2']
        
        if not (req_roles):
            return {'missing argument':'roles'}
            
        try:
            api.user.grant_roles(username=req_username, roles= req_roles)
            return {'sucess':'true'} #TODO Look up a better return
            
        except Exception as e:
            return {'error':str(e)}
            
    def revoke_roles(self):
        # Nicht getestet
        # ÜBERTRAGUNG UND KONVERTIERUNG DES REQUESTS IN EINE LISTE NICHT MÖGLICH
        """
        Revoke roles from a user.
        """
        request = context.REQUEST
        req_username = request.get('username')  # required argument 
        req_roles = request.get('roles')        # required argument #List of Roles ['role1','role2']

        if not (req_roles):
            return {'missing argument':'roles'}
        
        try:
            api.user.revoke_roles(username=req_username, roles=req_roles)
            return {'sucess':'true'} #TODO Look up a better return
            
        except Exception as e:
            return e
    
    def help(self):
        """ help function"""
        
        help = {
        'create_user':'Parameters: email, username',
        'delete_user':'Parameters: userid',
        'get_current':'no Parameters required, returns Id of currently logged in user',
        'is_anonymous':'returns true or false, no Parameter required',
        'get_users':'Parameters: groupname',
        'get_roles':'Parameters: username, folderuid',
        'get_permissions':'Parameters: username',
        'grant_roles':'Parameters: username, roles',
        'revoke_roles':'Parameters: username, roles',
        'help':'Parameters:',
        }
        return help
        


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
            

