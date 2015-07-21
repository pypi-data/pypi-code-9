from lisa_plugins_shopping.models import ShoppingList
from rest_framework import viewsets, status
from rest_framework.response import Response
from lisa_plugins_shopping.serializers import ShoppingListSerializer, ItemSerializer
from rest_framework.decorators import detail_route
from lisa_api.lisa.logger import logger
from django.utils.translation import ugettext as _


class ShoppingListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to add/edit/delete shopping lists.
    """
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer
    lookup_field = 'name'

    @detail_route(methods=['POST'], serializer_class=ItemSerializer)
    def item_delete(self, request, name=None):
        """
        This function manage the jsonfield of a shopping list to delete an item
        :param request:
        :param name:
        :return:

        Example (if the shopping list name is 'default'):
        curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8000/api/v1/plugin-shopping/lists/default/item_delete/ --data '{"items": ["carotte", "chocolat"]}
        ---
        request_serializer: ItemSerializer
        response_serializer: ItemSerializer
        """
        list = self.get_object()
        json_list = list.list

        if not json_list.get('items'):
            json_list = {'items': []}

        if request.method == 'POST':
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid():
                for item in serializer.data['items']:
                    if item in json_list['items']:
                        json_list['items'].remove(item)
                        logger.debug('Removing item {item} of the list'.format(item=item))
                    else:
                        logger.debug('Item {item} does not exist'.format(item=item))
                list.list = json_list
                list.save()
                return Response(_('Item {items} has been removed from the list').format(
                    items=', '.join(serializer.data['items'])), status=status.HTTP_202_ACCEPTED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['POST'], serializer_class=ItemSerializer)
    def item_add(self, request, name=None):
        """
        This function manage the jsonfield of a shopping list by adding a product
        :param request:
        :param name:
        :return:

        Example (if the shopping list name is 'default'):
        curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8000/api/v1/plugin-shopping/lists/default/item_add/ --data '{"items": ["carotte", "chocolat"]}
        ---
        request_serializer: ItemSerializer
        response_serializer: ItemSerializer
        """
        list = self.get_object()
        json_list = list.list

        if not json_list.get('items'):
            json_list = {'items': []}

        if request.method == 'POST':
            serializer = ItemSerializer(data=request.data)
            if serializer.is_valid():
                logger.debug(serializer.data['items'])
                for item in serializer.data['items']:
                    if item not in json_list['items']:
                        json_list['items'].append(item)
                        logger.debug('Adding item {item} to the list'.format(item=item))
                    else:
                        logger.debug('Item {item} already exist'.format(item=item))
                list.list = json_list
                list.save()
                return Response(_('Item {items} has been added to the list').format(
                    items=', '.join(serializer.data['items'])), status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['GET'], serializer_class=ItemSerializer)
    def item_list(self, request, name=None):
        """
        This function manage the jsonfield of a shopping list by listing all products.
        :param request:
        :param name:
        :return:

        Example (if the shopping list name is 'default'):
        curl -X GET -H "Content-Type: application/json" http://127.0.0.1:8000/api/v1/plugin-shopping/lists/default/item_list/
        ---
        request_serializer: ItemSerializer
        response_serializer: ItemSerializer
        """
        list = self.get_object()

        if request.method == 'GET':
            if 'items' in list.list:
                if len(list.list['items']) < 1:
                    return Response(_('You have nothing on your list {list_name}').format(
                                    list_name=name
                                    ), status=status.HTTP_200_OK)
                else:
                    return Response(_('You have {items} on your list {list_name}').format(
                                    items=', '.join(list.list['items']),
                                    list_name=name
                                    ), status=status.HTTP_200_OK)
