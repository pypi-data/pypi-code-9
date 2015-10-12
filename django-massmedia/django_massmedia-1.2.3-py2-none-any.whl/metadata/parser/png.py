from massmedia.metadata.utils import force_unicode
from types import UInt32, UInt16, UInt8,


def headerParse(parent):
    yield UInt32(parent, "width", "Width (pixels)")
    yield UInt32(parent, "height", "Height (pixels)")
    yield UInt8(parent, "bit_depth", "Bit depth")
    yield NullBits(parent, "reserved", 5)
    yield Bit(parent, "has_alpha", "Has alpha channel?")
    yield Bit(parent, "color", "Color used?")
    yield Bit(parent, "has_palette", "Has a color palette?")
    yield Enum(UInt8(parent, "compression", "Compression method"), COMPRESSION_NAME)
    yield UInt8(parent, "filter", "Filter method")
    yield UInt8(parent, "interlace", "Interlace method")

def headerDescription(parent):
    return "Header: %ux%u pixels and %u bits/pixel" % \
        (parent["width"].value, parent["height"].value, getBitsPerPixel(parent))

def paletteParse(parent):
    size = parent["size"].value
    if (size % 3) != 0:
        raise ParserError("Palette have invalid size (%s), should be 3*n!" % size)
    nb_colors = size // 3
    for index in range(nb_colors):
        yield RGB(parent, "color[]")

def paletteDescription(parent):
    return "Palette: %u colors" % (parent["size"].value // 3)

def gammaParse(parent):
    yield UInt32(parent, "gamma", "Gamma (x100,000)")
def gammaValue(parent):
    return float(parent["gamma"].value) / 100000
def gammaDescription(parent):
    return "Gamma: %.3f" % parent.value

def textParse(parent):
    yield CString(parent, "keyword", "Keyword", charset="ISO-8859-1")
    length = parent["size"].value - parent["keyword"].size//8
    if length:
        yield String(parent, "text", length, "Text", charset="ISO-8859-1")

def textDescription(parent):
    if "text" in parent:
        return 'Text: %s' % parent["text"].display
    else:
        return 'Text'

def timestampParse(parent):
    yield UInt16(parent, "year", "Year")
    yield UInt8(parent, "month", "Month")
    yield UInt8(parent, "day", "Day")
    yield UInt8(parent, "hour", "Hour")
    yield UInt8(parent, "minute", "Minute")
    yield UInt8(parent, "second", "Second")

def timestampValue(parent):
    value = datetime(
        parent["year"].value, parent["month"].value, parent["day"].value,
        parent["hour"].value, parent["minute"].value, parent["second"].value)
    return value

def physicalParse(parent):
    yield UInt32(parent, "pixel_per_unit_x", "Pixel per unit, X axis")
    yield UInt32(parent, "pixel_per_unit_y", "Pixel per unit, Y axis")
    yield Enum(UInt8(parent, "unit", "Unit type"), UNIT_NAME)

def physicalDescription(parent):
    x = parent["pixel_per_unit_x"].value
    y = parent["pixel_per_unit_y"].value
    desc = "Physical: %ux%u pixels" % (x,y)
    if parent["unit"].value == 1:
        desc += " per meter"
    return desc

def parseBackgroundColor(parent):
    yield UInt16(parent, "red")
    yield UInt16(parent, "green")
    yield UInt16(parent, "blue")

def backgroundColorDesc(parent):
    rgb = parent["red"].value, parent["green"].value, parent["blue"].value
    name = RGB.color_name.get(rgb)
    if not name:
        name = "#%02X%02X%02X" % rgb
    return "Background color: %s" % name



class PNGParser(object):
    """
    A parser is used to parse the file to retrieve parts of the file
    """
    TAG_INFO = {
        "tIME": ("time", timestampParse, "Timestamp", timestampValue),
        "pHYs": ("physical", physicalParse, physicalDescription, None),
        "IHDR": ("header", headerParse, headerDescription, None),
        "PLTE": ("palette", paletteParse, paletteDescription, None),
        "gAMA": ("gamma", gammaParse, gammaDescription, gammaValue),
        "tEXt": ("text[]", textParse, textDescription, None),
        "tRNS": ("transparency", parseTransparency, "Transparency Info", None),

        "bKGD": ("background", parseBackgroundColor, backgroundColorDesc, None),
        "IDAT": ("data[]", lambda parent: (ImageData(parent),), "Image data", None),
        "iTXt": ("utf8_text[]", None, "International text (encoded in UTF-8)", None),
        "zTXt": ("comp_text[]", None, "Compressed text", None),
        "IEND": ("end", None, "End", None)
    }

    def __init__(self, filepath, **args):
        self._filepath = filepath

    def parse_chunk(self, stream):


    def parse(self):
        with open(self._filepath, 'r') as f:
            signature = f.read(8)
