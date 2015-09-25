# -*- coding: utf-8 -*-
from zope.interface import Interface


class IGroupView(Interface):
    """
    api.group
    """
    def __call__(self):
        """
        """
    def get(self):
        """
        Get a group.
        Returns -> Group
        Return type -> GroupData object
        """
    def create(self):
        """
        Create a group.
        Returns-> Newly created group
        Return type -> GroupData object
        """
    def delete(self):
        """
        Delete a group.
        """
    def add_user(self):
        """
        Add the user to a group.
        """
    def remove_user(self):
        """
        Remove the user from a group.
        """
    def get_groups(self):
        """
        Get all groups or all groups filtered by user.
        
        Returns -> All groups (optionlly filtered by user)
        Return type -> List of GroupData objects
        """
    def get_roles(self):
        """
        Get group's site-wide or local roles.
        """
    def grant_roles(self):
        """
        Grant roles to a group.
        """
    def revoke_roles(self):
        """
        Revoke roles from a group.
        """
    def help(self):
        """
        """

