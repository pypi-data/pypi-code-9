from binascii import crc32
import os


def _pretty_byte_string(bytes_read):
    return ''.join("{:02x}".format(ord(x)) for x in bytes_read).upper()


def crc2hex(crc):
    res = ''

    for i in range(4):
        t = crc & 0xFF
        crc >>= 8
        res = '%02X%s' % (t, res)
    return res


offset = 16
filename = 'example_replays/1.04.replay'
filesize = os.path.getsize(filename) - offset

f = open(filename)

# Read the current CRC.
f.seek(4)
crc = _pretty_byte_string(f.read(4))

for length in xrange(1, filesize):
    f.seek(offset)

    if length % 10000 == 0:
        print length, '/', filesize

    if crc2hex(crc32(f.read(length))) == crc:
        print length
        break
