from django.contrib.auth.models import User, Group
from lisa_api.api.models import Plugin, Client, Zone, Intent
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'first_name', 'last_name', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class PluginSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Plugin
        fields = ('url', 'name', 'version')
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }


class IntentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Intent
        fields = ('url', 'name', 'method', 'api_url')
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Client
        fields = ('url', 'name', 'mac', 'zones')


class ZoneSerializer(serializers.HyperlinkedModelSerializer):
    clients = ClientSerializer(many=True, read_only=True)

    class Meta:
        model = Zone
        fields = ('url', 'name', 'clients')


class SpeakSerializer(serializers.Serializer):
    message = serializers.CharField(required=True, allow_blank=False)
    zone = serializers.CharField(required=False, allow_blank=True, max_length=100)
    source = serializers.CharField(required=True, allow_blank=True, max_length=50)
    driver = serializers.CharField(required=False, allow_blank=True, max_length=50)

    class Meta:
        fields = ('zone', 'message', 'source', 'driver')


class TTSSerializer(serializers.Serializer):
    message = serializers.CharField(required=True, allow_blank=False)
    lang = serializers.CharField(required=False, allow_blank=True, max_length=5)
    driver = serializers.CharField(required=False, allow_blank=True, max_length=50)

    class Meta:
        fields = ('message', 'lang', 'driver')
