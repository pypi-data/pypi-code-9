


class PrivateEnterpriseNumber(object):
    """Represents an IANA Private Enterprise Number (PEN) stored as a
    32-bit unsigned integer.
    """

    @classmethod
    def unpack(cls, identifier, width=32):
        """Unpack an unsigned integer into a tuple holding the Private
        Enterprise Number (PEN) and a value.
        """
        pen = identifier >> width
        value = identifier & ((1<<(width-1))-1)
        return cls(pen), value

    def __init__(self, pen):
        assert isinstance(pen, int)
        assert 0 <= pen < 2**32 - 1
        self.__pen = pen

    def pack(self, identifier, width=32):
        """Create an identifier using IANA Private Enterprise Number `pen`.
        The leftmost 32 bits of the return value contain the PEN; and the
        rightmost `width` bits contain `identifier`.
        """
        assert isinstance(identifier, int)
        assert 0 <= identifier < 2**width - 1
        return (self.__pen << width) | identifier

    def __eq__(self, other):
        return int(self) == int(other)


    def __int__(self):
        return self.__pen
