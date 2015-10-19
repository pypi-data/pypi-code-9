import datetime

from django.core.paginator import Page
from django.db import models
from django.utils.encoding import force_text
from django.conf import settings
from django import forms


class BaseSerializer(object):
    formats = ['json']

    def __init__(self, datetime_formatting=None):
        if datetime_formatting is not None:
            self.datetime_formatting = datetime_formatting
        else:
            self.datetime_formatting = getattr(settings, 'RESTIFY_DATETIME_FORMATTING', 'rfc-2822')

    def flatten(self, data):
        """
        For a piece of data, attempts to recognize it and provide a simplified
        form of something complex.

        This brings complex Python data structures down to native types of the
        serialization format(s).
        """
        if isinstance(data, (list, tuple)):
            return [self.flatten(item) for item in data]
        elif isinstance(data, dict):
            return dict((key, self.flatten(val)) for (key, val) in data.items())
        elif isinstance(data, (datetime.datetime, datetime.date)):
            return data
        elif isinstance(data, (int, float)):
            return data
        elif hasattr(data, 'flatten'):
            return data.flatten()

        return force_text(data)


class DjangoSerializer(BaseSerializer):
    def flatten(self, data):
        if isinstance(data, Page):
            retval = {
                'current': data.number,
                'num_pages': data.paginator.num_pages,
                'list': []
            }

            # Previous page
            previous = None
            if data.has_previous():
                number = data.previous_page_number()
                previous = {
                    'key': number,
                    'value': number
                }
            retval['list'].append(previous)

            # Current page must be at index #1 (because reply['pages']['current'] is initialized to 1)
            retval['list'].append({
                'key': data.number,
                'value': data.number
            })

            # Next page
            next = None
            if data.has_next():
                number = data.next_page_number()
                next = {
                    'key': number,
                    'value': number
                }
            retval['list'].append(next)

            return retval

        return super().flatten(data)


class ModelSerializer(DjangoSerializer):
    def __init__(self, serialize_related_fields=True):
        self._serialize_related_fields = serialize_related_fields

    def flatten(self, data):
        if isinstance(data, (forms.ModelForm, forms.Form,)):
            retval = {}
            if data.is_valid() or not data.is_bound:
                for field in data:
                    if hasattr(field.field, 'queryset'): ### ForeignKey, ManyToManyField
                        retval[field.name] = field.value() or ''
                    else:
                        retval[field.name] = field.value()
            else:
                retval = {key: list(value) for key, value in data.errors.items()}
            return retval
        elif isinstance(data, models.Model):
            retval = {}
            for field in data._meta.fields:
                if field.rel and self._serialize_related_fields == False:
                    continue

                if isinstance(field, models.ForeignKey):
                    retval[field.name] = getattr(data, '{0}_id'.format(field.name))
                else:
                    retval[field.name] = self.flatten(getattr(data, field.name))

            return retval

        return super(ModelSerializer, self).flatten(data)
