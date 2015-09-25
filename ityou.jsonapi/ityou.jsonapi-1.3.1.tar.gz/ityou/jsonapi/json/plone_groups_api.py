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


        
class GroupView():
    """
    api.group
    View: @@plonejsonapi-groupview
    """
    implements(IGroupView)
    
    def __call__(self):
        
        ju = JsonApiUtils()
        context   = aq_inner(self.context)  
        request = context.REQUEST
        action  = request.get('action')
        
        if action == "get_group":
            returndata = self.get(context)
            return ju._json_response( context, returndata )
            
        elif action == "create_group":
            returndata = self.create(context)
            return ju._json_response( context, returndata )

        elif action == "delete_group":  
            returndata = self.delete(context)
            return ju._json_response( context, returndata )

        elif action == "add_user":
            returndata = self.add_user(context)
            return ju._json_response( context, returndata )

        elif action == "remove_user":
            returndata = self.remove_user(context)
            return ju._json_response( context, returndata )

        elif action == "get_groups":
            returndata = self.get_groups(context)
            return ju._json_response( context, returndata )

        elif action == "get_roles":
            returndata = self.get_roles(context)
            return ju._json_response( context, returndata )

        elif action == "grant_roles":
            returndata = self.grant_roles(context)
            return ju._json_response( context, returndata )

        elif action == "revoke_roles":
            returndata = self.revoke_roles(context)
            return ju._json_response( context, returndata )

        elif action == "help":
            returndata = self.help()
            return ju._json_response( context, returndata )
            
        else:
            returndata = {"ERROR":"NO COMMAND FOUND YOU SENT"}
            return ju._json_response( context, returndata )


    def create(self,context):
        # Gestestet: Funktioniert
        """
        Create a group.
        Returns-> Newly created group
        Return type -> GroupData object
        """
        request = context.REQUEST
        
        req_groupname = request.get('groupname')        #(string) -- [required] Name of the new group.
        req_title = request.get('title')                #(string) -- Title of the new group
        req_description = request.get('description')    #(string) -- Description of the new group
        # ÜBERTRAGUNG UND KONVERTIERUNG DES REQUESTS IN EINE LISTE NICHT MÖGLICH
        req_roles = request.get('roles') or None        #(list) -- Roles to assign to this group
        req_groups = request.get('groups')  or None     #(list) -- Groups that belong to this group
        
        if not req_groupname:
            return {'error':'missing argument'}
            
        try:
            group = api.group.create(
                            groupname=req_groupname,
                            title= req_title,
                            description= req_description,
                            roles= req_roles,
                            groups=req_groups)
                            
            return {'newgroup': group.getId()}
                                
        except Exception as e :
            return {'error':str(e)}
            
        
    def delete(self,context):
        # Nicht getestet
        """
        Delete a group.
        """
        request = context.REQUEST
        req_group = request.get('groupname') 
        
        if not req_group:
            return {'error':'missing argument'}
            
        try:
            api.group.delete(groupname= req_group)
            return {'deleted': req_group}
            
        except Exception as e :
            return {'error':str(e)}
        
        
    def add_user(self,context):
        # Nicht getestet
        """
        Add the user to a group.
        """
        request = context.REQUEST
        req_username = request.get('username') #   [required](string) -- Username of the user to add to the group.
        req_groupname = request.get('groupname') # [required](string) -- Name of the group to which to add the user.
        
        if not req_username or not req_groupname:
            return {'error': 'missing argument'}
        
        try:
            user = api.group.add_user(groupname=req_username, username=req_groupname)
            return {'newuser:': user.getId()} 
            
        except Exception as e:
            return {'error':str(e)}
            
            
    def remove_user(self,context):
        # Nicht getestet
        """
        Remove the user from a group.
        """
        request = context.REQUEST
        req_username = request.get('username') #   [required](string) -- Username of the user to add to the group.
        req_groupname = request.get('groupname') # [required](string) -- Name of the group to which to add the user.
        
        if not req_username or not req_groupname:
            return {'error': 'missing argument'}
        
        try:
            api.group.remove_user(groupname=req_groupname, username=req_username) 
            return {'removed': req_username}
            
        except Exception as e:
            return {'error': str(e)}
            
            
    def get_groups(self,context):
        # Nicht getestet
        """
        Get all groups or all groups filtered by user.
        
        Returns -> All groups (optionlly filtered by user)
        Return type -> List of GroupData objects
        """
        
        request = context.REQUEST
        req_username = request.get('username') or None #   (string) -- Username of the user to add to the group.
        
        try:
            groups = api.group.get_groups(username=req_username)
            groupsidlist = []
            
            for i in groups:
                groupsidlist.append(i.getId())
            return {'groups':groupsidlist}
            
        except Exception as e:
            return {'error':str(e)}
        
        
    def get_roles(self,context):
        # Nicht getestet
        """
        Get group's site-wide or local roles.
        """
        request = context.REQUEST
        req_groupname = request.get('groupname')  #[required] 
        req_folderuid = request.get('folderuid')  #[optional] if not: site wide role will be return
        
        if not req_groupname:
            return {'error': 'missing argument'}
            
        try:
            folder = api.content.get(UID=req_folderuid)
            roles = api.group.get_roles(groupname=req_groupname, obj=folder)
            return roles # TODO what is a roles  # TODO Look up return 
                
        except Exception as e:
            return {'error':str(e)}
            
        
    def grant_roles(self,context):
        # Nicht getestet
        # ÜBERTRAGUNG UND KONVERTIERUNG DES REQUESTS IN EINE LISTE NICHT MÖGLICH
        """
        Grant roles to a group.
        """
        request = context.REQUEST
        req_groupname = request.get('groupname')
        req_roles = request.get('roles') # List of Roles: ['Reviewer, SiteAdministrator']
        
        if not req_groupname or not req_roles:
            return {'error':'missing arguments'}
       
        try:
            api.group.grant_roles(groupname=req_groupname, roles=req_roles)
            return {'grantedroles': req_roles}
            
        except Exception as e:
            return {'error': str(e)}
        
        
    def revoke_roles(self):
        # Nicht getestet
        # ÜBERTRAGUNG UND KONVERTIERUNG DES REQUESTS IN EINE LISTE NICHT MÖGLICH
        """
        Revoke roles from a group.
        """
        request = context.REQUEST
        req_groupname = request.get('groupname')
        req_roles = request.get('roles') # List of Roles: ['Reviewer, SiteAdministrator']

        if not req_groupname or not req_roles:
            return {'error':'missing arguments'}
        
        try:
            api.group.revoke_roles(groupname=req_groupname, roles=req_roles)
            return {'revokedroles': req_roles}
            
        except Exception as e:
            return {'error': str(e)}
            
    def help(self,context):
        """ help function"""
        
        help = {
            'get_group':'Parameter:',
            'create_group':'',
            'delete_group':'',
            'add_user':'',
            'remove_user':'',
            'get_groups':'',
            'get_roles':'',
            'grant_roles':'',
            'revoke_roles':'',
            'help':'',
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
            

