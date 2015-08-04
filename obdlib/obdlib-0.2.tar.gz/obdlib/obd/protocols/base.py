from obdlib.elm327 import NO_RESULT
from obdlib.logging import logger


class Base(object):
    def __init__(self):
        # see ELM spec. p. 25
        self.protocols = {
            0: ('Automatic',),
            1: ('SAE J1850 PWM (41.6 kbaud)',),
            2: ('SAE J1850 VPW (10.4 kbaud)',),
            3: ('ISO 9141-2  (5 baud init, 10.4 kbaud)',),
            4: ('ISO 14230-4 KWP (5 baud init, 10.4 kbaud)',),
            5: ('ISO 14230-4 KWP (fast init, 10.4 kbaud)',),
            6: ('ISO 15765-4 CAN (11 bit ID, 500 kbaud)', 11, 500),
            7: ('ISO 15765-4 CAN (29 bit ID, 500 kbaud)', 29, 500),
            8: ('ISO 15765-4 CAN (11 bit ID, 250 kbaud)', 11, 250),
            9: ('ISO 15765-4 CAN (29 bit ID, 250 kbaud)', 29, 250),
            10: ('SAE J1939 CAN (29 bit ID, 250* kbaud)', 29, 250),
            11: ('USER1 CAN (11* bit ID, 125* kbaud)',),
            12: ('USER2 CAN (11* bit ID, 50* kbaud)',),
        }

    def create_data(self, data):
        raise NotImplementedError()

    def check_message(self, ecu_messages):
        return self.check_result(ecu_messages) and self.check_error(ecu_messages)

    @classmethod
    def remove_searching(cls, data):
        """
            Removes SEARCHING... string
            This appears after OBD command 01 00 (checks available PID's)
        """
        try:
            pos = data.index('SEARCHING...')
            if pos != 1:
                data.pop(pos)
        except ValueError:
            pass

        return data

    @classmethod
    def check_result(cls, data):
        """
            Checks the data. Return False, if the data equal 'NO DATA'
        """
        return False if NO_RESULT in data else True

    @classmethod
    def check_error(cls, data):
        """
            Checks the error data. The data starts with 7F
            format: 7F mode code
        """
        response = True
        codes = {
            10: 'general reject',
            11: 'service not supported',
            12: 'invalid format',
            21: 'busy',
            22: 'conditions not correct',
            78: 'pending replies'
        }
        if data[0][0:2] == '7F':
            # logging error
            logger.error('Error: mode {} - {}'.format(data[0][2:4],  # mode
                                                      codes.get(int(data[0][-2:])))  # code
            )
            response = False

        return response
