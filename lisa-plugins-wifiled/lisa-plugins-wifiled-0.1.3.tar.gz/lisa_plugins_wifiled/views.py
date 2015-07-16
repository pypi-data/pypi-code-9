from models import Controller
from serializers import ControllerSerializer, PowerSerializer, ColorSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from lisa_api.lisa.logger import logger
# from lisa_api.api.decorators import add_intent
from django.utils.translation import ugettext as _
import wifileds


class ControllerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to add/edit/delete controller.
    """
    queryset = Controller.objects.all()
    serializer_class = ControllerSerializer
    lookup_field = 'name'

    @detail_route(methods=['POST'], serializer_class=PowerSerializer)
    def turn_power(self, request, name=None):
        """
        This function manage the power on or off for all or a group of lights.
        :param request:
        :param pk:
        :return:

        If no group is set, the default is to apply the command on all

        Example :
        curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8000/api/v1/plugin-wifiled/controllers/default/turn_power/ --data '{"power": "on", "groups": [1, 2]}'
        ---
        request_serializer: PowerSerializer
        response_serializer: PowerSerializer
        """

        controller = self.get_object()

        serializer = PowerSerializer(data=request.data)
        if serializer.is_valid():
            logger.debug('Create a connection to the wifi bridge {controller_name}'.format(
                controller_name=controller.name
            ))
            led_connection = wifileds.limitlessled.connect(controller.address, controller.port)
            if serializer.data['groups']:
                for group in serializer.data['groups']:
                    if serializer.data['power'] == 'on':
                        led_connection.rgbw.zone_on(group)
                        led_connection.white.zone_on(group)
                        led_connection.rgb.zone_on(group)
                        logger.debug('Turning on the lights for the group {group_name}'.format(group_name=group))
                    else:
                        led_connection.rgbw.zone_off(group)
                        led_connection.white.zone_off(group)
                        led_connection.rgb.zone_off(group)
                        logger.debug('Turning off the lights for the group {group_name}'.format(group_name=group))
            else:
                if serializer.data['power'] == 'on':
                    led_connection.rgbw.all_on()
                    led_connection.white.all_on()
                    led_connection.rgb.all_on()
                    logger.debug('Turning on the lights')
                else:
                    led_connection.rgbw.all_off()
                    led_connection.white.all_off()
                    led_connection.rgb.all_off()
                    logger.debug('Turning off the lights')

            if serializer.data['power'] == 'on':
                # Translators: This message is the state of the lights
                power_state = _('on')
            else:
                # Translators: This message is the state of the lights
                power_state = _('off')

            return Response(_('Light has been turned {power_state}').format(
                power_state=power_state, status=status.HTTP_200_OK))
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['POST'],)
    def change_color(self, request, name=None):
        """
        This function manage the color for all or a group of lights.
        :param request:
        :param pk:
        :return:

        If no group is set, the default is to apply the command on all

        Example :
        curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8000/api/v1/plugin-wifiled/controllers/1/change_color/ --data '{"color": "yellow", "groups": [1, 2]}'
        ---
        request_serializer: ColorSerializer
        response_serializer: ColorSerializer
        """

        controller = self.get_object()

        serializer = ColorSerializer(data=request.data)
        if serializer.is_valid():
            logger.debug('Create a connection to the wifi bridge {controller_name}'.format(
                controller_name=controller.name
            ))
            led_connection = wifileds.limitlessled.connect(controller.address, controller.port)
            if serializer.data['groups']:
                for group in serializer.data['groups']:
                    if serializer.data['color'] == _('white'):
                        led_connection.rgb.white(group)
                        led_connection.rgbw.white(group)
                    else:
                        led_connection.rgb.set_color(serializer.data['color'], group)
                        led_connection.rgbw.set_color(serializer.data['color'], group)
                    logger.debug('Changing the color of the lights to {color} for group {group}'.format(
                        color=serializer.data['color'],
                        group=group
                    ))
            else:
                if serializer.data['color'] == _('white'):
                        led_connection.rgb.white()
                        led_connection.rgbw.white()
                else:
                    led_connection.rgb.set_color(serializer.data['color'])
                    led_connection.rgbw.set_color(serializer.data['color'])
                logger.debug('Changing the color of the lights to {color}'.format(
                    color=serializer.data['color'],
                ))

            return Response(_('Color has been changed to {color}').format(
                color=serializer.data['color']), status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
