# Copyright (c) 2015 Nicolas JOUANIN
#
# See the file license.txt for copying permission.
import asyncio
from asyncio import IncompleteReadError
from math import ceil

from hbmqtt.errors import NoDataException


def bytes_to_hex_str(data):
    """
    converts a sequence of bytes into its displayable hex representation, ie: 0x??????
    :param data: byte sequence
    :return: Hexadecimal displayable representation
    """
    return '0x' + ''.join(format(b, '02x') for b in data)

def bytes_to_int(data):
    """
    convert a sequence of bytes to an integer using big endian byte ordering
    :param data: byte sequence
    :return: integer value
    """
    if isinstance(data, int):
        return data
    else:
        return int.from_bytes(data, byteorder='big')

def int_to_bytes(int_value: int, length=-1) -> bytes:
    """
    convert an integer to a sequence of bytes using big endian byte ordering
    :param int_value: integer value to convert
    :param length: (optional) byte length
    :return: byte sequence
    """
    if length == -1:
        length = ceil(int_value.bit_length()//8)
        if length == 0:
            length = 1
    return int_value.to_bytes(length, byteorder='big')


@asyncio.coroutine
def read_or_raise(reader, n=-1):
    """
    Read a given byte number from Stream. NoDataException is raised if read gives no data
    :param reader: Stream reader
    :param n: number of bytes to read
    :return: bytes read
    """
    try:
        data = yield from reader.readexactly(n)
    except IncompleteReadError:
        raise NoDataException("Incomplete read")
    if not data:
        raise NoDataException("No more data")
    return data

@asyncio.coroutine
def decode_string(reader) -> bytes:
    """
    Read a string from a reader and decode it according to MQTT string specification
    :param reader: Stream reader
    :return: UTF-8 string read from stream
    """
    length_bytes = yield from read_or_raise(reader, 2)
    str_length = bytes_to_int(length_bytes)
    byte_str = yield from read_or_raise(reader, str_length)
    return byte_str.decode(encoding='utf-8')

@asyncio.coroutine
def decode_data_with_length(reader) -> bytes:
    """
    Read data from a reader. Data is prefixed with 2 bytes length
    :param reader: Stream reader
    :return: bytes read from stream (without length)
    """
    length_bytes = yield from read_or_raise(reader, 2)
    bytes_length = bytes_to_int(length_bytes)
    data = yield from read_or_raise(reader, bytes_length)
    return data

def encode_string(string: str) -> bytes:
    data = string.encode(encoding='utf-8')
    data_length = len(data)
    return int_to_bytes(data_length, 2) + data

def encode_data_with_length(data: bytes) -> bytes:
    data_length = len(data)
    return int_to_bytes(data_length, 2) + data

@asyncio.coroutine
def decode_packet_id(reader) -> int:
    """
    Read a packet ID as 2-bytes int from stream according to MQTT specification (2.3.1)
    :param reader: Stream reader
    :return: Packet ID
    """
    packet_id_bytes = yield from read_or_raise(reader, 2)
    return bytes_to_int(packet_id_bytes)
