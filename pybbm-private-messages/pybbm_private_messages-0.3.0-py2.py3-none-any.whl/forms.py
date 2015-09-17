# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _
from django_select2.widgets import HeavySelect2MultipleWidget
from pybb import util

from private_messages.models import PrivateMessage


class MessageForm(forms.ModelForm):

    parent = forms.UUIDField(required=False, widget=forms.HiddenInput)

    class Meta(object):
        model = PrivateMessage
        fields = ('receivers', 'subject', 'body', 'parent')
        widgets = {
            'body': util.get_markup_engine().get_widget_cls(),
            'receivers': HeavySelect2MultipleWidget(data_view='private_messages:select2')
        }
        labels = {
            'receivers': _('To'),
        }
