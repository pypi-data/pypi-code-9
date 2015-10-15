#!/usr/bin/env python
import re
import base64
import struct
from io import StringIO

from . import packets

"""
This modules describe all the basic functions and class
needed to parse OpenPGP data. It provides generators for
packets being read from streams.
"""

armor_types = [
          'MESSAGE'
        , 'PUBLIC KEY BLOCK'
        , 'PRIVATE KEY BLOCK'
        , 'SIGNATURE'
        , 'SIGNED MESSAGE'
        ]

valid_headers = [
          'Version'
        , 'Comment'
        , 'MessageID'
        , 'Hash'
        , 'Charset'
        ]

class ParseException(Exception):
    """
    Base exception for this module
    """
    pass

class MalformedArmorException(ParseException):
    """
    The armor is malformed
    
    Attributes:
        armor: the string in armor who raised the error
        message: explanation of the error
    """
    def __init__(self, armor, message):
        self.armor = armor
        self.message = message

class InvalidHeaderException(ParseException):
    """
    We have an invalid header in our armor

    Attributes:
        header: The invalid header
    """
    def __init__(self, header):
        self.header = header
        self.message = 'Header {} invalid for this kind of armor.'.format(self.header)

class NonClearSignException(ParseException):
    """
    We tried to do some clear sign on a non-clearsign
    """
    pass

class ChecksumException(ParseException):
    """
    This exception occurs when we have no crc or an invalid one.

    Attributes:
        crc_found: the crc found in the message - or None
        crc_calc: the calculated crc, or None if no crc_found
    """
    def __init__(self, crc_found, crc_calc):
        self.crc_found = crc_found
        self.crc_calc = crc_calc
        if self.crc_found == None:
            self.message = 'No CRC24 found in RADIX message.'
        else:
            self.message = 'CRC24 found in message ({}) differs from the calculated one({})'.format(self.crc_found, self.crc_calc)

class BinaryGenerator(object):
    tag_flag = 0x80

    def parse(self, binary):
        self.binary = bytearray(binary)
        self.offset = 0

        # We must have a 1 as the 7th bit
        if not bool(binary[0] & self.tag_flag):
            raise ParseException("7th bit of data should be one.")

        self.length = len(self.binary)
        while self.offset <= self.length:
            length, packet = packets.bintopacket(self.binary, self.offset)
            self.offset += length
            yield packet

