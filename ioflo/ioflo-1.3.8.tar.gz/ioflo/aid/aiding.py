"""aiding.py constants and basic functions

"""
from __future__ import absolute_import, division, print_function

import sys
import math
import types
import socket
import os
import sys
import errno
import time
import struct
import re
import string
from collections import deque


try:
    import simplejson as json
except ImportError:
    import json

try:
    import win32file
except ImportError:
    pass

# Import ioflo libs
from .sixing import *
from ..base.globaling import *
from .odicting import odict
from ..base import excepting

from ..base.consoling import getConsole
console = getConsole()


def reverseCamel(name, lower=True):
    """ Returns camel case reverse of name.
        case change boundaries are the sections which are reversed.
        If lower is True then the initial letter in the reversed name is lower case

        Assumes name is of the correct format to be Python Identifier.
    """
    index = 0
    parts = [[]]
    letters = list(name) # list of the letters in the name
    for c in letters:
        if c.isupper(): #new part
            parts.append([])
            index += 1
        parts[index].append(c.lower())
    parts.reverse()
    parts = ["".join(part) for part in  parts]
    if lower: #camel case with initial lower
        name = "".join(parts[0:1] + [part.capitalize() for part in parts[1:]])
    else: #camel case with initial upper
        name = "".join([part.capitalize() for part in parts])
    return name

ReverseCamel = reverseCamel

def nameToPath(name):
    """ Converts camel case name into full node path where uppercase letters denote
        intermediate nodes in path. Node path ends in dot '.'

        Assumes Name is of the correct format to be Identifier.
    """
    pathParts = []
    nameParts = list(name)
    for c in nameParts:
        if c.isupper():
            pathParts.append('.')
            pathParts.append(c.lower())
        else:
            pathParts.append(c)
    pathParts.append('.')
    path = ''.join(pathParts)
    return path

NameToPath = nameToPath

def Repack(n, seq, default=None):
    """ Repacks seq into a generator of len n and returns the generator.
        The purpose is to enable unpacking into n variables.
        The first n-1 elements of seq are returned as the first n-1 elements of the
        generator and any remaining elements are returned in a tuple as the
        last element of the generator
        default (None) is substituted for missing elements when len(seq) < n

        Example:

        x = (1, 2, 3, 4)
        tuple(Repack(3, x))
        (1, 2, (3, 4))

        x = (1, 2, 3)
        tuple(Repack(3, x))
        (1, 2, (3,))

        x = (1, 2)
        tuple(Repack(3, x))
        (1, 2, ())

        x = (1, )
        tuple(Repack(3, x))
        (1, None, ())

        x = ()
        tuple(Repack(3, x))
        (None, None, ())

    """
    it = iter(seq)
    for _i in range(n - 1):
        yield next(it, default)
    yield tuple(it)

repack = Repack #alias


def just(n, seq, default=None):
    """ Returns a generator of just the first n elements of seq and substitutes
        default (None) for any missing elements. This guarantees that a generator of exactly
        n elements is returned. This is to enable unpacking into n varaibles

        Example:

        x = (1, 2, 3, 4)
        tuple(Just(3, x))
        (1, 2, 3)
        x = (1, 2, 3)
        tuple(Just(3, x))
        (1, 2, 3)
        x = (1, 2)
        tuple(Just(3, x))
        (1, 2, None)
        x = (1, )
        tuple(Just(3, x))
        (1, None, None)
        x = ()
        tuple(Just(3, x))
        (None, None, None)

    """
    it = iter(seq)
    for _i in range(n):
        yield next(it, default)

Just = just #alias

