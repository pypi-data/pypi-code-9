from obdlib.obd.protocols import protocols, can_protocols


class Response(object):
    """
        This object contains response data and
        includes the common data analyzing
    """

    def __init__(self, data=b'', proto_num=0):
        # convert to string
        # split by term
        # remove spaces
        buff = data.decode().replace('\n', '').split('\r')
        self.raw_data = [line.strip().replace(' ', '')
                         for line in buff if line]
        # init protocol (CAN or rest)
        self.protocol = can_protocols.ProtocolsCan(
            proto_num) if proto_num > 5 else protocols.Protocols()

    def _check_value(func):
        """
            Checks response value
            ? - this is a standard response for a misunderstood command
        """

        def wrapper(self):

            if '?' in self.raw_data[:1]:
                return None
            else:
                return func(self)

        return wrapper

    @property
    def value(self):
        """
            Retrieves useful value from data
            :return dictionary: key - ECU, value - frame data
        """
        return self.protocol.create_data(self.raw_data)

    @property
    @_check_value
    def raw_value(self):
        """
            Retrieves all available data (raw)
        """
        return self.raw_data

    @property
    def at_value(self):
        """
            Retrieves all available data (raw)
        """
        return self.raw_data[:1][0] if self.raw_data else []
