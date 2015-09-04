from django.conf import settings
from django.core.mail import EmailMessage
from django.core.exceptions import ImproperlyConfigured
from django.template import loader, Context, Template
from django.template.loader import get_template

from .client import MonomailClient
from .models import *

def get_email_template(template):
    try:
        return EmailTemplate.objects.get( txtid = template )
    except:
        return None


def send_mail_template(email, subject_template_string, body_template_string, context={}):
    
    

    c = Context(context)

    # -- Subject
    subject_template = Template(subject_template_string)
    subject = subject_template.render(c)
    subject = ''.join(subject.splitlines())

    # -- Render Email
    body_template = Template(body_template_string)
    body = body_template.render(c)

    from_email = "%s <%s>"%(settings.DEFAULT_FROM_EMAIL_NAME, settings.DEFAULT_FROM_EMAIL)

    try:
        html_template = get_template( settings.MONOMAIL['layout'])
    except:
        raise ImproperlyConfigured( "You must define MONOMAIL_LAYOUT in settings to use this method. This is the path to the HTML layout for your email to send." )

    receipt = EmailReceipt.create_receipt(email)
    message_html = html_template.render( Context( { 'subject' : subject, 'email' : email, 'body' : body, 'receipt':receipt } ) )

    receipt.rendered(subject, message_html)


    msg = EmailMessage(
        subject,
        unicode( message_html ),
        from_email,
        [email])
    msg.content_subtype = "html"
    msg.send()

def send_mail(email, subject_template, template, context={}):
    """
    Send a templated email.
    """

    receipt = EmailReceipt.create_receipt(email)
    context['receipt'] = receipt

    # -- Subject
    subject = loader.render_to_string(subject_template, context)
    subject = ''.join(subject.splitlines())

    # -- Render Email
    t = loader.get_template(template)
    c = Context(context)

    from_email = "%s <%s>"%(settings.DEFAULT_FROM_EMAIL_NAME, settings.DEFAULT_FROM_EMAIL)

    receipt.rendered(subject, t.render(c))

    msg = EmailMessage(
        subject,
        t.render(c),
        from_email,
        [email])
    msg.content_subtype = "html"
    msg.send()

def send_monomail(toemail, template_txtid, context={}, category_txtid=None):

    try:
        m = MonomailClient()
        m.send_from_model( toemail, template_txtid, context, category_txtid )
    except BaseException, error:
        print "Exception %s while sending email type [%s] to %s"%(error, template_txtid, toemail)


        