# Faster to use precompiled versions in globaling
def IsPath(s):
    """Returns True if string s is valid Store path name
       Returns False otherwise

       raw string
       this also matches an empty string so need
       r'^([a-zA-Z_][a-zA-Z_0-9]*)?([.][a-zA-Z_][a-zA-Z_0-9]*)*$'

       at least either one of these
       r'^([a-zA-Z_][a-zA-Z_0-9]*)+([.][a-zA-Z_][a-zA-Z_0-9]*)*$'
       r'^([.][a-zA-Z_][a-zA-Z_0-9]*)+$'

       so get
       r'^([a-zA-Z_][a-zA-Z_0-9]*)+([.][a-zA-Z_][a-zA-Z_0-9]*)*$|^([.][a-zA-Z_][a-zA-Z_0-9]*)+$'

       shorthand replace [a-zA-Z_0-9] with  \w which is shorthand for [a-zA-Z_0-9]
       r'^([a-zA-Z_]\w*)+([.][a-zA-Z_]\w*)*$|^([.][a-zA-Z_]\w*)+$'

       ^ anchor to start
       $ anchor to end
       | must either match preceding or succeeding expression
       * repeat previous match zero or more times greedily
       ? repeat previous match zero or one times
       ( ) group
       [ ] char from set of ranges
       [a-zA-Z_] alpha or underscore one and only one
       [a-zA-Z_0-9]* alpha numeric or underscore (zero or more)
       ([a-zA-Z_][a-zA-Z_0-9]*) group made up of one alpha_ and zero or more alphanumeric_
       ([a-zA-Z_][a-zA-Z_0-9]*)? zero or one of the previous group

       ([.][a-zA-Z_][a-zA-Z_0-9]*) group made of one period one alpha_ and zero or more alphanumeric_
       ([.][a-zA-Z_][a-zA-Z_0-9]*)* zero or more of the previous group

       so what it matches.
       if first character is alpha_ then all remaining alphanumeric_ characters will
       match up to but not including first period if any

       from then on it will match groups that start with period one alpha_ and zero
       or more alphanumeric_ until the end

       valid forms
       a
       a1
       .a
       .a1

       a.b
       a1.b2
       .a1.b2
       .a.b

       but not
       .
       a.
       a..b
       ..a
       1.2

    """
    if re.match(r'^([a-zA-Z_]\w*)+([.][a-zA-Z_]\w*)*$|^([.][a-zA-Z_]\w*)+$',s):
        return True
    else:
        return False

def IsIdentifier(s):
    """Returns True if string s is valid python identifier (variable, attribute etc)
       Returns False otherwise

       how to determine if string is valid python identifier

       r'^[a-zA-Z_]\w*$'
       r'^[a-zA-Z_][a-zA-Z_0-9]*$'  #equivalent \w is shorthand for [a-zA-Z_0-9]

       r' = raw string
       ^ = anchor to start
       [a-zA-Z_] = first char is letter or underscore
       [a-zA-Z_0-9] = next char is letter, underscore, or digit
       * = repeat previous character match greedily
       $ = anchor to end

       How
       import re
       reo = re.compile(r'^[a-zA-Z_]\w*$') #compile is faster
       if reo.match('_hello') is not None: #matched returns match object or None

       #re.match caches compiled pattern string compile so faster after first
       if re.match(r'^[a-zA-Z_]\w*$', '_hello')

       reo = re.compile(r'^[a-zA-Z_][a-zA-Z_0-9]*$')
       reo.match(

    """
    if re.match(r'^[a-zA-Z_]\w*$',s):
        return True
    else:
        return False

def IsIdentPub(s):
    """Returns True if string s is valid python public identifier,
       that is, an identifier that does not start with an underscore
       Returns False otherwise
    """
    if re.match(r'^[a-zA-Z]\w*$',s):
        return True
    else:
        return False

def PackByte(fmt = b'8', fields = [0x0000]):
    """Packs fields sequence into one byte using fmt string.

       Each fields element is a bit field and each
       char in fmt is the corresponding bit field length.
       Assumes unsigned fields values.
       Assumes network big endian so first fields element is high order bits.
       Format string is number of bits per bit field
       Fields with length of 1 are treated as has having boolean field values
          that is,   nonzero is True and packs as a 1
       for 2-8 length bit fields the field element is truncated
       to the number of low order bits in the bit field
       if sum of number of bits in fmt less than 8 last bits are padded
       if sum of number of bits in fmt greater than 8 returns exception
       to pad just use 0 value in source.
       example
       PackByte("1322",(True,4,0,3)). returns 0xc3
    """
    fmt = bytes(fmt)
    byte = 0x00
    bfp = 8 #bit field position
    bu = 0 #bits used

    for i in range(len(fmt)):
        bits = 0x00
        bfl = int(fmt[i:i+1])

        if not (0 < bfl <= 8):
            raise ValueError("Bit field length in fmt must be > 0 and <= 8")

        bu += bfl
        if bu > 8:
            raise ValueError("Sum of bit field lengths in fmt must be <= 8")

        if bfl == 1:
            if fields[i]:
                bits = 0x01
            else:
                bits = 0x00
        else:
            bits = fields[i] & (2**bfl - 1) #bit and to mask out high order bits

        bits <<= (bfp - bfl) #shift left to bit position less bit field size

        byte |= bits #or in bits
        bfp -= bfl #adjust bit field position for next element

    console.profuse("Packed byte = {0:#x}\n".format(byte))

    return byte

packByte = PackByte # alias

