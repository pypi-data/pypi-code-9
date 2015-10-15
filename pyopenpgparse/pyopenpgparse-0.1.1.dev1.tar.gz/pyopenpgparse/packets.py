#!/usr/bin/env python

from pygcrypt.types.sexpression import SExpression
#from pygcrypt.types.mpi import MPIint
from pygcrypt.utils import scan

from .utils import get_int2, get_int4, get_int8

"""
This module is used to manipulate PacketBinary data and to convert them to
S-Expression, and the other way around.

It uses a lot of code and principle used in python-pgpdump: https://github.com/toofishes/python-pgpdump
"""


class PacketException(Exception):
    pass

class UnknownPacketTypeException(Exception):
    pass

class Packet(object):
    """
    This class is used to parse and generates binary packets to and from S-Expression.
    It is not intended to be directly used, but rather implemented for each of the
    Packet defined in the OpenPGP RFC.

    The function bintosexp is called when the initializer is created with a data
    arguments( which should be a bytearray). The function sexptobin is called when
    a valid S-Expression has been given to the initiliazer.
    """
    def __init__(self, tag, new, length, data=None, sexp=None):
        """
        Let's create a Packet either from data, or from a S-Expression
        """
        self.tag = tag
        self.new = new
        self.length = length
        if data == None:
            self.data = bytearray()
        else:
            self.data = data
            self.sexp = self.bintosexp()

    def bintosexp(self):
        """
        This is a placeholder. It is implemented by subclasses
        """
        raise NotImplementedError

class AlgoMixin(object):
    """
    This is a mixin containing method and tables for various algorithm check needed
    """
    pub_algorithms = {
        1:  "RSA Encrypt or Sign",
        2:  "RSA Encrypt-Only",
        3:  "RSA Sign-Only",
        16: "ElGamal Encrypt-Only",
        17: "DSA Digital Signature Algorithm",
        18: "Elliptic Curve",
        19: "ECDSA",
        20: "Formerly ElGamal Encrypt or Sign",
        21: "Diffie-Hellman",
    }

    @classmethod
    def lookup_pub_algorithm(cls, alg):
        if 100 <= alg <= 110:
            return "Private/Experimental algorithm"
        return cls.pub_algorithms.get(alg, "Unknown")

    hash_algorithms = {
        1:  "MD5",
        2:  "SHA1",
        3:  "RIPEMD160",
        8:  "SHA256",
        9:  "SHA384",
        10: "SHA512",
        11: "SHA224",
    }

    @classmethod
    def lookup_hash_algorithm(cls, alg):
        # reserved values check
        if alg in (4, 5, 6, 7):
            return "Reserved"
        if 100 <= alg <= 110:
            return "Private/Experimental algorithm"
        return cls.hash_algorithms.get(alg, "Unknown")

    sym_algorithms = {
        # (Name, IV length)
        0:  ("Plaintext or unencrypted", 0),
        1:  ("IDEA", 8),
        2:  ("Triple-DES", 8),
        3:  ("CAST5", 8),
        4:  ("Blowfish", 8),
        5:  ("Reserved", 8),
        6:  ("Reserved", 8),
        7:  ("AES with 128-bit key", 16),
        8:  ("AES with 192-bit key", 16),
        9:  ("AES with 256-bit key", 16),
        10: ("Twofish with 256-bit key", 16),
        11: ("Camellia with 128-bit key", 16),
        12: ("Camellia with 192-bit key", 16),
        13: ("Camellia with 256-bit key", 16),
    }

    @classmethod
    def _lookup_sym_algorithm(cls, alg):
        return cls.sym_algorithms.get(alg, ("Unknown", 0))

    @classmethod
    def lookup_sym_algorithm(cls, alg):
        return cls._lookup_sym_algorithm(alg)[0]

    @classmethod
    def lookup_sym_algorithm_iv(cls, alg):
        return cls._lookup_sym_algorithm(alg)[1]

