#!/usr/bin/env python
#
# Module to get rsbac value from give integer number for human readable.
#
# Depencies:
#           python-argparse
#

"""
(c) 2011 Jens Kasten <jens@kasten-edv.de>
"""

import argparse


class Converter(object):
    """Converter to obtain names from rsbac values."""    
    
    def int_to_bin(self, value, bitmask_len):
        """interger to binary"""
        value = int(value)
        dual_count = 1
        values_to_find = []
        for i in range(bitmask_len):
            bit_count = value >> i & 1  
            if i >= 1:
                dual_count += dual_count
            if bit_count == 1:
                values_to_find.append(dual_count)
            if dual_count >= value:
                return values_to_find

    def show_bits_from_int(self, value, as_dual=False):
        """binary to integer"""
        value = int(value)
        result = []
        bit_count = ""
        while value > 0:
            bit_count = str(value % 2) + bit_count
            value = value >> 1  
        bit_count = "".join(reversed(bit_count))            
        if as_dual:
            for i in range(len(bit_count)):
                if int(bit_count[i]) == 1:
                    result.append(1)
                else:
                    result.append(0)
            result = "".join([str(i) for i in result])
            return result[::-1]
        else:
            for i in range(len(bit_count)):
                if int(bit_count[i]) == 1:
                    result.append(i)
            return result 
        
    def bin_to_int(self, value):
        """binary to integer"""
        value = int(value)
        result = []
        bit_count = ""
        while value > 0:
            bit_count = str(value % 2) + bit_count
            value = value >> 1  
        bit_count = "".join(reversed(bit_count))            
        for i in range(len(bit_count)):
            if int(bit_count[i]) == 1:
                result.append(i)
        return result 


def main():
    parser = argparse.ArgumentParser(description="Converter")
    parser.add_argument("-i", "--int-to-bin", type=int,
        metavar="interger count",
        help="Convert an interger to binary representation")
    parser.add_argument("-I", "--show-bits-from-int", type=int,
        metavar="integer count",
        help="Show the bit representation of an interger. The shown"
            " value are the place where bits are set.")
    parser.add_argument("-b", "--bin-to-int", type=str,
        metavar="dual string",
        help="Convert a binary to interger representation")
    parser.add_argument("-B", "--bitmask-length", default=32,
        action="store_true",
        help="The length of bitmask to using. Default length is 32.")
    parser.add_argument("-S", default=False, action="store_true",
        help="Show result as string")
    
    options = parser.parse_args()
    print(options)
    
    if not options.int_to_bin and not options.show_bits_from_int:
        parser.print_usage()
    c = Converter()

    if options.int_to_bin:
        print(c.int_to_bin(options.int_to_bin, options.bitmask_length))
    if options.show_bits_from_int:
        print(c.show_bits_from_int(options.show_bits_from_int, options.S))
    if options.bin_to_int:
        print(c.bin_to_int(options.bin_to_int))

if __name__ == "__main__":
    main()
