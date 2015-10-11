# coding: utf-8

import uuid

from django import template

from sticky_files.models import File


register = template.Library()


@register.assignment_tag()
def get_file_by_id(pk):
    try:
        return File.objects.get(pk=pk)
    except File.DoesNotExist:
        return None


@register.assignment_tag()
def make_unique_id(value):
    return '{}-{}'.format(value, uuid.uuid4())