class ArmoryGenerator(BinaryGenerator):
    """
    This class is used to parse or generate armors.
    """
    def __init__(self):
        # Some flag for all the armored packets.
        self.type = None
        self.headers = {}
        self.start = 0
        self.stop = None
        self.binary = b''
        # Those are only for multipart message
        self.multipart = False
        self.part = None
        self.part_total = None
        # And those only for clearsign
        self.clearsign = False
        self.clear_text = u''

    def dearmor(self, fd):
        self.fd = fd
        self.start = self.fd.tell()
        # First, let's get the first line ofthe radix block.
        armor_head = self.fd.readline()

        # We need to test if the head if correctly formed
        head_regexp = re.compile(r"""
                    ^-{5} # We must have 5 dash at the start of the line
                    BEGIN\ PGP\  # We want to match PGP message
                    ((MESSAGE)? # Is this a message?
                        (,\ PART\ ([0-9]+)(/([0-9]+))?)? # If this is a message, we may have a PART number
                        |([A-Z]+(\ [A-Z]+)*) # If not, then we can capture the rest
                    )
                    -{5}\ *$ # We must end with 5 dash. And we might have some spaces"""
                , re.X)
        matching = head_regexp.match(armor_head.decode())

        if not matching:
            raise MalformedArmorException(armor_head, "Armor Header line malformed")

        # Let's check if our header is in an known armor format
        if matching.group(2) == 'MESSAGE':
            armor_type = matching.group(2)
            if matching.group(3): # This is a multipart message
                self.multipart = True
                self.part = 5
                if matching.group(5): # We're in the form MESSAGE, PART X/Y. If we'renot, we keep the part_total to None
                    self.part_total = matching.group(6)
            full_armor = matching.group(1)
        else:
            armor_type = matching.group(1)
            full_armor = armor_type
        if armor_type not in armor_types:
            raise MalformedArmorException(armor_head, "Armor Header of type {} is unknown".format(armor_type))

        self.type = armor_type

        # We want to check if we have a CLEARSIGN message
        if self.type == 'SIGNED MESSAGE':
            self.clearsign = True

            # We want to parse the headers
            self.parse_headers()

            # Now we have the cleartext coming. in a dash escaped form
            try:
                line = self.fd.readline()
                matching = head_regexp.match(line.decode())
                while not matching:
                    self.clear_text += line.decode()
                    line = self.fd.readline()
                    matching = head_regexp.match(line.decode())
            except EOFError:
                raise ParseError("Got a SIGNED MESSAGE but no SIGNATURE block present.")
            # We do have a match. it should be of type SIGNATURE.
            if not matching.group(1) == 'SIGNATURE':
                raise ParseException("Got a SIGNED MESSAGE, but no SIGNATURE.")

            # Let's just get the start point.
            self.start = self.fd.tell() - len(line)

            # Now we can continue.

        # We want to parse each line until one match the end signature
        try:
            armor_tail = self.fd.readline()
            while not armor_tail.decode().startswith('-----'):
                armor_tail = self.fd.readline()
            self.stop = self.fd.tell() - len(armor_tail)
        except EOFError:
            raise MalformedArmorException(armor_head, "No armor tail found.")
        # We have a line starting with -----. If it's not a header … then raise.

        if self.clearsign:
            matching = re.match(r'^-{5}END PGP SIGNATURE-{5} *$', armor_tail.decode())
        else:
            matching = re.match(r'^-{5}END PGP %s-{5} *$' % (full_armor,), armor_tail.decode())
        if not matching:
            raise MalformedArmorException(armor_head, "Armor tail does not match armor head: {}".format(armor_tail))

        # Time to parse the headers
        self.parse_headers()

        # Now let's check the base64 and parse the binary
        self.verify()

    def parse(self):
        return super(ArmoryGenerator, self).parse(self.tobinary())

    def parse_headers(self):
        """
        This method parse the headers from an armor from the fd passed. It is usually done right
        after the 
        """
        # Let's rewing to the start of our block
        self.fd.seek(self.start)
        # And go after the armor head
        self.fd.readline()

        line = self.fd.readline()
        while line != b'\n':
            # We have a line of the form: Header: value
            split = re.split(r': ', line[:-1].decode())

            # Let's check that our headers are valid
            if split[0] not in valid_headers:
                raise InvalidHeaderException(split[0])

            if split[0] == 'MessageID' and (not self.multipart or self.part_total != None or len(split[1]) != 32):
                # We should not have a MessageID if we're not in a 
                # MESSAGE, PART X armor.
                raise InvalidHeaderException(split[0])

            if split[0] in self.headers:
                # We have multiple occurence of the same header
                self.headers[split[0]] = ' '.join(self.headers[split[0]], split[1])

            self.headers[split[0]] = split[1]
            line = self.fd.readline()

        # We must have a messageID in the case of a multipart Message without a total part.
        if self.multipart and self.part_total == None and 'MessageID' not in self.headers:
            raise ParseException('MessageID header not found while it should be present for this armor.')

        # The self.start now points at the start of the radix64 base
        self.start = self.fd.tell()

    def crc24(self, octets):
        """
        We need this function to work with armored things to check they are ok, or
        to compute the crc by itself.

        original C code is:

              #define CRC24_INIT 0xB704CEL
              #define CRC24_POLY 0x1864CFBL

              typedef long crc24;
              crc24 crc_octets(unsigned char *octets, size_t len)
              {
                  crc24 crc = CRC24_INIT;
                  int i;
                  while (len--) {
                      crc ^= (*octets++) << 16;
                      for (i = 0; i < 8; i++) {
                          crc <<= 1;
                          if (crc & 0x1000000)
                              crc ^= CRC24_POLY;
                      }
                  }
                  return crc & 0xFFFFFFL;
              }
         """
        INIT = 0xB704CE
        POLY = 0x1864CFB
        crc = INIT
        for octet in octets:
            crc ^= (octet << 16)
            for i in range(8):
                crc <<= 1
                if crc & 0x1000000: crc ^= POLY
        return crc & 0xFFFFFF

    def verify(self):
        """
        We need to verify the checksum of the RADIX64 part (the one between self.start and self.stop.
        We need to check that the base64 encoded version of the CRC24 (last line of the radix64 - minux the =
        sign) is the same that the one we're trying to calculate.
        """
        # First, let's assemble the base64 stuff
        self.fd.seek(self.start)
        self.base64_block = b''
        while self.fd.tell() < self.stop:
            line = self.fd.readline()
            if line.startswith(b'='):
                # We've reach the CRC. Let's decode it. We do not ant the starting =
                crc = line[1:]
                break
            self.base64_block += line
        try:
            crc_d = base64.b64decode(crc)
            # The CRC is a 24 bits int. Need to run some magic
            crc_found = (crc_d[0] << 16) + (crc_d[1] << 8) + crc_d[2]
        except Exception as e:
            raise ChecksumException(None, None)

        calc_crc = self.crc24(base64.b64decode(self.base64_block))
        if calc_crc != crc_found:
            raise ChecksumException(crc_found, calc_crc)
        return True

    def tobinary(self):
        """
        Let's convert our armor to a binary blob ready to be parsed.

        Just to be sure, we're going to check that the CRC is ok. Also,
        flags will be passed upon the BinaryParser instance.
        """
        self.verify()
        binary = base64.b64decode(self.base64_block)
        return binary

    def armor(self, binary, clear_text=None):
        """
        Let's generate an Armor using the parameters we already have. We do have a binary
        blob passed as an arguments.
        """
        # First, let's assemble an armor head and an armor tail
        if self.clearsign:
            armor_prologue = u'-----BEGIN PGP {}-----\n'.format(self.type)
            armor_head = u'-----BEGIN PGP SIGNATURE-----\n'
            armor_tail = u'-----END PGP SIGNATURE{}-----\n'
        else:
            armor_head = u'-----BEGIN PGP {}-----\n'.format(self.type)
            armor_tail = u'-----END PGP {}-----\n'.format(self.type)

        with StringIO('') as output:
            # Let's go for an hypotethic prologue
            if self.clearsign:
                output.write(armor_prologue)

                # We need to parse the Hash header
                output.write('Hash: {}\n'.format(self.headers['Hash']))

                # Add the clear text and a blank line
                output.write(clear_text + '\n\n')
                self.clear_text = clear_text

            # prologue is done
            output.write(armor_head)

            # Let's generate the headers
            self.headers['Version'] = u'Python OpenPGPParser'
            for header in self.headers:
                # if we have a version, skip it, we'll add our own later
                output.write('{}: {}\n'.format(header, self.headers[header]))

            # We now need a blank line
            output.write('\n')

            # let's put the bianry stuff in here.
            # Line should not be longer than 74chars.
            calc_crc = self.crc24(binary)
            # Let's convert our crc to a byte
            # Our CRC is on 24 bytes, not 32. So we're gonna have
            # A full byte of garbage, that needs to be swept out.
            crc_calc = self.crc24(binary)
            crc_byte = struct.pack('>i', crc_calc)[1:4] # We only want 3 bytes
            crc_b64 = base64.b64encode(crc_byte).decode()
            b64 = base64.b64encode(binary).decode()
            offset = 0
            while offset < len(b64):
                try:
                    output.write(b64[offset:offset+73] + '\n')
                    offset += 74
                except IndexError:
                    # We have less than 74 chars left
                    output.write(b64[offset:] + '\n')
                    break
            # Let's add the CRC
            output.write(u'={}\n'.format(crc_b64))
            output.write(armor_tail)
            output.seek(0)
            out = output.readlines()
            return out