def UnpackByte(fmt = b'11111111', byte = 0x00, boolean = True):
    """unpacks source byte into tuple of bit fields given by fmt string.

       Each char of fmt is a bit field length.
       returns unsigned fields values.
       Assumes network big endian so first fmt is high order bits.
       Format string is number of bits per bit field
       If boolean parameter is True then return boolean values for
          bit fields of length 1

       if sum of number of bits in fmt less than 8 then remaining
       bits returned as additional element in result.

       if sum of number of bits in fmt greater than 8 returns exception
       only low order byte of byte is used.

       example
       UnpackByte("1322",0xc3, False ) returns (1,4,0,3)
       UnpackByte("1322",0xc3, True ) returns (True,4,0,3)
    """
    fmt = bytes(fmt)
    fields = [] #list of bit fields
    bfp = 8 #bit field position
    bu = 0 #bits used
    byte &= 0xff #get low order byte

    for i in range(len(fmt)):
        bfl = int(fmt[i:i+1])

        if not (0 < bfl <= 8):
            raise ValueError("Bit field length in fmt must be > 0 and <= 8")

        bu += bfl
        if bu > 8:
            raise ValueError("Sum of bit field lengths in fmt must be <= 8")

        mask = (2**bfl - 1) << (bfp - bfl) #make mask
        bits = byte & mask #mask off other bits
        bits >>= (bfp - bfl) #right shift to low order bits
        if bfl == 1 and boolean: #convert to boolean
            if bits:
                bits = True
            else:
                bits = False

        fields.append(bits) #assign to fields list

        bfp -= bfl #adjust bit field position for next element

    return tuple(fields) #convert to tuple

unpackByte = UnpackByte # alias

def Hexize(s = b''):
    """Converts bytes s into hex format
       Where each char (byte) in bytes s is expanded into the 2 charater hex
       equivalent of the decimal value of each byte
       returns the expanded hex version of the bytes as string
    """
    h = ''
    for i in range(len(s)):
        h += ("%02x" % ord(s[i:i+1]))
    return h

hexize = Hexize # alias

def Binize(h = ''):
    """Converts string h from hex format into the binary equivalent bytes by
       compressing every two hex characters into 1 byte that is the binary equivalent
       If h does not have an even number of characters then a 0 is first prepended
       to h
       returns the packed binary  version of the string as bytes
    """
    #remove any non hex characters, any char that is not in '0123456789ABCDEF'
    hh = h #make copy so iteration not change
    for c in hh:
        if c not in string.hexdigits:
            h = h.replace(c,'') #delete characters

    if len(h) % 2: #odd number of characters
        h = '0' + h #prepend a zero to make even number

    p = ''
    for i in xrange(0,len(h),2):
        s = h[i:i+2]
        p = p + struct.pack('!B',int(s,16))

    return p

binize = Binize # alias

def Denary2BinaryStr(n, l = 8):
    """ Convert denary integer n to binary string bs, left pad to length l"""
    bs = ''
    if n < 0:  raise ValueError("must be a positive integer")
    if n == 0: return '0'
    while n > 0:
        bs = str(n % 2) + bs
        n = n >> 1
    return bs.rjust(l,'0')

denary2BinaryStr = Denary2BinaryStr # alias

def Dec2BinStr(n, count=24):
    """ returns the binary formated string of integer n, using count number of digits"""
    return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])

dec2BinStr = Dec2BinStr # alias

def PrintHex(s, chunk = 0, chunks = 0, silent = False, separator = '.'):
    """prints elements of bytes string s in hex notation.

       chunk is number of bytes per chunk
       0 means no chunking
       chunks is the number of chunks per line
       0 means no new lines

       silent = True means return formatted string but do not print
    """
    if (chunk < 0):
        raise ValueError("invalid size of chunk")

    if (chunks < 0):
        raise ValueError("invalid chunks per line")

    slen = len(s)

    if chunk == 0:
        chunk = slen

    if chunks == 0:
        line = slen
    else:
        line = chunk * chunks

    cc = 0
    ps = ''
    for i in range(len(s)):
        ps += ("%02x" % ord(s[i:i+1]))
        #add space or dot if not end of line or end of string
        if ((i + 1) % line) and ((i+1) % slen):
            if not ((i + 1) % chunk): #end of chunk
                ps += ' ' #space between chunks
            else:
                ps += separator #between bytes in chunk
        elif (i + 1) != slen: # newline if not last line
            ps += '\n' #newline

    if not silent:
        console.terse("{0}\n".format(ps))

    return ps

printHex = PrintHex # alias

