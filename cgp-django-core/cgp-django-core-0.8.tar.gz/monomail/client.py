import re
import logging
import traceback
import smtplib

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import get_template
from django.template import Context
from django.template import Template
from django.contrib import messages
from django.utils.safestring import mark_safe

from .models import *

class MonomailClient:
    """
    Monomail Email Client
    =====================
    The Monomail Email Client is a collection of convenience methods for sending
    emails from templates.

    Usage
    -----
    >>> client = MonomailClient()
    >>> client.send_from_template( toemail, "Subject", "path/to/template.html", { 'context' : '' } )
    """

    def __init__( self ):
        pass

    def send( self, toemail, subject, message, message_html = None, headers=None ):
        """
        Send Message
        ============
        Base method for constructing and sending an email message.
        """
        # -- Create Message
        msg = EmailMultiAlternatives( subject, message, self.mailfrom, self._getemail( toemail ), headers=headers )

        # -- Attach HTML Message
        if message_html:
            msg.attach_alternative( message_html, "text/html; charset=UTF-8" )

        # -- Send Message
        msg.send()


    def send_from_template( self, toemail, subject, template_txtid, context = {}, category_txtid=None ):
        """
        Send from Template
        ==================
        Sends an email message from a template.
        """
        
        category = get_category(category_txtid)

        site = Site.objects.get_current()
        site_url = 'https://%s'%(site.domain) if settings.USE_SSL else 'http://%s'%(site.domain)
        headers = {}

        if category:
            category_subscription_settings = get_category_settings_for_user(toemail, category)
            if category_subscription_settings.can_email() == False:
                #User has opted out
                return False
            else:
                if category.can_unsubscribe:
                    headers['List-Unsubscribe'] = '<%s%s>'%(site_url, category_subscription_settings.parent.get_absolute_url())
        else:
            category_subscription_settings = None
            

        receipt = EmailReceipt.create_receipt(toemail, category)
        context['receipt'] = receipt

        #Add additional context vars:
        context['settings'] = settings
        context['site'] = site
        context['site_url'] = site_url
        context['subscription_category'] = category
        context['subscription_settings'] = None if not category_subscription_settings else category_subscription_settings.parent
        context['category_subscription_settings'] = category_subscription_settings

        # -- Get & Render Template
        html_template   = get_template( template_txtid )
        message_html    = html_template.render( Context( context ) )

        # -- Compile HTML Message to Texts
        message         = self._totext( message_html )

        receipt.rendered(subject, message_html)

        # -- Send Message
        try:
            self.send( toemail, subject, message, message_html, headers )
        except smtplib.SMTPException:
            receipt.record_error( traceback.format_exc() )

        


    def send_from_model( self, toemail, txtid, context = {}, category_txtid=None ):
        """
        Send from an Email Template Model
        """
        try:
            email = EmailTemplate.objects.get( txtid = txtid )
        except:
            raise ObjectDoesNotExist()

        site = Site.objects.get_current()
        site_url = 'https://%s'%(site.domain) if settings.USE_SSL else 'http://%s'%(site.domain)
        headers = {}


        category = get_category(category_txtid)
        if category:
            category_subscription_settings = get_category_settings_for_user(toemail, category)
            if category_subscription_settings.can_email() == False:
                if settings.DEBUG:
                    logger.info("Not Sending Email; User %s has opted out of %s emails."%(toemail, category))
                #User has opted out
                return False
            else:
                if category.can_unsubscribe:
                    headers['List-Unsubscribe'] = '<%s%s>'%(site_url, category_subscription_settings.parent.get_absolute_url())
        else:
            category_subscription_settings = None

        
        # -- Render the Subject of the Email
        template        = Template( email.subject )
        subject         = template.render( Context( context ) )

        # -- Render the Body of the Email
        template        = Template( email.rendered )
        body            = template.render( Context( context ) )
        message         = self._totext( body )

        # -- Render the Template

        try:
            html_template = get_template( settings.MONOMAIL['layout'] )
        except:
            raise ImproperlyConfigured( "You must define MONOMAIL_LAYOUT in settings to use this method. This is the path to the HTML layout for your email to send." )

        receipt         = EmailReceipt.create_receipt(toemail, category)
        message_context = {
            'settings': settings,
            'site':site,
            'site_url':site_url,
            'subject' : subject, 
            'email' : toemail, 
            'body' : body, 
            'receipt': receipt,
            'subscription_category': category,
            'subscription_settings': None if not category_subscription_settings else category_subscription_settings.parent,
            'category_subscription_settings': category_subscription_settings
        }
        message_html    = html_template.render( Context( message_context ) )

        receipt.rendered(subject, message_html)

        # -- Send Message
        try:
            self.send( toemail, subject, message, unicode( message_html ), headers )
        except smtplib.SMTPException:
            receipt.record_error( traceback.format_exc() )
        

    @property
    def mailfrom( self ):
        try:
            return "%s <%s>" % ( settings.MONOMAIL['name'], settings.MONOMAIL['email'])
        except:
            raise ImproperlyConfigured( "The following variables must be defined in settings in order to use the emailer: MONOMAIL_NAME, MONOMAIL_EMAIL" )


    def _getemail( self, toemail ):
        """Ensure Email Address is Returned in a List"""
        if isinstance( toemail, str ):
            return [ toemail ]
        elif isinstance( toemail, unicode ):
            return [ toemail ]
        else:
            return toemail


    def _totext( self, data ):
        """Strips HTML from Email for Text Only"""
        p = re.compile(r'<.*?>')
        return p.sub('', data)

def get_settings_for_user(recipient_email):
    notification_settings, created = UserSubscriptionSettings.objects.get_or_create(recipient_email=recipient_email)
    return notification_settings

def get_category_settings_for_user(recipient_email, category):
    notification_settings = get_settings_for_user(recipient_email)
    return notification_settings.get_settings(category)

def get_category(category_txtid=None):
    if not category_txtid:
        return None
    try:
        category = EmailSubscriptionCategory.objects.get(txtid=category_txtid)
    except:
        return None
    return category
