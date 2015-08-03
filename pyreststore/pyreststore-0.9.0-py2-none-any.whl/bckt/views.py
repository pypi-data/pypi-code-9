# -*- coding: utf-8; mode: Python; -*-
from __future__ import unicode_literals

import logging
import django_filters
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from bckt.models import Bckt
from bckt.permissions import IsOwnerOrReadOnly
from bckt.serializers import BcktSerializer, BcktListSerializer, UserSerializer


class BcktFilter(django_filters.FilterSet):
    '''
    Enable filtering on Bckt regardless of
    the value of the parameter DEFAULT_FILTER_BACKENDS.

    Example: /api/bckt/?owner=admin&title__icontains=test
             /api/bckt/?owner=admin&created=2015-07-26%2017:45:45.316090
             /api/bckt/?owner=admin&created__gt=2015-07-26%2017:50:00

    Please be ware of:
    - https://github.com/tomchristie/django-rest-framework/issues/1338
    - https://code.djangoproject.com/ticket/23448
    - https://github.com/alex/django-filter/pull/264

    '2015-07-26T17:45:45.316090Z'
    url encoded is '2015-07-26T17%3A45%3A45.316090Z'
    '2015-07-26 17:45:45.316090Z'
    url encoded is '2015-07-26%2017%3A45%3A45.316090Z'
    '''
    # Owner is really a relation to an instance of
    # django.contrib.auth.models.User model.
    # Use the username in queries
    owner = django_filters.CharFilter(name="owner__username")

    class Meta:
        model = Bckt
        fields = {
            'owner': ['exact'],
            'language': ['exact'],
            'title': ['exact', 'icontains'],
            'created': ['exact', 'lt', 'gt'],
            'code': ['contains', 'icontains'],
        }


class BcktMultiViewSet(viewsets.ModelViewSet):
    '''
    BcktMultiViewSet is a cusom class based on viewsets.ModelViewSet
    enabeling the use of different serializers in te same model view set
    depending on the action.

    The initial aim was to ommit bulky details from lists, only using them in
    single record views.

    This is achieved by replacing the get_serializer_class method with
    one choosing serializer based on the value of action.
    '''

    serializers = {
        'default': None,
    }
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = BcktFilter

    def get_serializer_class(self):
        # Get an instance of a logger
        logger = logging.getLogger(__name__)
        m = '{:s}: action = {!s}'.format(
            'BcktMultiViewSet.get_serializer_class()',
            self.action)
        logger.debug(m)
        return self.serializers.get(self.action,
                                    self.serializers['default'])


class BcktViewSet(BcktMultiViewSet):
    '''
    This endpoint presents the buckets.

    The `highlight` field presents a hyperlink to the hightlighted HTML
    representation of the bucket.

    The **owner** of the bucket may update or delete instances
    of the bucket.
    '''
    # The class BcktViewSet is derrived from BcktMultiViewSet, which in turn is
    # derrived from viewsets.ModelViewSet to allow for different presentations
    # in lists and detailed views.

    # model = Bckt
    queryset = Bckt.objects.all()

    # The choice of which serializer to use is controlled by serializers
    # instead of a common serializer for all actions
    # (serializer_class = BcktSerializer)
    serializers = {
        'default': BcktSerializer,
        'list': BcktListSerializer,
        'retrieve': BcktSerializer,
    }
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    @detail_route(renderer_classes=(renderers.StaticHTMLRenderer,))
    def highlight(self, request, *args, **kwargs):
        bckt = self.get_object()
        return Response(bckt.highlighted)

    def perform_create(self, serializer):
        # Get an instance of a logger
        logger = logging.getLogger(__name__)
        m = '{:s}: self.action = {!s}'.format(
            'BcktViewSet.perform_create',
            self.action)
        logger.debug(m)
        m = '{:s}: self.request.user = {!s}'.format(
            'BcktViewSet.perform_create',
            self.request.user)
        logger.debug(m)
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This endpoint presents the users in the system.

    The collection of bckt instances owned by a user are
    serialized using a hyperlinked representation.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
