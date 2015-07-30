#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) 2015 Chintalagiri Shashank
# Copyright (C) 2014, 2015 David Dworken
#
# This file is based on David Dworken's implementation at
# https://github.com/ddworken/2200087-Serial-Protocol
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

"""Serial Decoder for RadioShack 2200087 Multimeter

This module provides functions for decoding the serial protocol of the
RadioShack 2200087 Mulitimeter. See the included `basic.rst` for the
protocol specifications and standalone usage instructions for the script.

The documentation in this file focuses on the usage of this file as a
module.
"""

import numpy as np
import subprocess
import serial
import argparse
import sys


class Grapher(object):
    """
    Grapher used to plot a graph of the data when used in standalone mode. When used as a
    module, you can probably just ignore it and use your own graphing mechanism, if any.
    """
    np = __import__('numpy')
    subprocess = __import__('subprocess')
    graphOutput = []                # a list of strings to store the graph in
    x = []						    # a list to store 100 most recent X values in
    y = []    						# a list to sore 100 most recent Y values in
    graphSize = 100					# an integer defining the maximum number of data points to track
    # set graphSize to the number of seconds of data you want displayed * 10
    # (b/c serial sends values at 10 hz)

    def __init__(self, y):
        for i in range(self.graphSize):
            self.x.append(i)
        self.y = y
        self.update(self.x, self.y)
        self.graphOutput = self.get_graph()
        self.gnuplot = None

    def update(self, x, y, label='DMM'):  # reimplementation of update method to allow setting label
        self.x = x
        self.y = y
        self.gnuplot = subprocess.Popen(["/usr/bin/gnuplot"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.gnuplot.stdin.write("set term dumb 150 25\n")
        self.gnuplot.stdin.write("plot '-' using 1:2 title '" + label + "' with linespoints \n")
        for i, j in zip(x, y):
            self.gnuplot.stdin.write("%f %f\n" % (i, j))
        self.gnuplot.stdin.write("e\n")
        self.gnuplot.stdin.flush()
        i = 0
        output = []
        while self.gnuplot.poll() is None:
            output.append(self.gnuplot.stdout.readline())
            i += 1
            if i == 24:
                break
        self.graphOutput = output

    def get_graph(self):			         # return a list of lines that when printed out show a graph
        return self.graphOutput

    def get_values(self):				 # return a list of x,y value pairs (that are currently on the graph)
        return zip(self.x, self.y)

    def append(self, y_val):				 # append a yValue to the graph
        # if we already graphSize variables, then delete the oldest value and add the newest
        if len(self.x) == len(self.y):
            self.y = np.delete(self.y, 0)
            self.y = np.append(self.y, y_val)
        else:
            if len(self.x) > len(self.y):
                self.y = np.append(self.y, y_val)
        self.update(self.x, self.y)

    def append_with_label(self, y_val, label):
        if len(self.x) == len(self.y):
            self.y = np.delete(self.y, 0)
            self.y = np.append(self.y, y_val)
        else:
            if len(self.x) > len(self.y):
                self.y = np.append(self.y, y_val)
        self.update(self.x, self.y, label)


def get_arr_from_str(serial_data):
    """
    Converts serial data to an array of strings each of which is a
    binary representation of a single byte

    :param serial_data: Series of bytes received over the serial line, separated by spaces
    :type serial_data: str
    :returns: list of ascii representations for each character in the serial data
    :rtype: list

    """
    output = []
    input_list = serial_data.split(" ")
    for value in input_list:
        # The [2:] removes the first 2 characters so as to trim off the 0b
        bin_str = bin(int(value, base=16))[2:]
        # we add enough 0s to the front in order to make it 8 bytes (since bin() trims off zeros in the start)
        for i in range(8-len(bin_str)):
            bin_str = '0' + bin_str
        output.append(bin_str)
    return output


def process_digit(digit_number, bin_array):
    """
    Extracts a single digit from the binary array, at the location specified by
    `digit_number`, and returns it's numeric value as well as whether a decimal
    point is to be included.

    :param digit_number: Location from which digit should be extracted (4, 3, 2, 1)
    :type digit_number: int
    :param bin_array: Array of binary representations of serial data
    :type bin_array: list
    :rtype: tuple
    :returns decimal_point_bool: Boolean if decimal point is to be included at the specified location
    :returns digit_value: Number value of the digit at the specified location

    """
    binn = []
    if digit_number == 4:
        binn.append(bin_array[2][::-1])  # reverse it because we want to start with bit 0, not bit 7
        binn.append(bin_array[3][::-1])  # reverse it because we want to start with bit 0, not bit 7
    if digit_number == 3:
        binn.append(bin_array[4][::-1])  # reverse it because we want to start with bit 0, not bit 7
        binn.append(bin_array[5][::-1])  # reverse it because we want to start with bit 0, not bit 7
    if digit_number == 2:
        binn.append(bin_array[6][::-1])  # reverse it because we want to start with bit 0, not bit 7
        binn.append(bin_array[7][::-1])  # reverse it because we want to start with bit 0, not bit 7
    if digit_number == 1:
        binn.append(bin_array[8][::-1])  # reverse it because we want to start with bit 0, not bit 7
        binn.append(bin_array[9][::-1])  # reverse it because we want to start with bit 0, not bit 7

    # Creates a dictionary where the keys follow the protocol description in readme.md
    digit_dict = {'A': int(binn[0][0]), 'F': int(binn[0][1]), 'E': int(binn[0][2]), 'B': int(binn[1][0]),
                  'G': int(binn[1][1]), 'C': int(binn[1][2]), 'D': int(binn[1][3])}

    # passes the digit dict to getCharFromDigitDict to decode what the value is
    digit_value = get_char_from_digit_dict(digit_dict)
    # checks if there should be a decimal point
    decimal_point_bool = bool(int(binn[0][3]))

    # if it is digit 4, a decimal point actually means MAX not decimal point
    # (see readme.md for full description of protocol)
    if digit_number == 4:
        decimal_point_bool = False

    # Returns a tuple containing both whether or not to include a decimal point and the digit on the display
    return decimal_point_bool, digit_value


def get_char_from_digit_dict(digit_dict):
    """
    Converts a digit_dict into the character it represents.

    :param digit_dict: dictionary containing the digit's information
    :type digit_dict: dict
    :returns: The character represented by digit_dict
    :rtype: int or char

    """
    if is_9(digit_dict):
        return 9
    if is_8(digit_dict):
        return 8
    if is_7(digit_dict):
        return 7
    if is_6(digit_dict):
        return 6
    if is_5(digit_dict):
        return 5
    if is_4(digit_dict):
        return 4
    if is_3(digit_dict):
        return 3
    if is_2(digit_dict):
        return 2
    if is_1(digit_dict):
        return 1
    if is_0(digit_dict):
        return 0
    if is_c(digit_dict):
        return 'C'
    if is_f(digit_dict):
        return 'F'
    if is_e(digit_dict):
        return 'E'
    if is_p(digit_dict):
        return 'P'
    if is_n(digit_dict):
        return 'N'
    if is_l(digit_dict):
        return 'L'


# All of these is_*(digitDict) methods are essentially implementing a
# bitmask to convert a series of bits into characters or numbers
# While this is a horrible format, it works and is unlikely to be
# changed as switching to a more traditional bitmask is not that advantageous


def is_e(digit_dict):
    if digit_dict['A'] == 1 and digit_dict['F'] == 1 and digit_dict['G'] == 1 and digit_dict['B'] == 0 \
            and digit_dict['C'] == 0 and digit_dict['D'] == 1 and digit_dict['E'] == 1:
        return True
    return False


def is_n(digit_dict):
    if digit_dict['A'] == 0 and digit_dict['F'] == 0 and digit_dict['G'] == 1 and digit_dict['B'] == 0 \
            and digit_dict['C'] == 1 and digit_dict['D'] == 0 and digit_dict['E'] == 1:
        return True
    return False


def is_l(digit_dict):
    if digit_dict['A'] == 0 and digit_dict['F'] == 1 and digit_dict['G'] == 0 and digit_dict['B'] == 0 \
            and digit_dict['C'] == 0 and digit_dict['D'] == 1 and digit_dict['E'] == 1:
        return True
    return False


def is_p(digit_dict):
    if digit_dict['A'] == 1 and digit_dict['F'] == 1 and digit_dict['G'] == 1 and digit_dict['B'] == 1 \
            and digit_dict['C'] == 0 and digit_dict['D'] == 0 and digit_dict['E'] == 1:
        return True
    return False


def is_f(digit_dict):
    if digit_dict['A'] == 1 and digit_dict['F'] == 1 and digit_dict['G'] == 1 and digit_dict['B'] == 0 \
            and digit_dict['C'] == 0 and digit_dict['D'] == 0 and digit_dict['E'] == 1:
        return True
    return False


def is_c(digit_dict):
    if digit_dict['A'] == 1 and digit_dict['F'] == 1 and digit_dict['G'] == 0 and digit_dict['B'] == 0 \
            and digit_dict['C'] == 0 and digit_dict['D'] == 1 and digit_dict['E'] == 1:
        return True
    return False


def is_9(digit_dict):
    if digit_dict['A'] == 1 and digit_dict['F'] == 1 and digit_dict['G'] == 1 and digit_dict['B'] == 1 \
            and digit_dict['C'] == 1 and digit_dict['D'] == 1 and digit_dict['E'] == 0:
        return True
    return False


def is_8(digit_dict):
    if digit_dict['A'] == 1 and digit_dict['F'] == 1 and digit_dict['G'] == 1 and digit_dict['B'] == 1 \
            and digit_dict['C'] == 1 and digit_dict['D'] == 1 and digit_dict['E'] == 1:
        return True
    return False


def is_7(digit_dict):
    if digit_dict['A'] == 1 and digit_dict['F'] == 0 and digit_dict['G'] == 0 and digit_dict['B'] == 1 \
            and digit_dict['C'] == 1 and digit_dict['D'] == 0 and digit_dict['E'] == 0:
        return True
    return False


def is_6(digit_dict):
    if digit_dict['A'] == 1 and digit_dict['F'] == 1 and digit_dict['G'] == 1 and digit_dict['B'] == 0 \
            and digit_dict['C'] == 1 and digit_dict['D'] == 1 and digit_dict['E'] == 1:
        return True
    return False


def is_5(digit_dict):
    if digit_dict['A'] == 1 and digit_dict['F'] == 1 and digit_dict['G'] == 1 and digit_dict['B'] == 0 \
            and digit_dict['C'] == 1 and digit_dict['D'] == 1 and digit_dict['E'] == 0:
        return True
    return False


def is_4(digit_dict):
    if digit_dict['A'] == 0 and digit_dict['F'] == 1 and digit_dict['G'] == 1 and digit_dict['B'] == 1 \
            and digit_dict['C'] == 1 and digit_dict['D'] == 0 and digit_dict['E'] == 0:
        return True
    return False


def is_3(digit_dict):
    if digit_dict['A'] == 1 and digit_dict['F'] == 0 and digit_dict['G'] == 1 and digit_dict['B'] == 1 \
            and digit_dict['C'] == 1 and digit_dict['D'] == 1 and digit_dict['E'] == 0:
        return True
    return False


def is_2(digit_dict):
    if digit_dict['A'] == 1 and digit_dict['F'] == 0 and digit_dict['G'] == 1 and digit_dict['B'] == 1 \
            and digit_dict['C'] == 0 and digit_dict['D'] == 1 and digit_dict['E'] == 1:
        return True
    return False


def is_1(digit_dict):
    if digit_dict['A'] == 0 and digit_dict['F'] == 0 and digit_dict['G'] == 0 and digit_dict['B'] == 1 \
            and digit_dict['C'] == 1 and digit_dict['D'] == 0 and digit_dict['E'] == 0:
        return True
    return False


def is_0(digit_dict):
    if digit_dict['A'] == 1 and digit_dict['F'] == 1 and digit_dict['G'] == 0 and digit_dict['B'] == 1 \
            and digit_dict['C'] == 1 and digit_dict['D'] == 1 and digit_dict['E'] == 1:
        return True
    return False


def str_to_flags(str_of_bytes):
    """
    Checks all possible flags that might be needed and returns a list containing all currently active flags

    :param str_of_bytes: a string of bytes
    :type str_of_bytes: str
    :returns: list of flags, each of which is a string
    :rtype: list

    """
    flags = []
    bin_array = get_arr_from_str(str_of_bytes)
    for index, binStr in enumerate(bin_array):
        bin_array[index] = binStr[::-1]
    if bin_array[0][2] == '1':
        flags.append('AC')
    #  Don't display this because it will always be on since whenever we are getting input, it will be on.
    # if bin_array[0][1] == '1':
    #   flags.append('SEND')
    if bin_array[0][0] == '1':
        flags.append('AUTO')
    if bin_array[1][3] == '1':
        flags.append('CONTINUITY')
    if bin_array[1][2] == '1':
        flags.append('DIODE')
    if bin_array[1][1] == '1':
        flags.append('LOW BATTERY')
    if bin_array[1][0] == '1':
        flags.append('HOLD')
    if bin_array[10][0] == '1':
        flags.append('MIN')
    if bin_array[10][1] == '1':
        flags.append('REL DELTA')
    if bin_array[10][2] == '1':
        flags.append('HFE')
    if bin_array[10][3] == '1':
        flags.append('Percent')
    if bin_array[11][0] == '1':
        flags.append('SECONDS')
    if bin_array[11][1] == '1':
        flags.append('dBm')
    if bin_array[11][2] == '1':
        flags.append('n (1e-9)')
    if bin_array[11][3] == '1':
        flags.append('u (1e-6)')
    if bin_array[12][0] == '1':
        flags.append('m (1e-3)')
    if bin_array[12][1] == '1':
        flags.append('VOLTS')
    if bin_array[12][2] == '1':
        flags.append('AMPS')
    if bin_array[12][3] == '1':
        flags.append('FARADS')
    if bin_array[13][0] == '1':
        flags.append('M (1e6)')
    if bin_array[13][1] == '1':
        flags.append('K (1e3)')
    if bin_array[13][2] == '1':
        flags.append('OHMS')
    if bin_array[13][3] == '1':
        flags.append('Hz')
    return flags


def str_to_digits(str_of_bytes):
    """
    Converts a string of space separated hexadecimal bytes into numbers following the protocol in readme.md

    :param str_of_bytes: a string of bytes
    :type str_of_bytes: str
    :rtype: str
    :return: string of digits represented by str_of_bytes with decimal point as applicable

    """
    bin_array = get_arr_from_str(str_of_bytes)  # Create an array of the binary values from those hexadecimal bytes
    digits = ""
    # reversed range so that we iterate through values 4,3,2,1 in that order
    # due to how serial protocol works (see readme.md)
    for number in reversed(range(1, 5)):
        out = process_digit(number, bin_array)
        if out[1] == -1:
            print("Protocol Error: Please start an issue here: https://github.com/ddworken/2200087-Serial-Protocol/issues and include the following data: '" + str_of_bytes + "'")
            exit(1)
        if out[0] is True:  # append the decimal point if the decimalPointBool in the tuple is true
            digits += "."
        digits += str(out[1])
    # following the serial protocol, calculate whether or not a negative sign is needed
    minus_bool = bool(int(bin_array[0][::-1][3]))
    if minus_bool:
        digits = '-' + digits
    return digits


def get_serial_chunk(ser):
    """
    Gets a serial chunk from the device.

    :param ser: serial.Serial object
    :rtype: str
    :returns: string of 14 received characters separated by spaces

    """
    while True:
        chunk = []
        for i in range(14):
            chunk.append(ser.read(1).encode('hex'))
        if chunk[0][0] != '1':
            for index, byte in enumerate(chunk):
                if byte[0] == '1':
                    start_chunk = chunk[index:]
                    end_chunk = chunk[:index]
                    chunk = start_chunk + end_chunk
        return " ".join(chunk)


def process_chunk(chunk):
    digits = str_to_digits(chunk)
    flags = ' '.join(str_to_flags(chunk))
    if "None" not in digits:
        return digits + ' ' + flags
    else:
        return None


def get_next_point(ser):
    """
    Get the next point from the device. This function raises an Exception if anything at all
    goes wrong during the process of obtaining the value. The returned value is a string which
    should then be parsed by downstream code to determine what it actually is.

    Due to the nature of the serial interface, the downstream code must also ensure that this
    function is called often enough to keep the data in the various serial buffers from going
    stale. This particular DMM sends back a point every 0.1s, so this function should effectively
    be called at that frequency.

    Alternatively, a crochet / twisted based protocol implementation can be used to provide an
    interface friendlier to more complex synchronous code without needing to create a plethora
    of threads that spend their time in time.sleep().

    .. warning:: This function will block.

    """
    chunk = get_serial_chunk(ser)
    return process_chunk(chunk)


def confirm_device(ser):
    """
    Test the serial object for the device. This is a naive test, assuming that if a value can
    be successfully parsed, the device is what is expected. This is a very weak test, and should
    not be overly relied upon.
    """
    # noinspection PyBroadException
    try:
        get_next_point(ser)
        return True
    except:
        return True


def get_serial_object(port='/dev/ttyUSB0'):
    """
    Get a serial object given the port. The object is also confirmed to be for the correct
    device by the implementation in confirm_device.
    """
    ser = serial.Serial(port=port, baudrate=2400, bytesize=8, parity='N', stopbits=1, timeout=5,
                        xonxoff=False, rtscts=False, dsrdtr=False)
    if confirm_device(ser):
        return ser
    else:
        raise Exception


def main_loop(vargs):
    """
    Main loop for standalone use
    """
    if len(vargs.port) == 1:
        ser = serial.Serial(port=vargs.port[0], baudrate=2400, bytesize=8, parity='N', stopbits=1, timeout=5,
                            xonxoff=False, rtscts=False, dsrdtr=False)
        grapher = Grapher([0])
        if vargs.csv:
            print vargs.port[0] + ','
        if not vargs.csv:
            print "| " + vargs.port[0] + " |"
        while True:
            chunk = get_serial_chunk(ser)
            if vargs.graph:
                try:
                    float_val = float(str_to_digits(chunk))
                    grapher.append_with_label(float_val, ' '.join(str_to_flags(chunk)))
                    graph = grapher.get_graph()
                    for line in graph:
                        print line
                except:
                    print str_to_digits(chunk)[-1]
                    try:
                        if str_to_digits(chunk)[-1] == 'C' or str_to_digits(chunk)[-1] == 'F':
                            float_val = float(str_to_digits(chunk)[0:-1])
                            grapher.append_with_label(float_val, ' '.join(str_to_flags(chunk)))
                            graph = grapher.get_graph()
                            for line in graph:
                                print line
                    except:
                        pass
            else:
                digits = str_to_digits(chunk)
                flags = ' '.join(str_to_flags(chunk))
                if "None" not in digits:
                    if vargs.csv:
                        if not vargs.quiet:
                            print digits + ' ' + flags + ","
                        if vargs.quiet:
                            print digits + ","
                    if not vargs.csv:
                        if not vargs.quiet:
                            print "| " + digits + ' ' + flags + " |"
                        if vargs.quiet:
                            print "| " + digits + " |"
    if len(vargs.port) > 1:
        serial_ports = []
        if vargs.graph:
            print "This program does not support graphing two multimeters at the same time. "
        else:
            for portNum in range(len(vargs.port)):
                serial_ports.append(serial.Serial(port=vargs.port[portNum], baudrate=2400, bytesize=8,
                                                  parity='N', stopbits=1, timeout=5, xonxoff=False,
                                                  rtscts=False, dsrdtr=False))
            if not vargs.csv:
                sys.stdout.write("| ")
            for index, port in enumerate(vargs.port):
                # We have to use sys.stdout.write() so that it doesn't print a new line after each time we write data
                sys.stdout.write(port),
                if vargs.csv:
                    if index != len(vargs.port)-1: 	# So that it doesn't print a , after the last element
                        sys.stdout.write(","),
                if not vargs.csv:
                    sys.stdout.write(" | ")
            sys.stdout.write("\n")		# So of course that means we have to print a new line so it still is a csv
        while True:
            data = []
            for ser in serial_ports:
                chunk = get_serial_chunk(ser)
                if not vargs.quiet:
                    data.append(str_to_digits(chunk) + ' ' + ' '.join(str_to_flags(chunk)))
                if vargs.quiet:
                    data.append(str_to_digits(chunk))
            if not any("None" in s for s in data):
                if not vargs.csv:
                    sys.stdout.write("| ")
                for index, datum in enumerate(data):
                    sys.stdout.write(datum)
                    if vargs.csv:
                        if index != len(data)-1: 	# So that it doesn't print a , after the last element
                            sys.stdout.write(",")
                    if not vargs.csv:
                        sys.stdout.write(" | ")
                sys.stdout.write("\n")


if __name__ == '__main__':  # Allows for usage of above methods in a library
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph",
                        help="Use this argument if you want to display a graph. ",
                        action="store_true")
    parser.add_argument("-p", "--port", nargs='*',
                        help="The serial port to use",
                        default="/dev/ttyUSB0")
    parser.add_argument("-q", "--quiet",
                        help="Use this argument if you only want the numbers, not the description. ",
                        action="store_true")
    parser.add_argument("-c", "--csv",
                        help="Use this argument to enable csv output",
                        action="store_true")
    args = parser.parse_args()
    main_loop(args)  # Call the mainLoop method with a list containing serial data
