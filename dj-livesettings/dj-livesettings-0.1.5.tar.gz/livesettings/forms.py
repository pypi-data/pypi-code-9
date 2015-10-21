# coding: utf-8

from django import forms
from django.conf import settings
import ujson
import yaml

from .models import LiveSetting


class LiveSettingsForm(forms.ModelForm):

    def clean(self):
        data = super(LiveSettingsForm, self).clean()
        key = self.cleaned_data['key']
        key_type = self.cleaned_data['key_type']
        value = self.cleaned_data['value']
        try:
            parse_value(value, key_type, key)
        except Exception as e:
            raise forms.ValidationError(str(e))
        return data

    class Meta:
        model = LiveSetting
        exclude = []


def _parse_schematics(value, key):
        try:
            data = ujson.loads(value)
        except ValueError:  # unable to parse json, try yaml
            try:
                data = yaml.load(value)
            except Exception:
                raise ValueError('Please provide valid JSON or YAML')
        model = getattr(settings, key).__class__(data)
        model.validate()
        return model


def parse_value(value, key_type, key):
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
    elif key_type == 'schematics':
        return _parse_schematics(value, key)

    raise TypeError('live_settings: unknown key_type: {0}'.format(key_type))
