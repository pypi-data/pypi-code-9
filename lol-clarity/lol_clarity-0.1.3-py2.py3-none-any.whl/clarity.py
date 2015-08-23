import struct
from builtins import bytes
from .hud import Vec2, Rect, LolRect

ELEMENT_SIGNATURE = b'\xdb\xbf\xef\x19\x10'
ANCHOR_SIGNATURE = b'\x19\x6b\x7c\x32\x0b'
POSITION_SIGNATURE = b'\x76\xbc\xf0\x8f\x0d'
RES_W_SIGNATURE = b'\xbb\xef\x24\x2d\x07'
RES_H_SIGNATURE = b'\x56\xc1\x8a\x34\x07'
SOMETHING_BEFORE_ANCHOR_SIGNATURE = b'\xad\xec\xa5\x82\x07' #AD EC A5 82 07

def read_element_property(binary, signature, format):
    if(binary.find(signature) > -1):
        offset = binary.find(signature)
        length = struct.calcsize(format)
        vals = struct.unpack_from(format, binary[(offset + len(signature)):(offset + len(signature) + length)])
        return (offset, vals)
    return None

def read_element_name(binary):
    (name_length, ) = struct.unpack('H', binary[0:2])
    return (2, binary[2:(2 + name_length)].decode('ascii'))

def read_element_anchor(binary):
    try:
        (offset, vals) = read_element_property(binary, ANCHOR_SIGNATURE, 'ff')
        return (offset, Vec2(vals[0], vals[1]))
    except TypeError:
        return (None, Vec2(0,0))


def read_element_position(binary):
    (offset, vals) = read_element_property(binary, POSITION_SIGNATURE, 'ffff')
    return (offset, Rect(Vec2(vals[0], vals[1]), Vec2(vals[2], vals[3])))

#@TODO offset should be stored for both
def read_element_resolution(binary):
    (offset_width, val_w) = read_element_property(binary, RES_W_SIGNATURE, 'I')
    (offset_height, val_h) = read_element_property(binary, RES_H_SIGNATURE, 'I')
    return (offset_width, offset_height, {'width': val_w[0], 'height':val_h[0] } )

class Clarity(object):
    def __init__(self, binary):
        self.elements = {}
        self.items = []
        items = binary.split(ELEMENT_SIGNATURE)
        self.header = UIHeader(items.pop(0))
        self.items.append(self.header)
        for item in items:
            el = UIElement(item)
            self.elements[el.name] = el
            self.items.append(el)

    @classmethod
    def from_binary(cls, binary):
        return cls(binary)

    @classmethod
    def from_file(cls, filename):
        with open(filename, 'rb') as fh:
            return cls(fh.read())

    def to_binary(self):
        binary_items = [item.binary for item in self.items]
        return ELEMENT_SIGNATURE.join(binary_items)

    def to_file(self, filename):
        with open(filename, 'wb') as f:
            f.write(self.to_binary())


class UIHeader(object):
    def __init__(self, binary):
        self.binary = binary

class UIElement(object):
    def __init__(self, binary):
        self.binary = binary
        (self._name_offset, self._name) = read_element_name(binary)
        (self._anchor_offset, self._anchor) = read_element_anchor(binary)
        (self._position_offset, self._position) = read_element_position(binary)
        (self._res_w_offset, self._res_h_offset, self._resolution) = read_element_resolution(binary)

    @property
    def name(self):
        return self._name

    @property
    def resolution(self):
        return self._resolution

    @resolution.setter
    def resolution(self, value):
        assert 'width' in value
        assert 'height' in value
        self._res = value
        packed_res_w = struct.pack('I', value['width'])
        packed_res_h = struct.pack('I', value['height'])
        self.binary = self.binary[:self._res_w_offset] + RES_W_SIGNATURE + packed_res_w + self.binary[self._res_w_offset + len(RES_W_SIGNATURE) + 4:]
        self.binary = self.binary[:self._res_h_offset] + RES_H_SIGNATURE + packed_res_h + self.binary[self._res_h_offset + len(RES_H_SIGNATURE) + 4:]

    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, value):
        assert isinstance(value, Vec2)
        self._anchor = value
        packed = struct.pack('ff', value.x, value.y)

        #@TODO: refactor me :)
        if(value.x == 0 and value.y == 0):
            # omit entirely if anchor is 0,0 (?)
            if(self._anchor_offset is not None):
                # previous had anchor but now shouldn't
                # cut out the anchor bit:
                self.binary = self.binary[:self._anchor_offset] + self.binary[(self._anchor_offset + len(ANCHOR_SIGNATURE) + 8):]
                # set anchor to none
                self._anchor_offset = None
        else:
            if(self._anchor_offset is None):
                # previously didn't have anchor but now should have
                self._anchor_offset = self.binary.find(SOMETHING_BEFORE_ANCHOR_SIGNATURE) + len(SOMETHING_BEFORE_ANCHOR_SIGNATURE) + 4
                self.binary = self.binary[:self._anchor_offset] + ANCHOR_SIGNATURE + packed + self.binary[self._anchor_offset:]
            self.binary = self.binary[:self._anchor_offset] + ANCHOR_SIGNATURE + packed + self.binary[(self._anchor_offset + len(ANCHOR_SIGNATURE) + 8):]

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        assert isinstance(value, Rect)
        self._position = value
        packed = struct.pack('ffff', value.start.x, value.start.y, value.end.x, value.end.y)
        self.binary = self.binary[:self._position_offset] + POSITION_SIGNATURE + packed + self.binary[(self._position_offset + len(POSITION_SIGNATURE) + 16):]

    @property
    def rect(self):
        return LolRect(self.position.start, self.position.end, self.resolution['width'], self.resolution['height'])

    @rect.setter
    def rect(self, value):
        assert isinstance(value, LolRect)
        self.position = Rect(value.start, value.end)
        self.resolution = {
            'width': value.res_w,
            'height': value.res_h
        }

