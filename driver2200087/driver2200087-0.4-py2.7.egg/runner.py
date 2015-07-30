#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) 2015 Chintalagiri Shashank
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
This module provides an asynchronous backend to the RadioShack 2200087
multimeter's PC interface. It uses crochet to provide a synchronous API
to an underlying Twisted based implementation. While the intent of this
script is to allow the use of the device from within a larger framework,
the use of crochet should allow the use of this API and therefore the
instrument in a naive python script as well.

See the 'main' section of this file for a minimal example of it's usage.
"""


from collections import deque

from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
from twisted.internet.protocol import connectionDone
from twisted.internet.serialport import SerialPort

from serialDecoder import process_chunk

from crochet import setup
from crochet import run_in_reactor
from crochet import wait_for

from twisted.internet import reactor


def unwrap_failures(err):
    """
    Takes nested failures and flattens the nodes into a list.
    The branches are discarded.
    """
    errs = []
    check_unwrap = [err]
    while len(check_unwrap) > 0:
        err = check_unwrap.pop()
        if hasattr(err.value, 'reasons'):
            errs.extend(err.value.reasons)
            check_unwrap.extend(err.value.reasons)
        else:
            errs.append(err)
    return errs


class InstProtocol2200087(Protocol):
    """
    This is a twisted protocol which handles serial communications with
    2200087 multimeters. This protocol exists and operates within the context
    of a twisted reactor. Applications themselves built on twisted should be
    able to simply import this protocol (or its factory).

    If you would like the protocol to produce datapoints in a different format,
    this protocol should be sub-classed in order to do so. The changes necessary
    would likely begin in this class's frame_recieved() function.

    Synchronous / non-twisted applications should use the InstInterface2200087
    class instead. The InstInterface2200087 class accepts a parameter to specify
    which protocol factory to use, in case you intend to subclass this protocol.

    :param port: Port on which the device is connected. Default '/dev/ttyUSB0'.
    :type port: str
    :param buffer_size: Length of the point buffer in the protocol. Default 100.
    :type buffer_size: int

    """
    def __init__(self, port='/dev/ttyUSB0', buffer_size=100):
        self._buffer = ""
        self._frame_size = 14
        self._point_buffer_size = buffer_size
        self.point_buffer = deque(maxlen=self._point_buffer_size)
        self._serial_port = port
        self._serial_transport = None
        self._frame_processor = process_chunk

    def make_serial_connection(self):
        """
        Creates the serial connection to the port specified by the instance's
        _serial_port variable and sets the instance's _serial_transport variable
        to the twisted.internet.serialport.SerialPort instance.
        """
        self._serial_transport = SerialPort(self, self._serial_port, reactor,
                                            baudrate=2400, bytesize=8,
                                            parity='N', stopbits=1, timeout=5,
                                            xonxoff=0, rtscts=0)

    def break_serial_connection(self):
        """
        Calls loseConnection() on the instance's _serial_transport object.
        """
        self._serial_transport.loseConnection()

    def connectionMade(self):
        """
        This function is called by twisted when a connection to the serial
        transport is successfully opened.
        """
        pass

    def connectionLost(self, reason=connectionDone):
        """
        This function is called by twisted when the connection to the
        serial transport is lost.
        """
        print "Lost Connection to Device"
        print reason

    def dataReceived(self, data):
        """
        This function is called by twisted when new bytes are received by the
        serial transport.

        This data is appended to the protocol's framing buffer, _buffer, and
        when the length of the buffer is longer than the frame size, that many
        bytes are pulled out of the start of the buffer and frame_recieved is
        called with the frame.

        This function also performs the initial frame synchronization by
        dumping any bytes in the beginning of the buffer which aren't the
        first byte of the frame. In its steady state, the protocol framing
        buffer will always have the beginning of a frame as the first element.

        :param data: The data bytes received
        :type data: str

        """
        self._buffer += data
        while len(self._buffer) and self._buffer[0].encode('hex')[0] != '1':
            self._buffer = self._buffer[1:]
        while len(self._buffer) >= self._frame_size:
            self.frame_received(self._buffer[0:self._frame_size])
            self._buffer = self._buffer[self._frame_size:]

    def frame_received(self, frame):
        """
        This function is called by data_received when a full frame is received
        by the serial transport and the protocol.

        This function recasts the frame into the format used by the serialDecoder
        and then uses that module to process the frame into the final string. This
        string is then appended to the protocol's point buffer.

        This string is treated as a fully processed datapoint for the purposes
        of this module.

        :param frame: The full frame representing a single data point
        :type frame: str

        """
        frame = [byte.encode('hex') for byte in frame]
        chunk = ' '.join(frame)
        point = self._frame_processor(chunk)
        self.point_buffer.append(point)

    def latest_point(self, flush=True):
        """
        This function can be called to obtain the latest data point from the
        protocol's point buffer. The intended use of this function is to allow
        random reads from the DMM. Such a typical application will want to
        discard all the older data points (including the one returned), which
        it can do with flush=True.

        This function should only be called when there is data already in the
        protocol buffer, which can be determined using data_available().

        This is a twisted protocol function, and should not be called directly
        by synchronous / non-twisted code. Instead, its counterpart in the
        InstInterface object should be used.

        :param flush: Whether to flush all the older data points.
        :type flush: bool
        :return: Latest Data Point as processed by the serialDecoder
        :rtype: str

        """
        rval = self.point_buffer[-1]
        if flush is True:
            self.point_buffer.clear()
        return rval

    def next_point(self):
        """
        This function can be called to obtain the next data point from the
        protocol's point buffer. The intended use of this function is to allow
        continuous streaming reads from the DMM. Such a typical application will
        want to pop the element from the left of the point buffer, which is what
        this function does.

        This function should only be called when there is data already in the
        protocol buffer, which can be determined using data_available().

        This is a twisted protocol function, and should not be called directly
        by synchronous / non-twisted code. Instead, its counterpart in the
        InstInterface object should be used.

        :return: Next Data Point in the point buffer as processed by the serialDecoder
        :rtype: str

        """
        return self.point_buffer.popleft()

    def data_available(self):
        """
        This function can be called to read the number of data points waiting in
        the protocol's point buffer.

        This is a twisted protocol function, and should not be called directly
        by synchronous / non-twisted code. Instead, its counterpart in the
        InstInterface object should be used.

        :return: Number of points waiting in the protocol's point buffer
        :rtype: int

        """
        return len(self.point_buffer)


class InstFactory2200087(Factory):
    """
    This is a twisted protocol factory which produces twisted protocol objects
    which handle serial communications with 2200087 multimeters. This class
    is typically not to be instantiated by application code. This module includes
    a single instance of this class (factory), which can be used to create as
    many such objects as are necessary.

    This protocol factory exists and operates within the context of a twisted
    reactor. Applications themselves built on twisted should be able to
    simply import this protocol factory. Synchronous / non-twisted applications
    should use the InstInterface2200087 class instead.
    """
    def __init__(self):
        self.instances = []

    def buildProtocol(self, port, buffer_size=100):
        """
        This function returns a InstProtocol2200087 instance, bound to the
        port specified by the param port.

        This is a twisted protocol factory function, and should not be called
        directly by synchronous / non-twisted code. The InstInterface2200087
        class should be instantiated instead.

        :param port: Serial port identifier to which the device is connected
        :type port: str
        :param buffer_size: Length of the point buffer in the protocol. Default 100.
        :type buffer_size: int

        """
        instance = InstProtocol2200087(port, buffer_size=buffer_size)
        return instance

factory = InstFactory2200087()


class InstInterface2200087(object):
    """
    This class provides an synchronous / non-twisted interface to 2200087
    multimeters. It uses the underlying _protocol object which does most
    of the heavy lifting using twisted / crochet.

    For each DMM you want to connect to, instantiate this class once with the
    correct serial port string.

    If you would like to use a custom protocol to interface with the device,
    you can do so by passing in the custom protocol factory as the named
    parameter pfactory. See the documentation of the default protocol object
    for information on creating a custom Protocol class.

    :param port: Port on which the device is connected. Default '/dev/ttyUSB0'.
    :type port: str
    :param buffer_size: Length of the point buffer in the protocol. Default 100.
    :type buffer_size: int
    :param pfactory: Custom protocol factory to use, if not the one implemented here.
    :type pfactory: InstFactory2200087

    Your application code is expected to setup crochet before creating the
    instance. A short example :

    >>> from crochet import setup
    >>> setup()
    >>> from driver2200087.runner import InstInterface2200087
    >>> dmm = InstInterface2200087('/dev/ttyUSB0')
    >>> dmm.connect()
    >>> print dmm.latest_point()

    """
    def __init__(self, port='/dev/ttyUSB0', buffer_size=100, pfactory=factory):
        self._port = port
        self._protocol = pfactory.buildProtocol(port, buffer_size)

    @run_in_reactor
    def connect(self):
        """
        This function connects to the serial port specified during the
        instantiation of the class.

        This function should be called before anything else can be done
        with the object.
        """
        self._protocol.make_serial_connection()

    @run_in_reactor
    def disconnect(self):
        """
        This function disconnects from the serial port specified during the
        instantiation of the class.
        """
        self._protocol.break_serial_connection()

    @wait_for(timeout=1)
    def latest_point(self, flush=True):
        """
        This function can be called to obtain the latest data point from the
        protocol's point buffer. The intended use of this function is to allow
        random reads from the DMM. Such a typical application will want to
        discard all the older data points (including the one returned), which
        it can do with flush=True.

        This function should only be called when there is data already in the
        protocol buffer, which can be determined using data_available().

        :param flush: Whether to flush all the older data points.
        :type flush: bool
        :return: Latest Data Point as processed by the serialDecoder
        :rtype: str

        """
        return self._protocol.latest_point(flush)

    @wait_for(timeout=1)
    def next_point(self):
        """
        This function can be called to obtain the next data point from the
        protocol's point buffer. The intended use of this function is to allow
        continuous streaming reads from the DMM. Such a typical application will
        want to pop the element from the left of the point buffer, which is what
        this function does.

        This function should only be called when there is data already in the
        protocol buffer, which can be determined using data_available().

        :return: Next Data Point in the point buffer as processed by the serialDecoder
        :rtype: str

        """
        return self._protocol.next_point()

    @wait_for(timeout=1)
    def data_available(self):
        """
        This function can be called to read the number of data points waiting in
        the protocol's point buffer.

        :return: Number of points waiting in the protocol's point buffer
        :rtype: int

        """
        return self._protocol.data_available()


if __name__ == '__main__':
    setup()
    dmm = InstInterface2200087()
    dmm.connect()
    while True:
        if dmm.data_available() > 0:
            print dmm.next_point()
