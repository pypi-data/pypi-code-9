# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _

from pybb import defaults, util
from private_messages.models import PrivateMessage


class MessageForm(forms.ModelForm):

    class Meta(object):
        model = PrivateMessage
        fields = ('receivers', 'subject', 'body',)
        widgets = {
            'body': util.get_markup_engine().get_widget_cls(),
        }
        labels = {
            'receivers': _('To'),
        }

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.available_smiles = defaults.PYBB_SMILES
        self.smiles_prefix = defaults.PYBB_SMILES_PREFIX
