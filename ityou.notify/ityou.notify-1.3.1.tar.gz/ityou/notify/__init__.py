# -*- coding: utf-8 -*-
from zope.i18nmessageid import MessageFactory
_ = MessageFactory("ityou.notify")

# Apps that can send notifications
ASTREAM      = "astream"
IMESSAGE     = "imessage"

# DEBUG = True -> send email to debug-email address
DEBUG = False   
DEBUG_EMAIL_ADR = 'XXXXX@YYYYYY.ZZ'

# /DEBUG -----------------------------------------

# --- mail template
# TODO: Übersetzungen
SUBJECT = {
    "astream"    : _(u"Document(s) had been created/updated"),
    "imessage"   : _(u"New message from %(sender_name)s"),
}

BODY = {
    "astream"   : _(u"""Hello %(receiver_name)s, here is a list of newly created or modified documents:

    %(body)s
"""),
    "imessage"  : _(u"""Hello %(receiver_name)s, You received a new message from %(sender_name)s:

    <------ Begin ----------------->

    %(message)s

    <------ End ------------------->

Please click here to see the message: %(content_url)s""")
}


# --- /mail template

# --- /Notify Mail params ------------------------


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
