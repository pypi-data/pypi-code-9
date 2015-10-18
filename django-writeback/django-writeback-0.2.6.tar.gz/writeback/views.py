# -*- coding: utf-8 -*-

import json

from django.views.generic.edit import CreateView
from django.http import HttpResponse
from django.forms import ModelForm, ValidationError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from writeback.models import Message
from django.conf import settings


class MessageCreateForm(ModelForm):
    """
    A form introduced merely for cleaning purposes.
    """
    class Meta:
        model = Message

    def clean(self):
        cleaned_data = super(MessageCreateForm, self).clean()
        name = cleaned_data.get("name")
        family_name = cleaned_data.get("family_name")
        company = cleaned_data.get("company")
        phone = cleaned_data.get("phone")
        email = cleaned_data.get("email")
        info = cleaned_data.get("info")

        if not (name or family_name or company or phone or email or info):
            raise ValidationError(_("Please, fill out at least one field."))

        return super(MessageCreateForm, self).clean()


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageCreateForm
    template_name = 'writeback/button.html'
    success_url = '.'

    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(MessageCreateView, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        form.save()
        context = {'form': form}
        message = render_to_string('writeback/email_notification.html', context)
        msg = EmailMultiAlternatives(settings.WRITEBACK_EMAIL_NOTIFICATION_SUBJECT, message,
                                     settings.WRITEBACK_EMAIL_NOTIFICATION_FROM,
                                     settings.WRITEBACK_EMAIL_NOTIFICATION_TO_LIST)
        msg.content_subtype = "html"
        msg.send()
        if self.request.is_ajax():
            return HttpResponse()
        else:
            return HttpResponseRedirect(self.get_success_url())
