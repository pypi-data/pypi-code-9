import functools

import vstruct
from vstruct import VStruct
from vstruct.primitives import v_wstr
from vstruct.primitives import v_enum
from vstruct.primitives import v_bytes
from vstruct.primitives import v_float
from vstruct.primitives import v_uint8
from vstruct.primitives import v_uint16
from vstruct.primitives import v_uint32
from vstruct.primitives import v_uint64

from vstructui import BasicVstructParserSet


CIM_TYPES = v_enum()
CIM_TYPES.CIM_TYPE_LANGID = 0x3
CIM_TYPES.CIM_TYPE_REAL32 = 0x4
CIM_TYPES.CIM_TYPE_STRING = 0x8
CIM_TYPES.CIM_TYPE_BOOLEAN = 0xB
CIM_TYPES.CIM_TYPE_UINT8 = 0x11
CIM_TYPES.CIM_TYPE_UINT16 = 0x12
CIM_TYPES.CIM_TYPE_UINT32 = 0x13
CIM_TYPES.CIM_TYPE_UINT64 = 0x15
CIM_TYPES.CIM_TYPE_DATETIME = 0x65

CIM_TYPE_SIZES = {
    CIM_TYPES.CIM_TYPE_LANGID: 4,
    CIM_TYPES.CIM_TYPE_REAL32: 4,
    CIM_TYPES.CIM_TYPE_STRING: 4,
    CIM_TYPES.CIM_TYPE_BOOLEAN: 2,
    CIM_TYPES.CIM_TYPE_UINT8: 1,
    CIM_TYPES.CIM_TYPE_UINT16: 2,
    CIM_TYPES.CIM_TYPE_UINT32: 4,
    CIM_TYPES.CIM_TYPE_UINT64: 8,
    # looks like: stringref to "\x00 00000000000030.000000:000"
    CIM_TYPES.CIM_TYPE_DATETIME: 4
}


ARRAY_STATES = v_enum()
ARRAY_STATES.NOT_ARRAY = 0x0
ARRAY_STATES.ARRAY = 0x20

BOOLEAN_STATES = v_enum()
BOOLEAN_STATES.FALSE = 0x0
BOOLEAN_STATES.TRUE = 0xFFFF


class CimType(vstruct.VStruct):
    def __init__(self):
        vstruct.VStruct.__init__(self)
        self.type = v_uint8(enum=CIM_TYPES)
        self.array_state = v_uint8(enum=ARRAY_STATES)
        self.unk0 = v_uint8()
        self.unk2 = v_uint8()

    @property
    def is_array(self):
        # TODO: this is probably a bit-flag
        return self.array_state == ARRAY_STATES.ARRAY

    @property
    def value_parser(self):
        if self.is_array:
            return v_uint32
        elif self.type == CIM_TYPES.CIM_TYPE_LANGID:
            return v_uint32
        elif self.type == CIM_TYPES.CIM_TYPE_REAL32:
            return v_float
        elif self.type == CIM_TYPES.CIM_TYPE_STRING:
            return v_uint32
        elif self.type == CIM_TYPES.CIM_TYPE_BOOLEAN:
            return functools.partial(v_uint16, enum=BOOLEAN_STATES)
        elif self.type == CIM_TYPES.CIM_TYPE_UINT8:
            return v_uint8
        elif self.type == CIM_TYPES.CIM_TYPE_UINT16:
            return v_uint16
        elif self.type == CIM_TYPES.CIM_TYPE_UINT32:
            return v_uint32
        elif self.type == CIM_TYPES.CIM_TYPE_UINT64:
            return v_uint64
        elif self.type == CIM_TYPES.CIM_TYPE_DATETIME:
            return v_uint32
        else:
            raise RuntimeError("unknown qualifier type: %s", h(self.type))

    def __repr__(self):
        r = ""
        if self.is_array:
            r += "arrayref to "
        r += CIM_TYPES.vsReverseMapping(self.type)
        return r


def vsEntryVstructParser():
    return BasicVstructParserSet((CimType,))

