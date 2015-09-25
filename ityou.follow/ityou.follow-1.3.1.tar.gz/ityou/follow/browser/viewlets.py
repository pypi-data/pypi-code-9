# -*- coding:utf-8 -*-
"""
--------------------------------------------------------------------------------
Viewlet to display Like/Dislike- and Follow-Buttons
--------------------------------------------------------------------------------
"""
from Acquisition import aq_inner

from zope.interface import implements
from zope.viewlet.interfaces import IViewlet
from zope.component import getUtility

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView

from plone import api
from plone.registry.interfaces import IRegistry

from ..dbapi import DBApi
from .. import _
from ..interfaces import IFollowSettings
from ..config import TEMPLATE_BLACKLIST

dbapi = DBApi()


class FollowViewlet(BrowserView):
    """Viewlet used to display the buttons
    """
    implements(IViewlet)
    render = ViewPageTemplateFile("templates/follow.pt")

    def __init__(self, context, request, view=None, manager=None):
        super(FollowViewlet, self).__init__(context, request)
        self.context = context

    def isAuthenticatedMember(self):
        """ Checks if the viewer is authenticated.
        """
        if api.user.is_anonymous():
            return False
        else:
            return True
    
    def isFollowing(self):
        """ Checks if the authenticated member is following the author
        """
        mt = getToolByName(self.context, "portal_membership")
        auth_member = mt.getAuthenticatedMember()
        auth_member_id = auth_member.getId()
        author = self.context.Creator()

        return dbapi.isFollowing(auth_member_id, author)
    
    def author(self):
        """ Returns author of the current object
        """
        return self.context.Creator()

    def authorname(self):
        """ Returns authorname of the current object
        """
        mt = getToolByName(self.context, "portal_membership")
        creator = mt.getMemberById(self.context.Creator())        
        if creator:
            authorname = creator.getProperty("fullname") or creator.getId()
        else:
            authorname = ''
        return authorname

    def isMe(self):
        """ Returns if the creator is the authenticatedMember
        """
        mt = getToolByName(self.context, "portal_membership")
        return mt.getAuthenticatedMember().getId() == self.context.Creator()

    def template_blacklist(self,template_id):
        """Do not show ityou.follow in all templates/views
        """
        print template_id
        if template_id in TEMPLATE_BLACKLIST:
            return True
        return False


    def followText(self):
        """ Returns follow text to show in template
        """
        msgid = _(u"follow_btn" , default=u"Follow ${authorname}", mapping={ u"authorname" : self.authorname().decode("utf-8")})
        return self.context.translate(msgid)

    def unfollowText(self):
        """ Returns Unfollow text to show in template
        """
        msgid = _(u"unfollow_btn" , default=u"${authorname} subscribed", mapping={ u"authorname" : self.authorname().decode("utf-8")})
        return self.context.translate(msgid)

    def followEnabled(self):
        """Is Follow enabled?
        """
        if getUtility(IRegistry).forInterface(IFollowSettings).follow_enable:
            return True
        else:
            return False


class LikeViewlet(BrowserView):
    """Viewlet used to display the Like buttons
    """
    implements(IViewlet)
    render = ViewPageTemplateFile("templates/like.pt")

    def __init__(self, context, request, view=None, manager=None):
        super(LikeViewlet, self).__init__(context, request)
        self.context = context

    def get_auth_user(self):        
        if not api.user.is_anonymous():
            auth_user = api.user.get_current()
        else:
            auth_user = None
        return auth_user

    def likeEnabled(self):
        """Is Like / Voting enabled?
        """
        if getUtility(IRegistry).forInterface(IFollowSettings).like_enable:
            return True

    def template_blacklist(self,template_id):
        """Do not show ityou.follow in all templates/views
        """
        print template_id
        if template_id in TEMPLATE_BLACKLIST:
            return True
        return False



