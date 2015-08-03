# -*- coding: utf-8; mode: Python; -*-
from __future__ import unicode_literals

from rest_framework import serializers
from bckt.models import Bckt
from django.contrib.auth.models import User


class BcktSerializer(serializers.HyperlinkedModelSerializer):
    '''
    Default serializer for the Bckt model.

    This serializer handles all the fields of the model exposed via the api.
    '''
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(
        view_name='bckt-highlight',
        format='html'
    )

    class Meta:
        model = Bckt
        fields = ('url', 'highlight', 'owner',
                  'title', 'reqttl',
                  'code',
                  'linenos', 'language', 'style',
                  'created', 'reqttl')


class BcktListSerializer(BcktSerializer):
    '''
    List oriented serializer for the Bckt model

    Based on BcktSerializer, overriding the Meta class to leave bulky fields
    out of the serialization - to achieve more compact lists.
    '''

    class Meta:
        model = Bckt
        fields = ('url', 'highlight', 'owner',
                  'title', 'language', 'created', 'reqttl')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    '''
    Default serializer for the User model.

    This serializer handles the fields relevant for this application.
    '''
    bckts = serializers.HyperlinkedRelatedField(queryset=Bckt.objects.all(),
                                                view_name='bckt-detail',
                                                many=True)

    class Meta:
        model = User
        fields = ('url', 'username', 'bckts')
