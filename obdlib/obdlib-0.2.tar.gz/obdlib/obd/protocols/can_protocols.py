from obdlib.obd.protocols.base import Base


class ProtocolsCan(Base):
    """
        Supports the CAN protocol (from 6 ...)
    """

    def __init__(self, number, head=True):
        """
            :param number - the number of protocol
            :param head - flag for init header
        """
        Base.__init__(self)
        self.header = head
        self.add_bits = '00000'
        # message types, see ELM spec. page 44
        self.mess_SF = 0  # the Single Frame
        self.mess_FF = 1  # the First Frame (of a multi frame message)
        self.mess_CF = 2  # the Consecutive Frame
        # The header bits depends on protocol number.
        # It uses for CAN protocol only
        self.header_bits = self.__get_bits(number)
        self.header_11 = 11
        self.header_29 = 29
        self.frame_start = 10
        self.data_start_byte = 4

    def create_data(self, raw_data):
        """
            Analyzes raw data
            :param raw_data - OBDII response
            :return dict
        """
        data = {}
        if raw_data:
            ecu_messages = self.remove_searching(raw_data)

            if self.check_message(ecu_messages):
                # if the header enabled
                if self.header:
                    data = self.process_data(ecu_messages)
        return data

    def process_data(self, ecu_messages):
        data = {}
        # multi line (ELM spec page 42) or single frame response
        self.data_start_byte = 4
        # sorts ECU's messages
        ecu_messages = sorted(ecu_messages)

        ecu_messages = self.check_frame(ecu_messages)
        for message in ecu_messages:
            ecu_number, f_type, response_mode = self.__get_frame_params(message)
            # check if response trouble codes
            if response_mode == 43:
                # add fake byte after the mode one
                # nothing to do
                self.data_start_byte = 2

            self.__process(data, message, ecu_number, f_type)
        return data

    def check_frame(self, frame):
        if self.check_header():
            # align CAN header (11 bits to 29 bits)
            # PCI byte are 8 and 9 indexes
            frame = self.__align_frame(frame)
        return frame

    def check_header(self):
        """
            Checks header. If header bits are 11, returns True
        """
        return self.header_bits == self.header_11

    def __process(self, data, message, ecu_number, f_type):
        # Single Frame
        if f_type == self.mess_SF:
            # 11 bits header:
            # 7E8 06 41 00 FF FF FF FF FC
            #
            # 29 bits header:
            # 18 DA F1 10 06 41 00 FF FF FF FF FC
            data[ecu_number] = self.__get_single_data(message)

        # multi line frame
        # the First Frame (of a multi frame message)
        #
        # 11 bits header:
        # [ecu][type][order][        data       ]
        # 7E8    1      0   13 49 04 01 35 36 30
        # 7E8 21 32 38 39 34 39 41 43
        # 7E8 22 00 00 00 00 00 00 31
        #
        # 29 bits header:
        # ........[ecu][type][order][       data       ]
        # 18 DA F1 10    1      0   32 38 39 34 39 41 43
        # 18 DA F1 10 21 32 38 39 34 39 41 43
        # 18 DA F1 10 22 00 00 00 00 00 00 31
        elif f_type == self.mess_FF:
            data[ecu_number] = message[self.frame_start:]

        # the Consecutive Frame
        elif f_type == self.mess_CF:
            data[ecu_number] += message[self.frame_start:]

    def __get_single_data(self, message):
        """
            Retrieves data from the single frame
            :param message - the OBD frame
            :return string
        """
        return message[self.frame_start:self.__last_bytes(
            self.__digit(message[9]))][self.data_start_byte:]

    def __last_bytes(self, count_byte):
        """
            Counts the last bytes
        """
        return self.frame_start + count_byte * 2

    def __get_frame_params(self, frame):
        """
            Retrieves some params from the frame
            :param frame - the OBD frame
            :return tuple of ecu_number, frame_type, response_mode
        """
        return (
            frame[6:8],
            self.__digit(frame[8]),
            int(frame[10:12])
        )

    def __align_frame(self, frame):
        """
            Align CAN header (11 bits to 29 bits)
            :param frame - the OBD frame
        """
        return [self.add_bits + mess for mess in frame]

    @staticmethod
    def __digit(value):
        """
            Hex to int
        """
        return int(value, 16)

    def __get_bits(self, n):
        """
            Retrieves header bits count
            :param n - protocol number
        """
        return self.protocols.get(n)[1] if n else None
