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


class ContentView():
    """
    api.content
    View: @@plonejsonapi-contentview
    """       
    
    implements(IContentView)
    
    def __call__(self):
        """
        get from request the command of portal api method.
        sends json data as response.
        """
        ju = JsonApiUtils()
        context   = aq_inner(self.context)  
        request = context.REQUEST
        action  = request.get('action')
                    
        if action == "create_content":
            dictdata = self.create(context)
            return ju._json_response( context, dictdata )

        elif action == "delete_content":  
            dictdata = self.delete(context)
            return ju._json_response( context, dictdata )

        elif action == "copy_content":
            dictdata = self.copy(context)
            return ju._json_response( context, dictdata )

        elif action == "move_content":
            dictdata = self.move(context)
            return ju._json_response( context, dictdata )

        elif action == "rename_content":
            dictdata = self.rename(context)
            return ju._json_response( context, dictdata )

        elif action == "get_uuid":
            dictdata = self.get_uuid(context)
            return ju._json_response( context, dictdata )

        elif action == "get_state":
            dictdata = self.get_state(context)
            return ju._json_response( context, dictdata )

        elif action == "transition":
            dictdata = self.transition(context)
            return ju._json_response( context, dictdata )

        elif action == "get_view":
            dictdata = self.get_view(context)
            return ju._json_response( context, dictdata )

        elif action == "help":
            dictdata = self.help(context)
            return ju._json_response( context, dictdata )
            
        else:                
            dictdata = {"ERROR":"NO COMMAND FOUND YOU SENT"}
            return ju._json_response( context, dictdata )
        

    def create(self,context):
        #fertig
        """
        Create a new content item.
        return -> Content object
        """
        request = context.REQUEST 

        req_type = request.get('type')      # required argument
        req_id = request.get('id')          # optional argument (will be generated out of title)
        req_title = request.get('title')    # required argument
        req_save_id = request.get('save_id', '1')
        
        if not(req_container) or not(req_type):
            return {'error': 'missing arguments'}
        
        if req_save_id == '0':
            req_save_id = False
        else:
            req_save_id = True
            
        # container object berechnen
        container = api.content.get(UID=req_container)
        if not container:
            return {'error':'Missing Container'}

        try:            
            content = api.content.create(
                container = container, 
                type = req_type, 
                id = req_id, 
                title = req_title, 
                safe_id = req_save_id)
                     
            return {'uuid':api.content.get_uuid(obj=content)}
          
        except Exception as e:
            return {'error': str(e)}
        
    
    def delete(self,context):
        #fertig
        """
        Delete the object.
        """
        request = context.REQUEST
        req_uid = request.get('uid') # required argument

        if not(req_uid):
            return {'error':'missing arguments'}
        
        try:
            content = api.content.get(UID=req_uid)
            api.content.delete(obj=content)
                        
            return {'deleted':req_uid}
            
        except Exception as e:
            return {'error': str(e)}
        
    def copy(self,context):
        #fertig
        
        """
        Copy the object to the target container.
        return -> Content object that was created in the target location
        """
        portal = api.portal.get()
        
        request = context.REQUEST
        req_source = request.get('source') # required argument (uid)
        req_target = request.get('target') # optional argument (uid of folder)
        req_id = request.get('id')         # optional argument (id of copied object on target location)    
        req_save_id = request.get('save_id', '1')

        if req_save_id == '0':
            req_save_id = False
        else:
            req_save_id = True
        
        if not(req_source):
            return {'error':'missing arguments'}
        
        try:                                      
            content = api.content.get(UID=req_source)
            targetfolder = api.content.get(UID=req_target)
                 
            newcontent = api.content.copy(source= content, target= targetfolder, id=req_id, safe_id= req_save_id)
            contentuuid = api.content.get_uuid(obj=newcontent)
                         
            return {'newobj':contentuuid} 
        
        except Exception as e:
            return {'error': str(e)}
            
      
    def move(self,context):
        #fertig
        """
        Move the object to the target container.
        """
        request = context.REQUEST
        req_source = request.get('source') # required argument (uid)
        req_target = request.get('target') # optional argument (uid of folder)
        req_id = request.get('id')         # optional argument (id of moved object on target location)

        if not(req_source):
            return {'error':'missing arguments'}
        
        try:        
            content = api.content.get(UID=req_source)
            targetfolder = api.content.get(UID=req_target)
            movedcontent = api.content.move(source=content, target=targetfolder, id=req_id)
            contentuuid = api.content.get_uuid(obj=movedcontent)
            
            return {'uuid':contentuuid}
            
        except Exception as e:
            return {'error': str(e)}
       
            
    def rename(self,context):
        #fertig
        """
        Rename the object.
        """            
        request = context.REQUEST
        req_uid = request.get('uid')       # required argument (uid of object we want to rename)
        req_newid = request.get('new_id')  # required argument (new id of the obj)

        if not (req_uid) or not(req_newid):
            return {'error':'missing arguments'}
        
        try:
            content = api.content.get(UID=req_uid)

            renamedcontent = api.content.rename(obj=content, new_id=req_newid)
            contentuuid = api.content.get_uuid(obj=renamedcontent)
            
            return {'id_new':contentuuid}
        
        except Exception as e:
            return {'error': str(e)}
            
                
    def get_state(self,context):
        #fertig
        """
        Get the current workflow state of the object.
        return -> Object's current workflow state
        Return type -> string
        """
        request = context.REQUEST
        req_uid = request.get('uid') # required argument
        
        try:
            content = api.content.get(UID=req_uid)
            state = api.content.get_state(obj=content)
            return {'state':state}
            
        except Exception as e:
            return {'error': str(e)}
        
        
    def transition(self,context):
        #noch zu erledigen
        """
        Perform a workflow transition for the object or attempt to perform 
        workflow transitions on the object to reach the given state.
        """
        request = context.REQUEST
        req_uid = request.get('uid') 
        req_transition = request.get('transition')
        req_to_state = request.get('to_state')
        
        try:
            content = api.content.get(UID=req_uid)
            api.content.transition(obj=content, transition=req_transition, to_state= req_to_state) #TODO get_state ???
            return {'status':'ok'}
            # no return in documentation given     
            
        except Exception as e:
            return {'error': str(e)}
       

    def get_view(self,context):
         """Get a BrowserView object. 
         #-----
         portal = api.portal.get()    
         yourrequest = context.REQUEST
         yourname = yourrequest.get('name')
         yourcontext = yourrequest.get('context')
         try:
             ViewObj = api.content.get_view(name=yourname, context=context[yourcontext],request=yourrequest)
             return {'name':viewname}
         except Exception as e:
             return str(e)
         """
         pass
        
    def help(self,context):
        """
        help function
        returns text about the methods and their using
        """
        
        help = {
        'create_content':'Parameters: container, type, id, title',
        'delete_content':'Parameters: id',
        'copy_content':'Parameters: source, target',
        'move_content':'Parameters: source, target, id(id of moved object)',
        'rename_content':'Parameters: id, new_id',
        'get_state':'Parameters: id', 
        'transition':'id, transition, to_state', 
#        'get_view':'Parameters: name, context',
        'help':'help function', 
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
            

