import types
import pandas as pd
import numpy as np
from nadamq.NadaMq import cPacket, PACKET_TYPES
from arduino_rpc.proxy import ProxyBase
try:
    from google.protobuf.message import Message
    _translate = (lambda arg: arg.SerializeToString()
                  if isinstance(arg, Message) else arg)
except ImportError:
    _translate = lambda arg: arg



from base_node_rpc.proxy import ProxyBase, I2cProxyMixin



class Proxy(ProxyBase):


    _CMD_BASE_NODE_SOFTWARE_VERSION = 0x00;
    _CMD_NAME = 0x01;
    _CMD_MANUFACTURER = 0x02;
    _CMD_SOFTWARE_VERSION = 0x03;
    _CMD_URL = 0x04;
    _CMD_MICROSECONDS = 0x05;
    _CMD_MILLISECONDS = 0x06;
    _CMD_DELAY_MS = 0x08;
    _CMD_RAM_FREE = 0x09;
    _CMD_PIN_MODE = 0x0a;
    _CMD_DIGITAL_READ = 0x0b;
    _CMD_DIGITAL_WRITE = 0x0c;
    _CMD_ANALOG_READ = 0x0d;
    _CMD_ANALOG_WRITE = 0x0e;
    _CMD_ARRAY_LENGTH = 0x0f;
    _CMD_ECHO_ARRAY = 0x10;
    _CMD_STR_ECHO = 0x11;
    _CMD_MAX_SERIAL_PAYLOAD_SIZE = 0x20;
    _CMD_UPDATE_EEPROM_BLOCK = 0x40;
    _CMD_READ_EEPROM_BLOCK = 0x41;
    _CMD_I2C_ADDRESS = 0x61;
    _CMD_I2C_BUFFER_SIZE = 0x62;
    _CMD_I2C_SCAN = 0x63;
    _CMD_I2C_AVAILABLE = 0x64;
    _CMD_I2C_READ_BYTE = 0x65;
    _CMD_I2C_REQUEST_FROM = 0x66;
    _CMD_I2C_READ = 0x67;
    _CMD_I2C_WRITE = 0x68;
    _CMD_I2C_ENABLE_BROADCAST = 0x69;
    _CMD_I2C_DISABLE_BROADCAST = 0x6a;
    _CMD_MAX_I2C_PAYLOAD_SIZE = 0x80;
    _CMD_I2C_REQUEST = 0x81;
    _CMD_LOAD_CONFIG = 0xa0;
    _CMD_SAVE_CONFIG = 0xa1;
    _CMD_RESET_CONFIG = 0xa2;
    _CMD_SERIALIZE_CONFIG = 0xa3;
    _CMD_UPDATE_CONFIG = 0xa4;
    _CMD_ON_CONFIG_SERIAL_NUMBER_CHANGED = 0xa5;
    _CMD_ON_CONFIG_BAUD_RATE_CHANGED = 0xa6;
    _CMD_ON_CONFIG_I2C_ADDRESS_CHANGED = 0xa7;
    _CMD_RESET_STATE = 0xc0;
    _CMD_SERIALIZE_STATE = 0xc1;
    _CMD_UPDATE_STATE = 0xc2;
    _CMD_SET_MS = 0xe0;
    _CMD_GET_BUFFER = 0xe1;
    _CMD_BEGIN = 0xe2;
    _CMD_SET_I2C_ADDRESS = 0xe3;
    _CMD_TARGET_POSITION = 0xe4;
    _CMD_SET_TARGET_POSITION = 0xe5;
    _CMD_ON_TICK = 0xe6;
    _CMD_TICK_COUNT = 0xe7;
    _CMD_RESET_TICK_COUNT = 0xe8;
    _CMD_SET_PERIOD = 0xe9;
    _CMD_ENABLE_TIMER = 0xea;
    _CMD_DISABLE_TIMER = 0xeb;
    _CMD_POSITION = 0xec;
    _CMD_MOVE = 0xed;
    _CMD_PULSE_US = 0xee;
    _CMD_DELAY_US = 0xef;
    _CMD_MOTOR_SET_SPEED = 0xf0;
    _CMD_MOTOR_START = 0xf1;
    _CMD_MOTOR_STOP = 0xf2;
    _CMD_MOTOR_SET_HOME = 0xf3;
    _CMD_ON_STATE_MOTOR_DELAY_US_CHANGED = 0xf4;
    _CMD_ON_STATE_MOTOR_CONTINUOUS_CHANGED = 0xf5;
    _CMD_ON_STATE_MOTOR_ENABLED_CHANGED = 0xf6;
    _CMD_ON_STATE_MOTOR_DIRECTION_CHANGED = 0xf7;


    def base_node_software_version(self):
        command = np.dtype('uint8').type(self._CMD_BASE_NODE_SOFTWARE_VERSION)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def name(self):
        command = np.dtype('uint8').type(self._CMD_NAME)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def manufacturer(self):
        command = np.dtype('uint8').type(self._CMD_MANUFACTURER)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def software_version(self):
        command = np.dtype('uint8').type(self._CMD_SOFTWARE_VERSION)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def url(self):
        command = np.dtype('uint8').type(self._CMD_URL)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def microseconds(self):
        command = np.dtype('uint8').type(self._CMD_MICROSECONDS)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint32')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def milliseconds(self):
        command = np.dtype('uint8').type(self._CMD_MILLISECONDS)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint32')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def delay_ms(self, ms):
        command = np.dtype('uint8').type(self._CMD_DELAY_MS)
        ARG_STRUCT_SIZE = 2
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(ms, )],
                               dtype=[('ms', 'uint16'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def ram_free(self):
        command = np.dtype('uint8').type(self._CMD_RAM_FREE)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint32')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def pin_mode(self, pin, mode):
        command = np.dtype('uint8').type(self._CMD_PIN_MODE)
        ARG_STRUCT_SIZE = 2
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(pin, mode, )],
                               dtype=[('pin', 'uint8'), ('mode', 'uint8'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def digital_read(self, pin):
        command = np.dtype('uint8').type(self._CMD_DIGITAL_READ)
        ARG_STRUCT_SIZE = 1
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(pin, )],
                               dtype=[('pin', 'uint8'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def digital_write(self, pin, value):
        command = np.dtype('uint8').type(self._CMD_DIGITAL_WRITE)
        ARG_STRUCT_SIZE = 2
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(pin, value, )],
                               dtype=[('pin', 'uint8'), ('value', 'uint8'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def analog_read(self, pin):
        command = np.dtype('uint8').type(self._CMD_ANALOG_READ)
        ARG_STRUCT_SIZE = 1
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(pin, )],
                               dtype=[('pin', 'uint8'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint16')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def analog_write(self, pin, value):
        command = np.dtype('uint8').type(self._CMD_ANALOG_WRITE)
        ARG_STRUCT_SIZE = 2
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(pin, value, )],
                               dtype=[('pin', 'uint8'), ('value', 'uint8'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def array_length(self, array):
        command = np.dtype('uint8').type(self._CMD_ARRAY_LENGTH)
        ARG_STRUCT_SIZE = 4

        array = _translate(array)
        if isinstance(array, str):
            array = map(ord, array)
        # Argument is an array, so cast to appropriate array type.
        array = np.ascontiguousarray(array, dtype='uint8')
        array_info = pd.DataFrame([array.shape[0], ],
                                  index=['array', ],
                                  columns=['length'])
        array_info['start'] = array_info.length.cumsum() - array_info.length
        array_data = ''.join([array.tostring(), ])
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(array_info.length['array'], ARG_STRUCT_SIZE + array_info.start['array'], )],
                               dtype=[('array_length', 'uint16'), ('array_data', 'uint16'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint16')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def echo_array(self, array):
        command = np.dtype('uint8').type(self._CMD_ECHO_ARRAY)
        ARG_STRUCT_SIZE = 4

        array = _translate(array)
        if isinstance(array, str):
            array = map(ord, array)
        # Argument is an array, so cast to appropriate array type.
        array = np.ascontiguousarray(array, dtype='uint32')
        array_info = pd.DataFrame([array.shape[0], ],
                                  index=['array', ],
                                  columns=['length'])
        array_info['start'] = array_info.length.cumsum() - array_info.length
        array_data = ''.join([array.tostring(), ])
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(array_info.length['array'], ARG_STRUCT_SIZE + array_info.start['array'], )],
                               dtype=[('array_length', 'uint16'), ('array_data', 'uint16'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint32')

        # Return type is an array, so return entire array.
        return result


    def str_echo(self, msg):
        command = np.dtype('uint8').type(self._CMD_STR_ECHO)
        ARG_STRUCT_SIZE = 4

        msg = _translate(msg)
        if isinstance(msg, str):
            msg = map(ord, msg)
        # Argument is an array, so cast to appropriate array type.
        msg = np.ascontiguousarray(msg, dtype='uint8')
        array_info = pd.DataFrame([msg.shape[0], ],
                                  index=['msg', ],
                                  columns=['length'])
        array_info['start'] = array_info.length.cumsum() - array_info.length
        array_data = ''.join([msg.tostring(), ])
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(array_info.length['msg'], ARG_STRUCT_SIZE + array_info.start['msg'], )],
                               dtype=[('msg_length', 'uint16'), ('msg_data', 'uint16'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def max_serial_payload_size(self):
        command = np.dtype('uint8').type(self._CMD_MAX_SERIAL_PAYLOAD_SIZE)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='int32')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def update_eeprom_block(self, address, data):
        command = np.dtype('uint8').type(self._CMD_UPDATE_EEPROM_BLOCK)
        ARG_STRUCT_SIZE = 6

        data = _translate(data)
        if isinstance(data, str):
            data = map(ord, data)
        # Argument is an array, so cast to appropriate array type.
        data = np.ascontiguousarray(data, dtype='uint8')
        array_info = pd.DataFrame([data.shape[0], ],
                                  index=['data', ],
                                  columns=['length'])
        array_info['start'] = array_info.length.cumsum() - array_info.length
        array_data = ''.join([data.tostring(), ])
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(address, array_info.length['data'], ARG_STRUCT_SIZE + array_info.start['data'], )],
                               dtype=[('address', 'uint16'), ('data_length', 'uint16'), ('data_data', 'uint16'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def read_eeprom_block(self, address, n):
        command = np.dtype('uint8').type(self._CMD_READ_EEPROM_BLOCK)
        ARG_STRUCT_SIZE = 4
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(address, n, )],
                               dtype=[('address', 'uint16'), ('n', 'uint16'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def i2c_address(self):
        command = np.dtype('uint8').type(self._CMD_I2C_ADDRESS)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def i2c_buffer_size(self):
        command = np.dtype('uint8').type(self._CMD_I2C_BUFFER_SIZE)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint16')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def i2c_scan(self):
        command = np.dtype('uint8').type(self._CMD_I2C_SCAN)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def i2c_available(self):
        command = np.dtype('uint8').type(self._CMD_I2C_AVAILABLE)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='int16')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def i2c_read_byte(self):
        command = np.dtype('uint8').type(self._CMD_I2C_READ_BYTE)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='int8')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def i2c_request_from(self, address, n_bytes_to_read):
        command = np.dtype('uint8').type(self._CMD_I2C_REQUEST_FROM)
        ARG_STRUCT_SIZE = 2
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(address, n_bytes_to_read, )],
                               dtype=[('address', 'uint8'), ('n_bytes_to_read', 'uint8'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='int8')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def i2c_read(self, address, n_bytes_to_read):
        command = np.dtype('uint8').type(self._CMD_I2C_READ)
        ARG_STRUCT_SIZE = 2
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(address, n_bytes_to_read, )],
                               dtype=[('address', 'uint8'), ('n_bytes_to_read', 'uint8'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def i2c_write(self, address, data):
        command = np.dtype('uint8').type(self._CMD_I2C_WRITE)
        ARG_STRUCT_SIZE = 5

        data = _translate(data)
        if isinstance(data, str):
            data = map(ord, data)
        # Argument is an array, so cast to appropriate array type.
        data = np.ascontiguousarray(data, dtype='uint8')
        array_info = pd.DataFrame([data.shape[0], ],
                                  index=['data', ],
                                  columns=['length'])
        array_info['start'] = array_info.length.cumsum() - array_info.length
        array_data = ''.join([data.tostring(), ])
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(address, array_info.length['data'], ARG_STRUCT_SIZE + array_info.start['data'], )],
                               dtype=[('address', 'uint8'), ('data_length', 'uint16'), ('data_data', 'uint16'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def i2c_enable_broadcast(self):
        command = np.dtype('uint8').type(self._CMD_I2C_ENABLE_BROADCAST)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def i2c_disable_broadcast(self):
        command = np.dtype('uint8').type(self._CMD_I2C_DISABLE_BROADCAST)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def max_i2c_payload_size(self):
        command = np.dtype('uint8').type(self._CMD_MAX_I2C_PAYLOAD_SIZE)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint32')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def i2c_request(self, address, data):
        command = np.dtype('uint8').type(self._CMD_I2C_REQUEST)
        ARG_STRUCT_SIZE = 5

        data = _translate(data)
        if isinstance(data, str):
            data = map(ord, data)
        # Argument is an array, so cast to appropriate array type.
        data = np.ascontiguousarray(data, dtype='uint8')
        array_info = pd.DataFrame([data.shape[0], ],
                                  index=['data', ],
                                  columns=['length'])
        array_info['start'] = array_info.length.cumsum() - array_info.length
        array_data = ''.join([data.tostring(), ])
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(address, array_info.length['data'], ARG_STRUCT_SIZE + array_info.start['data'], )],
                               dtype=[('address', 'uint8'), ('data_length', 'uint16'), ('data_data', 'uint16'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def load_config(self):
        command = np.dtype('uint8').type(self._CMD_LOAD_CONFIG)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def save_config(self):
        command = np.dtype('uint8').type(self._CMD_SAVE_CONFIG)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def reset_config(self):
        command = np.dtype('uint8').type(self._CMD_RESET_CONFIG)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def serialize_config(self):
        command = np.dtype('uint8').type(self._CMD_SERIALIZE_CONFIG)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def update_config(self, serialized):
        command = np.dtype('uint8').type(self._CMD_UPDATE_CONFIG)
        ARG_STRUCT_SIZE = 4

        serialized = _translate(serialized)
        if isinstance(serialized, str):
            serialized = map(ord, serialized)
        # Argument is an array, so cast to appropriate array type.
        serialized = np.ascontiguousarray(serialized, dtype='uint8')
        array_info = pd.DataFrame([serialized.shape[0], ],
                                  index=['serialized', ],
                                  columns=['length'])
        array_info['start'] = array_info.length.cumsum() - array_info.length
        array_data = ''.join([serialized.tostring(), ])
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(array_info.length['serialized'], ARG_STRUCT_SIZE + array_info.start['serialized'], )],
                               dtype=[('serialized_length', 'uint16'), ('serialized_data', 'uint16'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def on_config_serial_number_changed(self, new_value):
        command = np.dtype('uint8').type(self._CMD_ON_CONFIG_SERIAL_NUMBER_CHANGED)
        ARG_STRUCT_SIZE = 4
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(new_value, )],
                               dtype=[('new_value', 'uint32'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def on_config_baud_rate_changed(self, new_value):
        command = np.dtype('uint8').type(self._CMD_ON_CONFIG_BAUD_RATE_CHANGED)
        ARG_STRUCT_SIZE = 4
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(new_value, )],
                               dtype=[('new_value', 'uint32'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def on_config_i2c_address_changed(self, new_value):
        command = np.dtype('uint8').type(self._CMD_ON_CONFIG_I2C_ADDRESS_CHANGED)
        ARG_STRUCT_SIZE = 4
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(new_value, )],
                               dtype=[('new_value', 'uint32'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def reset_state(self):
        command = np.dtype('uint8').type(self._CMD_RESET_STATE)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def serialize_state(self):
        command = np.dtype('uint8').type(self._CMD_SERIALIZE_STATE)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def update_state(self, serialized):
        command = np.dtype('uint8').type(self._CMD_UPDATE_STATE)
        ARG_STRUCT_SIZE = 4

        serialized = _translate(serialized)
        if isinstance(serialized, str):
            serialized = map(ord, serialized)
        # Argument is an array, so cast to appropriate array type.
        serialized = np.ascontiguousarray(serialized, dtype='uint8')
        array_info = pd.DataFrame([serialized.shape[0], ],
                                  index=['serialized', ],
                                  columns=['length'])
        array_info['start'] = array_info.length.cumsum() - array_info.length
        array_data = ''.join([serialized.tostring(), ])
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(array_info.length['serialized'], ARG_STRUCT_SIZE + array_info.start['serialized'], )],
                               dtype=[('serialized_length', 'uint16'), ('serialized_data', 'uint16'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def set_MS(self, ms1, ms2, ms3):
        command = np.dtype('uint8').type(self._CMD_SET_MS)
        ARG_STRUCT_SIZE = 3
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(ms1, ms2, ms3, )],
                               dtype=[('ms1', 'uint8'), ('ms2', 'uint8'), ('ms3', 'uint8'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def get_buffer(self):
        command = np.dtype('uint8').type(self._CMD_GET_BUFFER)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is an array, so return entire array.
        return result


    def begin(self):
        command = np.dtype('uint8').type(self._CMD_BEGIN)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def set_i2c_address(self, value):
        command = np.dtype('uint8').type(self._CMD_SET_I2C_ADDRESS)
        ARG_STRUCT_SIZE = 1
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(value, )],
                               dtype=[('value', 'uint8'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def target_position(self):
        command = np.dtype('uint8').type(self._CMD_TARGET_POSITION)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='int32')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def set_target_position(self, absolute):
        command = np.dtype('uint8').type(self._CMD_SET_TARGET_POSITION)
        ARG_STRUCT_SIZE = 4
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(absolute, )],
                               dtype=[('absolute', 'int32'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def on_tick(self):
        command = np.dtype('uint8').type(self._CMD_ON_TICK)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def tick_count(self):
        command = np.dtype('uint8').type(self._CMD_TICK_COUNT)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint32')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def reset_tick_count(self):
        command = np.dtype('uint8').type(self._CMD_RESET_TICK_COUNT)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def set_period(self, period):
        command = np.dtype('uint8').type(self._CMD_SET_PERIOD)
        ARG_STRUCT_SIZE = 4
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(period, )],
                               dtype=[('period', 'uint32'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def enable_timer(self, period):
        command = np.dtype('uint8').type(self._CMD_ENABLE_TIMER)
        ARG_STRUCT_SIZE = 4
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(period, )],
                               dtype=[('period', 'uint32'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def disable_timer(self):
        command = np.dtype('uint8').type(self._CMD_DISABLE_TIMER)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def position(self):
        command = np.dtype('uint8').type(self._CMD_POSITION)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='int32')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def move(self, relative):
        command = np.dtype('uint8').type(self._CMD_MOVE)
        ARG_STRUCT_SIZE = 4
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(relative, )],
                               dtype=[('relative', 'int32'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def pulse_us(self):
        command = np.dtype('uint8').type(self._CMD_PULSE_US)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint32')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def delay_us(self):
        command = np.dtype('uint8').type(self._CMD_DELAY_US)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint32')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def motor_set_speed(self, steps_per_second):
        command = np.dtype('uint8').type(self._CMD_MOTOR_SET_SPEED)
        ARG_STRUCT_SIZE = 4
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(steps_per_second, )],
                               dtype=[('steps_per_second', 'int32'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def motor_start(self, steps_per_second):
        command = np.dtype('uint8').type(self._CMD_MOTOR_START)
        ARG_STRUCT_SIZE = 4
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(steps_per_second, )],
                               dtype=[('steps_per_second', 'int32'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def motor_stop(self):
        command = np.dtype('uint8').type(self._CMD_MOTOR_STOP)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def motor_set_home(self):
        command = np.dtype('uint8').type(self._CMD_MOTOR_SET_HOME)
        payload_size = 0
        payload_data = ''

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)


    def on_state_motor_delay_us_changed(self, new_value):
        command = np.dtype('uint8').type(self._CMD_ON_STATE_MOTOR_DELAY_US_CHANGED)
        ARG_STRUCT_SIZE = 4
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(new_value, )],
                               dtype=[('new_value', 'uint32'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def on_state_motor_continuous_changed(self, new_value):
        command = np.dtype('uint8').type(self._CMD_ON_STATE_MOTOR_CONTINUOUS_CHANGED)
        ARG_STRUCT_SIZE = 1
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(new_value, )],
                               dtype=[('new_value', 'uint8'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def on_state_motor_enabled_changed(self, new_value):
        command = np.dtype('uint8').type(self._CMD_ON_STATE_MOTOR_ENABLED_CHANGED)
        ARG_STRUCT_SIZE = 1
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(new_value, )],
                               dtype=[('new_value', 'uint8'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is a scalar, so return first entry in array.
        return result[0]


    def on_state_motor_direction_changed(self, new_value):
        command = np.dtype('uint8').type(self._CMD_ON_STATE_MOTOR_DIRECTION_CHANGED)
        ARG_STRUCT_SIZE = 1
        array_data = ''
        payload_size = ARG_STRUCT_SIZE + len(array_data)
        struct_data = np.array([(new_value, )],
                               dtype=[('new_value', 'uint8'), ])
        payload_data = struct_data.tostring() + array_data

        payload_data = command.tostring() + payload_data
        packet = cPacket(data=payload_data, type_=PACKET_TYPES.DATA)
        response = self._send_command(packet)

        result = np.fromstring(response.data(), dtype='uint8')

        # Return type is a scalar, so return first entry in array.
        return result[0]







class I2cProxy(I2cProxyMixin, Proxy):
    pass


