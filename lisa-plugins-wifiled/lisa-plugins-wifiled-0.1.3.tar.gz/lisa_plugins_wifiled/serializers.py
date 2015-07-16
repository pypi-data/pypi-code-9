from models import Controller
from rest_framework import serializers
from django.utils.translation import ugettext as _


class ControllerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Controller
        fields = ('url', 'name', 'address', 'port', 'zone')
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }


class PowerSerializer(serializers.Serializer):
    power = serializers.ChoiceField(['on', 'off'])
    groups = serializers.ListField(child=serializers.IntegerField(), default=[], required=False)


class ColorSerializer(serializers.Serializer):
    color = serializers.ChoiceField(
        [
            _('violet'),
            _('royal_blue'),
            _('baby_blue'),
            _('aqua'),
            _('mint'),
            _('seafoam_green'),
            _('green'),
            _('lime_green'),
            _('yellow'),
            _('yellow_orange'),
            _('orange'),
            _('red'),
            _('pink'),
            _('fusia'),
            _('lilac'),
            _('lavendar'),
            _('white')
        ]
    )
    groups = serializers.ListField(child=serializers.IntegerField(), default=[], required=False)
