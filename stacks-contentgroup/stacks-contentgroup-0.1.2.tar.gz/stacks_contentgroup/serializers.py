from django.conf import settings
from django.utils.text import slugify

from rest_framework import serializers
from textplusstuff.serializers import (
    ExtraContextSerializerMixIn,
    TextPlusStuffFieldSerializer
)
from versatileimagefield.serializers import VersatileImageFieldSerializer

from .models import Content, ContentGroup

image_sets = getattr(
    settings,
    'VERSATILEIMAGEFIELD_RENDITION_KEY_SETS',
    {}
).get(
    'stacks_contentgroup',
    [
        ('full_size', 'url'),
        ('3up_thumb', 'crop__700x394'),
        ('2up_thumb', 'crop__800x450'),
        ('full_width', 'crop__1600x901'),
    ]
)


class ContentSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    menu_image = VersatileImageFieldSerializer(
        sizes=image_sets
    )
    alternate_menu_image = VersatileImageFieldSerializer(
        sizes=image_sets
    )
    content = TextPlusStuffFieldSerializer()

    class Meta:
        model = Content
        fields = (
            'id',
            'title',
            'menu_image',
            'alternate_menu_image',
            'content'
        )

    def get_id(self, obj):
        return "{}-{}-{}".format(
            slugify(obj.group.display_title),
            obj.group.pk,
            obj.pk
        )


class ContentGroupSerializer(ExtraContextSerializerMixIn,
                             serializers.ModelSerializer):
    content = ContentSerializer(source='content_set', many=True)

    class Meta:
        model = ContentGroup
        fields = (
            'display_title',
            'name',
            'content'
        )
