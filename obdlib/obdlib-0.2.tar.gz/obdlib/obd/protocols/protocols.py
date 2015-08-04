from obdlib.obd.protocols.base import Base
from obdlib.logging import logger


class Protocols(Base):
    """
        Supports next protocols - PWM, VPW, KWP (from 0 to 5)
    """

    def __init__(self, head=True):
        Base.__init__(self)
        self.header = head
        self.check_sum = -2

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
                if self.header:
                    data = self.process_data(ecu_messages)
        return data

    def process_data(self, ecu_messages):
        data = {}
        self.check_sum = -2
        # sorts ECU's messages
        ecu_messages = sorted(ecu_messages)
        service_data = self._parse_headers(ecu_messages)
        for message in ecu_messages:
            # if one ECU returns multi line
            # multi line includes line number byte
            ecu_number, response_mode = self._get_frame_params(message)

            # check if response trouble codes
            if response_mode == 43:
                # add fake byte after the mode one
                message = self._add_additional_byte(message)
                self.check_sum = None

            self._process(data, message, ecu_number, service_data[ecu_number])
        return data

    def _process(self, data, message, ecu_number, multi):
        if multi > 1:
            # multi line response - ELM spec page 42
            # response format priority:receiver:transmitter:mode:pid:line_number:data:checksum
            # >0902 - (ex: get VIN)
            # 86 F1 10 49 02 01 00 00 00 31 FC
            # 86 F1 10 49 02 02 44 34 47 50 FC
            # 86 F1 10 49 02 03 30 30 52 35 FC
            # 86 F1 10 49 02 04 35 42 31 32 FC
            # 86 F1 10 49 02 05 33 34 35 36 FC
            # 6 * 2: means that we are removed
            # "mode:pid:line" info from the record
            try:
                data[ecu_number] += self._get_multi_data(message)
            except KeyError:
                data[ecu_number] = self._get_multi_data(message)
        # frame without line number byte
        # removes header and checksum
        # format priority:receiver:transmitter:mode:pid:data:checksum
        # [ header][serv][   data   ][CS]
        # 86 F1 10 41 00 FF FF FF FF FC  - ELM spec page 38
        else:
            data[ecu_number] = self.get_data(message)

    def _get_multi_data(self, record):
        """
            Retrieves the necessary content
        """
        return record[12:self.check_sum]

    @staticmethod
    def _get_frame_params(frame):
        """
            Retrieves some params from the frame
            :param frame - the OBD frame
            :return tuple of ecu_number, response_mode
        """
        return (
            frame[4:6],
            int(frame[6:8])
        )

    @staticmethod
    def _add_additional_byte(record):
        """
            Adds fake byte after the mode one (byte is 00)
        """
        return record[:8] + '00' + record[8:]

    @staticmethod
    def _parse_headers(frames):
        """
            Collects info, how many times ECU met
            :param frames - OBDII response
            :return dict
        """
        ecu_headers = {}
        for mess in frames:
            try:
                ecu_headers[mess[4:6]] += 1
            except KeyError:
                ecu_headers[mess[4:6]] = 1

        return ecu_headers

    def get_data(self, record):
        record = record[6:self.check_sum]
        if len(record) >= 6 and len(record) <= 16:
            # remove first 4 characters. This are service bytes from ELM
            # format mode:pid:data
            # ex: 4100FFFFFFFF - ELM spec page 38
            record = record[4:]
        else:
            mess = "The frame size is not suitable."
            logger.error(mess)
            raise Exception(mess)

        return record
