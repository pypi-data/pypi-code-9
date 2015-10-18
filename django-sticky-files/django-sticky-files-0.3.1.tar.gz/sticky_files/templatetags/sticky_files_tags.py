# coding: utf-8

import uuid

from django import template
from django.apps import apps


register = template.Library()


@register.assignment_tag()
def get_file_by_id(pk, app, model):
    file_model_class = apps.get_model(app, model)
    try:
        return file_model_class.objects.get(pk=pk)
    except file_model_class.DoesNotExist:
        return None


@register.assignment_tag()
def make_unique_id(value):
    return '{}-{}'.format(value, uuid.uuid4())
