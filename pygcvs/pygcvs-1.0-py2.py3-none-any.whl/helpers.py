from .parser import GcvsParser

try:
    import ephem
except ImportError:
    ephem = None


def read_gcvs(filename):
    """
    Reads variable star data in `GCVS format`_.

    :param filename: path to GCVS data file (usually ``iii.dat``)

    .. _`GCVS format`: http://www.sai.msu.su/gcvs/gcvs/iii/html/
    """
    with open(filename, 'r') as fp:
        parser = GcvsParser(fp)
        for star in parser:
            yield star


def dict_to_body(star_dict):
    """
    Converts a dictionary of variable star data to a `Body` instance.

    Requires `PyEphem <http://rhodesmill.org/pyephem/>`_ to be installed.
    """
    if ephem is None:
        raise NotImplementedError("Please install PyEphem in order to use dict_to_body.")
    body = ephem.FixedBody()
    body.name = star_dict['name']
    body._ra = ephem.hours(str(star_dict['ra']))
    body._dec = ephem.degrees(str(star_dict['dec']))
    body._epoch = ephem.J2000
    return body
