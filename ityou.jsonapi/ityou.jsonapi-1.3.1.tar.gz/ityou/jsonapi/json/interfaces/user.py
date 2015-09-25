# -*- coding: utf-8 -*-
"""plone.api.users -> returns json
"""
from zope.interface import Interface


class IUserView(Interface):
    """
    api.user
    """
    def __call__(self):
        """ default view
        """
    def get(self):
        """
        Get a User.
        Returns -> User
        Return type -> MemberData object
        """
    def create(self):
        """
        Create a user.
        Returns -> Newly created user
        Return type -> MemberData object
        """
    def delete(self):
        """
        Delete a user.
        Arguments username and user are mutually exclusive. 
        You can either set one or the other, but not both.
        """
    def get_current(self):
        """
        Get the currently logged-in user.
        Returns -> Currently logged-in user
        Return type ->	MemberData object
        """
    def is_anonymous(self):
        """
        Check if the currently logged-in user is anonymous.
        Returns -> True if the current user is anonymous, False otherwise.
        Return type -> bool
        """
    def get_users(self):
        """
        Get all users or all users filtered by group.
        Returns -> All users (optionlly filtered by group)
        Return type -> List of MemberData objects
        """
    def get_roles(self):
        """
        Get user's site-wide or local roles.
        Arguments username and user are mutually exclusive. 
        You can either set one or the other, but not both. 
        if username and user are not given, the currently authenticated member will be used.
        """
    def get_permissions(self):
        """
        Get user's site-wide or local permissions.
        """
    def grant_roles(self):
        """
        Grant roles to a user.
        if username and user are not given, the authenticated member will be used.
        """
    def revoke_roles(self):
        """
        Revoke roles from a user.
        """
    def help(self):
        """
        """
            

