# -*- coding: utf-8 -*-
## -----------------------------------------------------------------
## Copyright (C)2013 ITYOU - www.ityou.de - support@ityou.de
## -----------------------------------------------------------------
"""
This module contains the interface classes of ityou.follow
"""
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope import schema

_ = MessageFactory('ityou.follow')

class IFollowSettings(Interface):
    """Global follow settings. This describes records stored in the
    configuration registry and obtainable via plone.registry.
    """

    follow_enable = schema.Bool(
            title=_(u"Enable follow"),
            description=_(u"If enabled, user can select the 'follow' function"),
            required=True,
            default=False,
        )

    like_enable = schema.Bool(
            title=_(u"Enable like/dislike"),
            description=_(u"If enabled, the user can like/dislike documents"),
            required=False,
            default=False,
        )

class IFollow(Interface):
    """Marker Interface
    """

class ILike(Interface):
    """Marker Interface
    """



