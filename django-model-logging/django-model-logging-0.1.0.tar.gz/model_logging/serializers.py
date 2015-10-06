import json

from rest_framework.serializers import (
    CharField,
    Field,
    ModelSerializer,
)

from . import models


class JSONField(Field):
    def to_representation(self, obj):
        return json.loads(obj)


class LogEntrySerializer(ModelSerializer):
    data = JSONField()
    creator = CharField(source='creator.email')
    operation_label = CharField(source='get_operation_display', read_only=True)

    class Meta:
        model = models.LogEntry
        fields = (
            'date_created', 'creator', 'operation', 'operation_label', 'data',
        )
        read_only_fields = fields
