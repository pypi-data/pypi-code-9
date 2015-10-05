from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Poll, PollItem, Vote
User = get_user_model()


class PollItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollItem


class PollSerializer(serializers.ModelSerializer):
    pollitem_set = PollItemSerializer(many=True)

    class Meta:
        model = Poll


class VoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        required=False,
        allow_null=True,
        read_only=True,
        default=None)

    class Meta:
        model = Vote
        fields = ('user', 'ip', 'item',)
        read_only_fields = ('user', 'ip')
