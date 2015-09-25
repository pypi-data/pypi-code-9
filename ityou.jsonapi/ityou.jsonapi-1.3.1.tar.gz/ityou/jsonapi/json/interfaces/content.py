# -*- coding: utf-8 -*-
from zope.interface import Interface


class IContentView(Interface):
    """
    api.content
    """
    def __call__(self):
        """
        get from request the command of portal api method.
        sends json data as response.
        
        REQUEST PARAMS:
        
        get()       ->  'get_content' 
        create()    ->  'create_content'
        delete()    ->  'delete_content'
        copy()      ->  'copy_content'
        move()      ->  'move_content'
        rename()    ->  'rename_content'
        get_uuid()  ->  'get_uuid'
        get_state() ->  'get_state'
        transition()->  'transition'
        get_view()  ->  'get_view'
        
        """
# Kein Verwendungszweck                     
#        def get(self):
#            """
#            Get an object.
#            return -> Content object
#            """
    def __call__(self):
        """
        """  
    def create(self):
        """
        Create a new content item.
        return -> Content object
        """
    def delete(self):
        """
        Delete the object.
        """
    def copy(self):
        """
        Copy the object to the target container.
        
        return -> Content object that was created in the target location
        """
    def move(self):
        """
        Move the object to the target container.
        """
    def rename(self):
        """
        Rename the object.
        """
        
# Sinnlos
#        def get_uuid(self):
#            """
#            Get the object's Universally Unique IDentifier (UUID).
#            return -> Object's UUID
#            return type -> string
#            """

    def get_state(self):
        """
        Get the current workflow state of the object.
        return -> Object's current workflow state
        Return type -> string
        """
    def transition(self):
        """
        Perform a workflow transition for the object or attempt to perform 
        workflow transitions on the object to reach the given state.
        """
    def get_view(self):
        """
        Get a BrowserView object.
        """
    def help(self):
        """
        """