def PrintDecimal(s):
    """prints elements of string s in decimal notation.

    """
    ps = ''
    for i in range(len(s)):
        ps = ps + ("%03d." % ord(s[i:i+1]))
    ps = ps[0:-1] #strip trailing .
    print(ps)

printDecimal = PrintDecimal # alias

def CRC16(inpkt):
    """ Returns 16 bit crc or inpkt packed binary string
        compatible with ANSI 709.1 and 852
        inpkt is bytes in python3 or str in python2
        needs struct module
    """
    inpkt = bytearray(inpkt)
    poly = 0x1021  # Generator Polynomial
    crc = 0xffff
    for element in inpkt :
        i = 0
        #byte = ord(element)
        byte = element
        while i < 8 :
            crcbit = 0x0
            if (crc & 0x8000):
                crcbit = 0x01
            databit = 0x0
            if (byte & 0x80):
                databit = 0x01
            crc = crc << 1
            crc = crc & 0xffff
            if (crcbit != databit):
                crc = crc ^ poly
            byte = byte << 1
            byte = byte & 0x00ff
            i += 1
    crc = crc ^ 0xffff
    return struct.pack("!H",crc )

crc16 = CRC16 # alias

def CRC64(inpkt) :
    """ Returns 64 bit crc of inpkt binary packed string inpkt
        inpkt is bytes in python3 or str in python2
        returns tuple of two 32 bit numbers for top and bottom of 64 bit crc
    """
    inpkt = bytearray(inpkt)
    polytop = 0x42f0e1eb
    polybot = 0xa9ea3693
    crctop  = 0xffffffff
    crcbot  = 0xffffffff
    for element in inpkt :
        i = 0
        #byte = ord(element)
        byte = element
        while i < 8 :
            topbit = 0x0
            if (crctop & 0x80000000):
                topbit = 0x01
            databit = 0x0
            if (byte & 0x80):
                databit = 0x01
            crctop = crctop << 1
            crctop = crctop & 0xffffffff
            botbit = 0x0
            if (crcbot & 0x80000000):
                botbit = 0x01
            crctop = crctop | botbit
            crcbot = crcbot << 1
            crcbot = crcbot & 0xffffffff
            if (topbit != databit):
                crctop = crctop ^ polytop
                crcbot = crcbot ^ polybot
            byte = byte << 1
            byte = byte & 0x00ff
            i += 1
    crctop = crctop ^ 0xffffffff
    crcbot = crcbot ^ 0xffffffff
    return (crctop, crcbot)

crc64 = CRC64 # alias

def ocfn(filename, openMode = 'r+', binary=False):
    """Atomically open or create file from filename.

       If file already exists, Then open file using openMode
       Else create file using write update mode If not binary Else
           write update binary mode
       Returns file object

       If binary Then If new file open with write update binary mode
    """
    try:
        newfd = os.open(filename, os.O_EXCL | os.O_CREAT | os.O_RDWR, 436) # 436 == octal 0664
        if not binary:
            newfile = os.fdopen(newfd,"w+")
        else:
            newfile = os.fdopen(newfd,"w+b")
    except OSError as ex:
        if ex.errno == errno.EEXIST:
            newfile = open(filename, openMode)
        else:
            raise
    return newfile

Ocfn = ocfn # alias

def Load(file = ""):
    """Loads object from pickled file, returns object"""

    if not file:
        raise ParameterError("No file to Load form: {0}".format(file))

    f = open(file,"r+")
    p = pickle.Unpickler(f)
    it = p.load()
    f.close()
    return it

load = Load

def Dump(it = None, file = ""):
    """Pickles  it object to file"""

    if not it:
        raise ParameterError("No object to Dump: {0}".format(str(it)))

    if not file:
        raise ParameterError("No file to Dump to: {0}".format(file))


    f = open(file, "w+")
    p = pickle.Pickler(f)
    p.dump(it)
    f.close()

dump = Dump

def DumpJson(it = None, filename = "", indent=2):
    """Jsonifys it and dumps it to filename"""
    if not it:
        raise ValueError("No object to Dump: {0}".format(it))

    if not filename:
        raise ValueError("No file to Dump to: {0}".format(filename))

    with ocfn(filename, "w+") as f:
        json.dump(it, f, indent=2)
        f.flush()
        os.fsync(f.fileno())

dumpJson = DumpJson

def LoadJson(filename = ""):
    """ Loads json object from filename, returns unjsoned object"""
    if not filename:
        raise ParameterError("Empty filename to load.")

    with ocfn(filename) as f:
        try:
            it = json.load(f, object_pairs_hook=odict())
        except EOFError:
            return None
        except ValueError:
            return None
        return it

loadJson = LoadJson

