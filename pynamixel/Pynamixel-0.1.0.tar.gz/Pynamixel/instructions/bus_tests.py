# coding: utf8

# Copyright 2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest

import MockMockMock

from ..bus import Bus
from .ping import Ping
from .read_data import ReadData
from .write_data import WriteData
from .reg_write import RegWrite
from .action import Action
from .reset import Reset
from .sync_write import SyncWrite


class InstructionsOnBusTestCase(unittest.TestCase):
    def setUp(self):
        super(InstructionsOnBusTestCase, self).setUp()
        self.mocks = MockMockMock.Engine()
        self.hardware = self.mocks.create("hardware")
        self.bus = Bus(self.hardware.object)

    def tearDown(self):
        self.mocks.tearDown()
        super(InstructionsOnBusTestCase, self).tearDown()

    def test_ping(self):
        self.hardware.expect.send([0xFF, 0xFF, 0x07, 0x02, 0x01, 0xF5])
        self.hardware.expect.receive(4).andReturn([0xFF, 0xFF, 0x07, 0x02])
        self.hardware.expect.receive(2).andReturn([0x00, 0xF6])
        self.bus.send(0x07, Ping())

    def test_read_data(self):
        # http://support.robotis.com/en/product/dynamixel/communication/dxl_instruction.htm (example 1)
        self.hardware.expect.send([0xFF, 0xFF, 0x01, 0x04, 0x02, 0x2B, 0x01, 0xCC])
        self.hardware.expect.receive(4).andReturn([0xFF, 0xFF, 0x01, 0x03])
        self.hardware.expect.receive(3).andReturn([0x00, 0x20, 0xDB])
        ident, error, response = self.bus.send(0x01, ReadData(0x2B))
        self.assertEqual(response.data, [0x20])

    def test_write_data(self):
        self.hardware.expect.send([0xFF, 0xFF, 0x01, 0x06, 0x03, 0x2B, 0x10, 0x11, 0x12, 0x97])
        self.hardware.expect.receive(4).andReturn([0xFF, 0xFF, 0x07, 0x02])
        self.hardware.expect.receive(2).andReturn([0x00, 0xF6])
        self.bus.send(0x01, WriteData(0x2B, [0x10, 0x11, 0x12]))

    def test_reg_write(self):
        self.hardware.expect.send([0xFF, 0xFF, 0x01, 0x06, 0x04, 0x2B, 0x10, 0x11, 0x12, 0x96])
        self.hardware.expect.receive(4).andReturn([0xFF, 0xFF, 0x07, 0x02])
        self.hardware.expect.receive(2).andReturn([0x00, 0xF6])
        self.bus.send(0x01, RegWrite(0x2B, [0x10, 0x11, 0x12]))

    def test_action(self):
        self.hardware.expect.send([0xFF, 0xFF, 0x07, 0x02, 0x05, 0xF1])
        self.hardware.expect.receive(4).andReturn([0xFF, 0xFF, 0x07, 0x02])
        self.hardware.expect.receive(2).andReturn([0x00, 0xF6])
        self.bus.send(0x07, Action())

    def test_reset(self):
        self.hardware.expect.send([0xFF, 0xFF, 0x07, 0x02, 0x06, 0xF0])
        self.hardware.expect.receive(4).andReturn([0xFF, 0xFF, 0x07, 0x02])
        self.hardware.expect.receive(2).andReturn([0x00, 0xF6])
        self.bus.send(0x07, Reset())

    def test_sync_write(self):
        # http://support.robotis.com/en/product/dynamixel/communication/dxl_instruction.htm (example 5)
        self.hardware.expect.send([
            0xFF, 0xFF, 0xFE, 0x18, 0x83, 0x1E, 0x04,
            0x00, 0x10, 0x00, 0x50, 0x01,
            0x01, 0x20, 0x02, 0x60, 0x03,
            0x02, 0x30, 0x00, 0x70, 0x01,
            0x03, 0x20, 0x02, 0x80, 0x03,
            0x12,
        ])
        self.bus.broadcast(SyncWrite(
            0x1E,
            {
                0: [0x10, 0x00, 0x50, 0x01],
                1: [0x20, 0x02, 0x60, 0x03],
                2: [0x30, 0x00, 0x70, 0x01],
                3: [0x20, 0x02, 0x80, 0x03],
            }
        ))
