# -*- coding: utf-8 -*-
import re

from django import forms
from django.conf import settings
from django.core.validators import validate_email
from django.utils.translation import ugettext_lazy as _
from django.forms.util import ErrorList
from django.contrib.sites.models import Site
from django.template import Context
from django.template import Template
from django.core.urlresolvers import reverse

from form.forms import Form
from form.widgets import *

from .models import SocialShareSettings




class EmailsListField(forms.CharField):

    SEPARATOR_RE = re.compile(r'[,;]+')


    def clean(self, value):
        super(EmailsListField, self).clean(value)

        emails = EmailsListField.SEPARATOR_RE.split(value)
        emails = [email.strip() for email in emails]
        unique_emails = list(set(emails))

        if len(unique_emails) < 1:
            raise ValidationError(_(u'Enter at least one e-mail address.'))

        for email in unique_emails:
            validate_email(email)

        return unique_emails

class EmailForm( Form ):


    to_email = EmailsListField(widget=TextInputWidget(attrs={'placeholder': 'Enter recipient email address(es)'}), 
        help_text='Separate multple addresses with commas', required=True)
    from_email = forms.EmailField(widget=TextInputWidget(attrs={'placeholder': 'Enter your email address'}),
        required=True)

    subject = forms.CharField(widget=TextInputWidget(attrs={'placeholder': 'Enter email subject'}),
        required=True)
    message = forms.CharField(widget=TextareaWidget(attrs={'placeholder': 'Your email message'}), required=True)
    
    topic = forms.CharField(widget=HoneypotWidget(), required=False) #NOTE -- THIS IS A HONEYPOT
    redirect = forms.CharField(widget=forms.HiddenInput(), required=False)
    title = forms.CharField(widget=forms.HiddenInput(), required=False)
    url = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, url, title, data=None, files=None, auto_id='id_%s', prefix=None,
                 initial=None, error_class=ErrorList, label_suffix=None,
                 empty_permitted=False):

        if initial==None:
            initial = {}

        context = {}

        context['url'] = initial['redirect'] = initial['url'] = url
        context['title'] = initial['title'] = title
        context['site'] = Site.objects.get_current()
        

        settings = SocialShareSettings.get_site_settings()
        if settings:
            form_settings = settings.get_email_form_settings()

            if form_settings:
                template_context = Context( context )
                subject_template = Template( form_settings.title_template )
                subject_rendered = subject_template.render( template_context )

                message_template = Template( form_settings.description_template )
                message_rendered = message_template.render( template_context )

                initial['subject'] = subject_rendered
                initial['message'] = message_rendered

        super(EmailForm, self).__init__(data, files, auto_id, prefix, initial,
            error_class, label_suffix, empty_permitted)

    def get_action_url(self):
        return reverse('share_by_email_view')

    
    def clean_topic(self):
        #validate honeypot
        topic_value = self.cleaned_data['topic']
        if topic_value != None and topic_value != '':
            raise forms.ValidationError("Invalid value")
        return ''


