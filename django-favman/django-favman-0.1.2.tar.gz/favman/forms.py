# -*- coding: utf-8 -*-

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError

class ContentTypeField(forms.CharField): 
    def clean(self, value):
        super(ContentTypeField, self).clean(value)
        if value:
            try:
                return ContentType.objects.get(id=value)
            except ContentType.DoesNotExist:
                raise ValidationError(_(u"The content type {0} doesn't exist").format(value))
        return value

class UpdateFavoriteForm(forms.Form):
    object_id = forms.IntegerField(required=True)
    content_type = ContentTypeField(required=True)
    
    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        if instance:
            kwargs['initial'] = {
                'object_id': instance.id,
                'content_type': ContentType.objects.get_for_model(instance.__class__).id,
            }
        super(UpdateFavoriteForm, self).__init__(*args, **kwargs)

    