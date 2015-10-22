import exifread
from iptcinfo import IPTCInfo

__all__ = ['get_metadata']


def convert_to_utf8(val):
    """
    Convert the string or list into utf8 values
    """
    if isinstance(val, basestring):
        try:
            return val.encode('utf-8')
        except UnicodeDecodeError:
            return val.decode('iso8859_1').encode('utf-8')
    if isinstance(val, (list, tuple)):
        replacement = []
        for i in val:
            if isinstance(i, basestring):
                replacement.append(i.encode('utf-8'))
            else:
                replacement.append(i)
        if len(replacement) == 1:
            return replacement[0]
        return replacement


def get_metadata(filepath):
    """
    Return a dict with the metadata for the filepath
    """
    # Do the EXIF information first, then IPTC
    with open(filepath) as f:
        exif_info = exifread.process_file(f, details=False)

    metadata = {}
    for key, val in exif_info.items():
        metadata[key] = convert_to_utf8(val.values)

    iptc_info = IPTCInfo(filepath)
    for intkey, val in iptc_info.data.viewitems():
        key = iptc_info.data.keyAsStr(intkey)
        metadata[key] = convert_to_utf8(val)

    return metadata
