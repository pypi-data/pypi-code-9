from obdlib.obd.pids import *
from binascii import unhexlify

unit_english = 0


def set_unit(v):
    """
        Sets unit flag
    """
    global unit_english
    unit_english = v


def zfill(string, width):
    """
        Wrapper for str.zfill which is not exists in micropython
        :param string: a string for alignment
        :param width: width of the resulted string
        :return: a string that has been aligned to the width
    """
    return string.zfill(width) if hasattr(
        string,
        'zfill') else (
        '{0:0%d}' %
        (width)).format(
        __digit(string))

def bitwise_pids(hex_string, start=0):
    """
        Determine supported PIDs based on the supplied hexadecimal string
        :param hex_string:a hex string representing bitwise encoded PID support
        :return: a dictionary of PID number: boolean pairs that indicate
        whether or not a PID is supported
    """
    bits = zfill(bin(int(hex_string, 16))[2:], 32)
    return dict(
        (zfill(hex(i + 1 + start)[2:], 2).upper(), 1 if value == '1' else 0)
        for i, value in enumerate(bits)
    )


def rpm(value):
    """
        Converts the vehicle's current engine RPM value
        :return: the current engine RPM
    """
    return __digit(value) / 4.0


def speed(value):
    """
        Converts the vehicle's current engine RPM value
        :return: the current engine speed
    """
    value = __digit(value)
    # English - > mph
    if unit_english:
        # km/h - > mph conversion
        value = value * 0.621371192
    return value


def load_value(value):
    """
        Converts the vehicle's current engine load value
        :return: the current engine value
    """
    return __digit(value) * 100 / 255

def term_fuel(value):
    """
        Converts the vehicle's short term fuel or long term fuel
        :return: the current engine value
    """
    return round((__digit(value) - 128) * 100 / 128.0, 2)


def fuel_pressure(value):
    """
        Converts the vehicle's fuel pressure
        :return: the current engine value
    """
    value = __digit(value) * 3
    # English - > psi
    if unit_english:
        # kPa - > psi conversion
        value = value * 0.145037738
    return round(value, 2)


def absolute_pressure(value):
    """
        Converts the vehicle's intake manifold absolute pressure
        :return: the current engine value
    """
    value = __digit(value)
    # English - > psi
    if unit_english:
        # kPa - > psi conversion
        value = value * 0.145037738
    return round(value, 2)


def timing_advance(value):
    """
        Converts the vehicle's Timing advance
        :return: the current engine value
    """
    return round((__digit(value) - 128) / 2.0, 2)


def air_flow_rate(value):
    """
        Converts the vehicle's MAF air flow rate
        :return: the current engine value
    """
    return round(__digit(value) / 100.0, 2)


def throttle_pos(value):
    """
        Converts the vehicle's Throttle position
        :return: the current engine value
    """
    return __digit(value) * 100 / 255


def air_status(value):
    """
        Converts the vehicle's Commanded secondary air status
        :return: the current engine value
    """
    return SECONDARY_AIR_STATUS.get(__digit(value), None)


def voltage(value):
    """
        Converts the vehicle's Oxygen sensor voltage
        0 - 1.275 Volts
        :return: the current engine value
    """
    return __digit(value) / 200.0


def coolant_temp(value):
    """
        Converts the vehicle's current engine coolant temperature
        :return: the current engine coolant temperature in degrees Celsius
    """
    # The data returned in the OBD response is in hexadecimal with a zero
    # offset to account for negative temperatures. To return the current
    # temperature in degrees Celsius, we must first convert to decimal and
    # then subtract 40 to account for the zero offset.
    value = __digit(value) - 40
    # English - > F
    if unit_english:
        # C - > F
        value = value * 9 / 5 + 32
    return value


def obd_standards(value):
    """
        Converts the vehicle's OBD standards this vehicle conforms to
        :return: the current engine value
    """
    return OBD_STANDARDS[__digit(value)] if len(
        OBD_STANDARDS) >= __digit(value) else None


def time(value):
    """
        Converts the vehicle's Run time since engine start
        :return: the current engine value
    """
    return __digit(value)


def oil_temp(value):
    """
        Converts the vehicle's current engine oil temperature
        :return: the current engine oil temperature in degrees Celsius
    """
    # The data returned in the OBD response is in hexadecimal with a zero
    # offset to account for negative temperatures. To return the current
    # temperature in degrees Celsius, we must first convert to decimal and
    # then subtract 40 to account for the zero offset.
    value = __digit(value) - 40
    # English - > F
    if unit_english:
        # C - > F
        value = value * 9 / 5 + 32
    return value


