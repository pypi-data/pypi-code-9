# coding: utf-8

from django import forms
import ujson
import yaml

from .models import LiveSetting


class LiveSettingsForm(forms.ModelForm):

    def clean(self):
        data = super(LiveSettingsForm, self).clean()
        key_type = self.cleaned_data['key_type']
        value = self.cleaned_data['value']
        try:
            parse_value(value, key_type)
        except Exception as e:
            raise forms.ValidationError(str(e))
        return data

    class Meta:
        model = LiveSetting
        exclude = []


def parse_value(value, key_type):
    if value is None:
        return value
    if key_type == 'bool':
        lower = value.lower()
        if lower == 'true':
            return True
        elif lower == 'false':
            return False
        else:
            return int(value) != 0
    elif key_type == 'int':
        return int(value)
    elif key_type == 'str':
        return str(value)
    elif key_type == 'float':
        return float(value)
    elif key_type == 'json':
        return ujson.loads(value)
    elif key_type == 'yaml':
        return yaml.load(value)

    raise TypeError('live_settings: unknown key_type: {0}'.format(key_type))
