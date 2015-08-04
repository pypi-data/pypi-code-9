from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from lisa_api.api.models import Plugin, Client, Zone, Intent
from lisa_api.lisa.configuration import CONF as config
from rest_framework import viewsets, permissions
from lisa_api.api.serializers import (UserSerializer, GroupSerializer,
                                      PluginSerializer, SpeakSerializer,
                                      TTSSerializer, ClientSerializer,
                                      ZoneSerializer, IntentSerializer)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from stevedore import driver
from lisa_api.lisa.logger import logger
from django.utils.translation import ugettext as _
from django.conf import settings
import os
import pip


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ZoneViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows zones to be viewed or edited.
    """
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows clients to be viewed or edited.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class IntentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows intents to be viewed or edited.
    """
    queryset = Intent.objects.all()
    serializer_class = IntentSerializer
    lookup_field = 'name'


class PluginViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows plugins to be viewed or edited.
    """
    queryset = Plugin.objects.all()
    serializer_class = PluginSerializer
    lookup_field = 'name'

    def _touch(self, fname, times=None):
        with open(fname, 'a'):
            os.utime(fname, times)

    def perform_create(self, serializer):
        instance = serializer.save()
        version_str = ''
        if instance.version:
            version_str = ''.join(["==", instance.version])
        pip.main(['install', 'lisa-plugins-' + instance.name + version_str])
        if settings.BASE_DIR:
            self._touch(fname='/'.join([settings.BASE_DIR, '__init__.py']))
        logger.info(msg="Plugin installed")

    def perform_destroy(self, instance):
        pip.main(['uninstall', '--yes', 'lisa-plugins-' + instance.name])
        instance.delete()
        if settings.BASE_DIR:
            self._touch(fname='/'.join([settings.BASE_DIR, '__init__.py']))
        logger.info(msg="Delete plugin")

    def perform_update(self, serializer):
        instance = serializer.save()
        version_str = ''
        if instance.version:
            version_str = ''.join(["==", instance.version])
        pip.main(['install', 'lisa-plugins-' + instance.name + version_str])
        logger.info(msg="Plugin updated")


@api_view(['POST'])
def SpeakView(request, format=None):
    """
    API endpoint that allows to send a message to rabbitmq to vocalize it.
    ---
    request_serializer: SpeakSerializer
    response_serializer: SpeakSerializer
    """
    if request.method == 'POST':
        serializer = SpeakSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data.get('driver'):
                speak = serializer.data.get('driver')
            else:
                speak = config.api.speak
            try:
                mgr = driver.DriverManager(
                    namespace='lisa.api.speak',
                    name=speak,
                    invoke_on_load=True,
                )
                message = mgr.driver.send_message(message=serializer.data.get('message'),
                                                  zone=serializer.data.get('zone'),
                                                  source=serializer.data.get('source'))
                if message:
                    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except RuntimeError:
                return Response(_('Driver {speak} not found').format(speak=speak),
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', 'GET'])
@permission_classes([permissions.AllowAny])
def TTSView(request, format=None):
    """
    API endpoint that allows to do text to speech.
    ---
    request_serializer: TTSSerializer
    response_serializer: TTSSerializer
    """
    if request.method == "POST":
        serializer = TTSSerializer(data=request.data)
    else:
        serializer = TTSSerializer(data=request.GET)
    if serializer.is_valid():
        if serializer.data.get('driver'):
            tts = serializer.data.get('driver')
        else:
            tts = config.api.tts

        try:
            mgr = driver.DriverManager(
                namespace='lisa.api.tts',
                name=tts,
                invoke_on_load=True,
            )
            sound = mgr.driver.convert(message=serializer.data.get('message'),
                                       lang=serializer.data.get('lang'))
            if sound:
                return HttpResponse(sound,
                                    content_type="audio/mpeg")
            else:
                return Response('',
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except RuntimeError:
            return Response(_('Driver {tts} not found').format(tts=tts),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