class PublicKeyEncryptedSessionKeyPacket(Packet, AlgoMixin):
    def __init__(self, *args, **kwargs):
        self.session_key_version = None
        self.key_id = None
        self.pub_algo = None
        super(PublicKeyEncryptedSessionKeyPacket, self).__init__(*args, **kwargs)

    def bintosexp(self):
        """
        This blocks is structured like that:
            0 - version, must be 3 nothing else is supported
            1-9 - The key ID
            10 - public key algorithm used
            11+ - the encrypted session key. Depending on the algorithm used
                it might be one MPI (RSA) or 2 (ElGamal)
        """
        self.version = self.data[0]
        if self.version != 3:
            raise UnknownPacketTypeException("Unexpected version for {}".format(type(self)), self.version)
        self.key_id = self.data[1:9]
        algo = self.data[9]
        if algo in (1, 2, 3):
            # We're in a RSA algorithm, we need to get a MPI
            nbits = get_int2(self.data, 10)
            nbytes = (nbits + 7) // 8

            # We need to get the length of the MPI, including the two bytes for the size
            a = self.data[10:nbytes + 12]
            mpi = scan(bytes(a), 'PGP')

        # Now let's build a s-expression
        return SExpression(b"(pkesk (keyid %s) (enc-val (rsa (a %M))))", bytes(self.key_id), mpi)

def new_length(data, start):
    """
    New way of computing length. takes a bytearray as a raw input and an offset
    where the size is located. returns a (offset, length, partial) tuple.
    """
    first = data[start]
    offset = length = 0
    partial = False

    # One byte
    if first < 192:
        offset = 1
        length = first

    # Length on two bytes
    elif first < 224:
        offset = 2
        length = ((first - 192) << 8) + data[start + 1] + 192

    # Length on five byte
    elif first == 255:
        offset = 5
        length = get_int4(data, start + 1)

    # Partial body length, one byte long
    else:
        offset = 1
        # partial length is more than 224 but less than 255
        length = 1 << (first & 0x1f)
        partial = True

    return (offset, length, partial)

def old_length(data, start):
    """
    Old way of compuiting packet length. takes a bytearray as an input and an
    offset to where to look. Returns a (offset, length) tuple
    """
    offset = length = 0
    temp_len = data[start] & 0x03

    if temp_len == 0:
        offset = 1
        length = data[start + 1]
    elif temp_len == 1:
        offset = 2
        length = get_int2(data, start + 1)
    elif temp_len == 2:
        offset = 4
        length = get_int4(data, start + 1)
    elif temp_len == 3:
        length = len(data) - start - 1

    return (offset, length)

tag_types = {
        # tag: Packet Type 
          0: None
        , 1: PublicKeyEncryptedSessionKeyPacket
        , 2: None #SignaturePacket
        , 3: None #SymmetricEncryptedSessionKeyPacket
        , 4: None #OnePassSignaturePacket
        , 5: None #SecretKeyPacket
        , 6: None #PublicKeyPacket
        , 7: None #SecretSubkeyPacket
        , 8: None #CompressedDataPacket
        , 9: None #SymmetricallyEncryptedDataPacket
        , 10: None #MarkerPacket
        , 11: None #LiteralDataPacket
        , 12: None #TrustPacket
        , 13: None #UserIDPacket
        , 14: None #PublicSubkeyPacket
        , 17: None #UserAttributepacket
        , 18: None #SymmetricallyEncryptedAndMDCPacket
        , 19: None #ModificationDetectionCodepacket
        , 60: None
        , 61: None
        , 62: None
        , 63: None
        }

def bintopacket(binary, offset):
    """
    We will parse thepacket header to find thetype of header and then create
    a header from binary, starting at offset.

    We must returns the length of the packet and the packet itself in a tuple.
    """
    # The tag defining the packet type is the first byte. But a bit complicated one.
    # 7th bit is always 1
    # 6th bit is one if it's a new packet, 0 otherwise
    # 5 to 0 bits are the actual tag (mask is 0x3f)
    tag = binary[offset] & 0x3f

    # Are we new? 5th bitonly mask is 0x40
    new = bool(binary[offset] & 0x40)

    if new:
        # length is encoded in the second - and following - bytes
        # can be partial.
        data_offset, data_length, partial = new_length(binary, offset + 1)
    else:
        # tag is in bits 5-2, need to remove the 2 lower bits
        tag >>=2
        data_offset, data_length = old_length(binary, offset)
        partial = False

    PacketClass = tag_types.get(tag, None)
    if PacketClass is None:
        raise UnknownPacketTypeException(tag)

    # We managed the first byte
    data_offset += 1

    # Now let's keep track of consumed data
    consumed = 0
    packet_data = bytearray()

    while True:
        consumed += data_offset
        start = offset + data_offset
        offset = start + data_length
        packet_data = binary[start:offset]
        consumed += data_length

        if partial:
            # We are in a partial state, as long as this is true
            # Wer're alternating headers and packet data/
            data_offset, data_length, partial = new_length(binary, offset)
        else:
            # We're at the end of the packet
            break
    PacketType = tag_types.get(tag, None)
    packet = PacketType(tag, new, data_length, data=packet_data)
    return (consumed, packet)
