# Copyright (c) 2015 Nicolas JOUANIN
#
# See the file license.txt for copying permission.
from hbmqtt.errors import HBMQTTException
from hbmqtt.mqtt.packet import MQTTFixedHeader, MQTTPacket, PacketType
from hbmqtt.mqtt.connect import ConnectPacket
from hbmqtt.mqtt.connack import ConnackPacket
from hbmqtt.mqtt.disconnect import DisconnectPacket
from hbmqtt.mqtt.pingreq import PingReqPacket
from hbmqtt.mqtt.pingresp import PingRespPacket
from hbmqtt.mqtt.publish import PublishPacket
from hbmqtt.mqtt.puback import PubackPacket
from hbmqtt.mqtt.pubrec import PubrecPacket
from hbmqtt.mqtt.pubrel import PubrelPacket
from hbmqtt.mqtt.pubcomp import PubcompPacket
from hbmqtt.mqtt.subscribe import SubscribePacket
from hbmqtt.mqtt.suback import SubackPacket
from hbmqtt.mqtt.unsubscribe import UnsubscribePacket
from hbmqtt.mqtt.unsuback import UnsubackPacket

packet_dict = {
    PacketType.CONNECT: ConnectPacket,
    PacketType.CONNACK: ConnackPacket,
    PacketType.PUBLISH: PublishPacket,
    PacketType.PUBACK: PubackPacket,
    PacketType.PUBREC: PubrecPacket,
    PacketType.PUBREL: PubrelPacket,
    PacketType.PUBCOMP: PubcompPacket,
    PacketType.SUBSCRIBE: SubscribePacket,
    PacketType.SUBACK: SubackPacket,
    PacketType.UNSUBSCRIBE: UnsubscribePacket,
    PacketType.UNSUBACK: UnsubackPacket,
    PacketType.PINGREQ: PingReqPacket,
    PacketType.PINGRESP: PingRespPacket,
    PacketType.DISCONNECT: DisconnectPacket
}

def packet_class(fixed_header: MQTTFixedHeader):
    try:
        cls = packet_dict[fixed_header.packet_type]
        return cls
    except KeyError:
        raise HBMQTTException("Unexpected packet Type '%s'" % fixed_header.packet_type)