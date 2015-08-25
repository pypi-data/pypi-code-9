# -*- coding: utf-8 -*-
from django import template
from django.template.base import Variable, VariableDoesNotExist
from favman.forms import UpdateFavoriteForm
from favman.models import Favorite
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType

register = template.Library()

@register.inclusion_tag('favman/_media.html', takes_context=True)
def fav_media(context):
    return {}
    
@register.inclusion_tag('favman/_item.html', takes_context=True)
def fav_item(context, object):
    ct = ContentType.objects.get_for_model(object.__class__)
    user = context['request'].user
    if user and user.is_authenticated():
        is_in_favorite = Favorite.objects.filter(
            user = context['request'].user,
            content_type = ct,
            object_id = object.id
        ).count()
    else:
        is_in_favorite = 0

    return {
        'status': 'in-fav' if is_in_favorite else 'out-fav',
        'post_url': reverse('favman_toggle'),
        'form': UpdateFavoriteForm(instance=object),
    }