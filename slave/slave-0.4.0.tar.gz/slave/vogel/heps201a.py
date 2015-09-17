class HEPS201A(object):
    """A Vogel-Electronik HEPS 201A heat pulse currentsource.

    E.g.::

        from slave.transport import Serial
        from slave.vogel import HEPS201A

        device = HEPS201A(Serial(0, baudrate=9600))
        device.range = 0.001 # Sets current range to 0.0001 A - 0.001 A.
        device.pulse_duration = 455 # Sets the pulse duration to 455 ms.
        device.trigger()

        # The smallest possible range is chosen before the current is set.
        device.current = 0.0001 # Sets the current to 0.1 mA.
        device.trigger()
        

    :param transport: A transport object.
    """
    RANGES = (10e-6, 100e-6, 1000e-6, 10000e-6)

    def __init__(self, transport, protocol=None):
        if not protocol:
            # The protocol in use is a subset of the Oxford Isobus protocol.
            protocol = OxfordIsobusProtocol(address=None, echo=False)
        super(HEPS201A, self).__init__(transport, protocol=protocol)

    @property
    def current(self):
        pass

    @current.setter
    def current(self, value):
        for range in self.RANGES:
            if range > value:
                self.range = range
                value = 100 * value / range # convert value to percent of range
                break
        else:
            raise ValueError('current is too large')
        self._write(('i', Integer(min=1, max=100), value / range)