def vin(value):
    """
        Returns the name of the VIN
        :return: the VIN
    """
    # checks the first 3 bytes
    # if 00 - remove
    for s in range(3):
        if __digit(value[0:2]) == 0:
            value = value[2:]

    return unhexlify(value).decode()


def ecu_name(value):
    """
        Returns the name of the Engine Control Unit (ECU)
        :return: the name of the ECU (if available)
    """
    return unhexlify(value).decode()


def fuel_type(value):
    """
        Converts the vehicle's fuel type
        :return: a description of the type of fuel used by the vehicle
    """
    try:
        return FUEL_TYPE_DESCRIPTION[__digit(value)]
    except IndexError:
        return None


def fuel_system_status(value):
    """
        Converts the vehicle's Fuel system status
        :return: tuple of Fuel system status, (fuel_1, fuel_2)
    """
    # fuel system #1
    fuel_1 = __digit(value[0:2])
    # fuel system #2
    fuel_2 = __digit(value[2:])
    return (
        FUEL_SYSTEM_STATUS_DESC.get(fuel_1, FUEL_SYSTEM_STATUS_DESC[0]),
        FUEL_SYSTEM_STATUS_DESC.get(fuel_2, FUEL_SYSTEM_STATUS_DESC[0])
    )


def oxygen_sensors(value):
    """
        Checks the vehicle's Oxygen sensors
        :return: list of available sensors
    """
    # if PID 13 - [A0..A3] == Bank 1, Sensors 1-4. [A4..A7] == Bank 2...
    #
    # if PID 1D - Similar to PID 13,
    # but [A0..A7] == [B1S1, B1S2, B2S1, B2S2, B3S1, B3S2, B4S1, B4S2]
    value = bin(__digit(value))[2:]
    sensors = []
    for sensor in value:
        if sensor:
            sensors.append(int(sensor))
    return sensors


def aux_input_status(value):
    """
        Checks the vehicle's Auxiliary input status
        :return: boolean, Power Take Off (PTO) status
        True - active
    """
    return bin(__digit(value))[2:][0] == '1'


def dtc_statuses(value):
    # see https://en.wikipedia.org/wiki/OBD-II_PIDs#Mode_1_PID_01
    monitor_statuses = {
        'mil': 0,
        'dtc': 0,
        'ignition_test': 0,
        'base_tests': [
            (0, 0),  # Misfire
            (0, 0),  # Fuel-System
            (0, 0)  # Components
        ],
        'spark_tests': [
            (0, 0),  # Catalyst
            (0, 0),  # Heated-Catalyst
            (0, 0),  # Evaporative-Systems
            (0, 0),  # Secondary-Air-System
            (0, 0),  # A/C-Refrigerant
            (0, 0),  # Oxygen-Sensor
            (0, 0),  # Oxygen-Sensor-Heater
            (0, 0)  # EGR-Sytem
        ],
        'compression_tests': [
            (0, 0),  # NMHC-Cat
            (0, 0),  # N0x/Scr-Monitor
            (0, 0),  # Boost-Pressure
            (0, 0),  # Exhaust-Gas-Sensor
            (0, 0),  # PM-Filter-Monitoring
            (0, 0)  # EGR/VVT-System
        ]}
    # converts hex string to bits string
    value = bin(__digit(value))[2:]
    monitor_statuses['mil'] = int(value[0])  # A7
    monitor_statuses['dtc'] = int(value[1:8], 2)  # A6-A0
    monitor_statuses['ignition_test'] = int(value[11])  # B3

    for item in range(3):
        monitor_statuses['base_tests'][item] = (
            int(value[8 + item]),  # B0, B1, B2
            int(value[12 + item])  # B4, B5, B6
        )
    except_compr_bits = (2, 4)
    curr_compr_step = 0
    for item in range(8):
        # spark tests
        monitor_statuses['spark_tests'][item] = (
            int(value[16 + item]),  # C0-C7
            int(value[24 + item])  # D0-D7
        )
        # compression tests
        if item not in except_compr_bits:
            monitor_statuses['compression_tests'][curr_compr_step] = (
                int(value[16 + item]),  # C0, C1, C3, C5, C6, C7
                int(value[24 + item])  # D0, D1, D3, D5, D6, D7
            )
            curr_compr_step += 1

    return monitor_statuses


def trouble_codes(value):
    """
        Checks the vehicle's trouble codes
        :return list of codes
    """
    codes = []
    # trouble data frame include 6 bytes - 3 trouble codes
    # ex: 0133 0000 0000
    for item in range(0, 12, 4):
        # get trouble code
        code = value[item:item + 4]
        # check first byte
        first_char = DTCs_table.get(code[0])
        if first_char and __digit(code):
            codes.append(first_char + code[1:])

    return codes


def __digit(value):
    """
        Converts hex to digit
    """
    return int(value, 16)
