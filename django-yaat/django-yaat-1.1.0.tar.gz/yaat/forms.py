# coding: utf-8
import json
import six
from copy import deepcopy

from django import forms
from django.db import transaction

from yaat.models import Column


class HeadersField(forms.Field):
    def to_python(self, value):
        if isinstance(value, six.string_types):
            try:
                return json.loads(value)
            except ValueError:
                raise forms.ValidationError('Enter valid JSON')
        return value


class YaatValidatorForm(forms.Form):
    limit = forms.IntegerField(min_value=0, initial=10)
    offset = forms.IntegerField(min_value=0, initial=1)
    headers = HeadersField(required=False)

    def __init__(self, *args, columns, **kwargs):
        self.columns = columns
        self._column_fields = {column.key: i for i, column in enumerate(self.columns)}

        super().__init__(*args, **kwargs)

    def _get_column(self, name):
        retval = deepcopy(self.columns[self._column_fields[name]])
        retval.pk = None
        return retval

    def full_clean(self):
        super().full_clean()

        if 'limit' in self._errors.keys():
            self.cleaned_data['limit'] = self.fields['limit'].initial
            del self._errors['limit']

        if 'offset' in self._errors.keys():
            self.cleaned_data['offset'] = self.fields['offset'].initial
            del self._errors['offset']

        if 'headers' in self._errors.keys():
            self.cleaned_data['headers'] = self.columns
            del self._errors['headers']

    def clean_headers(self):
        posted = self.cleaned_data['headers']

        headers = []

        try:
            for head in posted:
                try:
                    # TODO: Add validaton here
                    col = self._get_column(head['key'])
                    headers.append(col)

                    if col.ordering != Column.ORDER_DISALLOWED:
                        col.ordering = head['order']

                    if col.is_shown != Column.HIDE_DISALLOWED:
                        col.is_shown = not head['hidden']
                except KeyError:
                    raise forms.ValidationError('')
        except TypeError: # None type is not iterable (posted data is None)
            raise forms.ValidationError('')

        return headers

    def save(self, user):
        if self.columns == self.cleaned_data['headers']:
            return

        for i in range(0, len(self.cleaned_data['headers'])):
            self.cleaned_data['headers'][i].order = i + 1
            self.cleaned_data['headers'][i].user = user

        with transaction.atomic():
            col = self.cleaned_data['headers'][0]
            Column.objects.filter(user_id=col.user_id, resource=col.resource).delete()
            Column.objects.bulk_create(self.cleaned_data['headers'])
            Column.cached.bulk_create(self.cleaned_data['headers'])
