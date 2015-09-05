# coding: utf8

# Copyright 2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest

import MockMockMock


def compute_checksum(payload):
    return ~(sum(payload)) & 0xFF


# @todo Extract in exceptions.py (Easier to document)
class CommunicationError(Exception):
    """
    @todoc
    """
    pass


class Bus(object):
    """
    @todoc
    """
    def __init__(self, hardware):
        self.__hardware = hardware

    def send(self, ident, instruction):
        """
        @todoc
        """
        self.__send(ident, instruction)
        return self.__receive(instruction.response_class)

    def broadcast(self, instruction):
        """
        @todoc
        """
        self.__send(0xFE, instruction)

    def __send(self, ident, instruction):
        length = len(instruction.parameters) + 2
        payload = [ident, length, instruction.code] + instruction.parameters
        checksum = compute_checksum(payload)
        packet = [0xFF, 0xFF] + payload + [checksum]
        self.__hardware.send(packet)

    def __receive(self, response_class):
        # @todo Catch and translate exceptions raised by hardware
        ff1, ff2, ident, length = self.__receive_from_hardware(4)
        if ff1 != 0xFF or ff2 != 0xFF:
            raise CommunicationError
        payload = self.__receive_from_hardware(length)
        error = payload[0]
        parameters = payload[1:-1]
        checksum = payload[-1]
        payload = [ident, length, error] + parameters
        if checksum != compute_checksum(payload):
            raise CommunicationError
        return ident, error, response_class(parameters)

    def __receive_from_hardware(self, count):
        payload = self.__hardware.receive(count)
        if len(payload) != count:
            raise CommunicationError
        return payload


class ComputeChecksumTestCase(unittest.TestCase):
    def test(self):
        # From http://support.robotis.com/en/product/dynamixel/communication/dxl_packet.htm
        self.assertEqual(compute_checksum([0x01, 0x05, 0x03, 0x0C, 0x64, 0xAA]), 0xDC)


class BusTestCase(unittest.TestCase):
    class TestInstruction:
        def __init__(self, code, parameters):
            self.code = code
            self.parameters = parameters
            self.response_class = lambda parameters: parameters

    def setUp(self):
        super(BusTestCase, self).setUp()
        self.mocks = MockMockMock.Engine()
        self.hardware = self.mocks.create("hardware")
        self.bus = Bus(self.hardware.object)

    def tearDown(self):
        self.mocks.tearDown()
        super(BusTestCase, self).tearDown()

    def test_send(self):
        # From http://support.robotis.com/en/product/dynamixel/communication/dxl_instruction.htm (example 1)
        self.hardware.expect.send([0xFF, 0xFF, 0x01, 0x04, 0x02, 0x2B, 0x01, 0xCC])
        self.hardware.expect.receive(4).andReturn([0xFF, 0xFF, 0x01, 0x03])
        self.hardware.expect.receive(3).andReturn([0x00, 0x20, 0xDB])
        ident, error, parameters = self.bus.send(0x01, self.TestInstruction(0x02, [0x2B, 0x01]))
        self.assertEqual(ident, 0x01)
        self.assertEqual(error, 0x00)
        self.assertEqual(parameters, [0x20])

    def test_broadcast(self):
        # From http://support.robotis.com/en/product/dynamixel/communication/dxl_instruction.htm (example 2)
        self.hardware.expect.send([0xFF, 0xFF, 0xFE, 0x04, 0x03, 0x03, 0x01, 0xF6])
        self.bus.broadcast(self.TestInstruction(0x03, [0x03, 0x01]))

    def test_hardware_returns_wrong_number_of_bytes(self):
        self.hardware.expect.send([0xFF, 0xFF, 0x01, 0x04, 0x02, 0x2B, 0x01, 0xCC])
        self.hardware.expect.receive(4).andReturn([0xFF, 0xFF, 0x01])
        with self.assertRaises(CommunicationError):
            self.bus.send(0x01, self.TestInstruction(0x02, [0x2B, 0x01]))

    def test_hardware_returns_not_ffff(self):
        self.hardware.expect.send([0xFF, 0xFF, 0x01, 0x04, 0x02, 0x2B, 0x01, 0xCC])
        self.hardware.expect.receive(4).andReturn([0xFE, 0xFF, 0x01, 0x00])
        with self.assertRaises(CommunicationError):
            self.bus.send(0x01, self.TestInstruction(0x02, [0x2B, 0x01]))

    def test_wrong_checksum(self):
        self.hardware.expect.send([0xFF, 0xFF, 0x01, 0x04, 0x02, 0x2B, 0x01, 0xCC])
        self.hardware.expect.receive(4).andReturn([0xFF, 0xFF, 0x01, 0x03])
        self.hardware.expect.receive(3).andReturn([0x00, 0x20, 0xDA])
        with self.assertRaises(CommunicationError):
            self.bus.send(0x01, self.TestInstruction(0x02, [0x2B, 0x01]))
