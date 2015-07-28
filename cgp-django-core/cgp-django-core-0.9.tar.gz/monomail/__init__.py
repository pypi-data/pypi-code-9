import re

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import get_template
from django.template import Context
from django.template import Template
from django.contrib import messages
from django.utils.safestring import mark_safe


from .models import EmailTemplate
from .client import MonomailClient

try:
    from .tasks import task_send_from_model, task_send_from_template
except:
    pass

class Monomail:
    """
    Monomail Email Client
    =====================
    The Monomail Email Client is a collection of convenience methods for sending
    emails from templates.
    
    Usage
    -----
    >>> m = Monomail()
    >>> m.send_from_template( toemail, "Subject", "path/to/template.html", { 'context' : '' } )
    >>> m.send_from_model( toemail, "txt-id-of-record", { 'context' : '' } )
    """
    
    def __init__( self ):
        pass

    def send_from_template( self, toemail, subject, template, context = {} ):
        """
        Send from Template
        ==================
        Will attempt to send the email asyncronously via Celery before falling
        back to call _send_from_template syncronously.
        """
        try:
            task_send_from_template.delay( toemail, subject, template, context )
        except:
            c = MonomailClient()
            c.send_from_template( toemail, subject, template, context )
        
    def send_from_model( self, toemail, txtid, context = {} ):
        """
        Send from Model
        ===============
        Will attempt to send the email asyncronously via Celery before falling
        back to call _send_from_template syncronously.
        """
        try:
            task_send_from_model.delay( toemail, txtid, context )
        except:
            c = MonomailClient()
            c._send_from_model( self, toemail, txtid, context )