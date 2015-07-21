from lisa_plugins_shopping.models import ShoppingList
from rest_framework import serializers


class ShoppingListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ShoppingList
        fields = ('url', 'name', 'list')
        extra_kwargs = {
            'url': {'lookup_field': 'name'}
        }


class ItemSerializer(serializers.Serializer):
    items = serializers.ListField(child=serializers.CharField())
