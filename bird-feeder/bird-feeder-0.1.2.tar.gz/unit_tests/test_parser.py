import nose
from nose.tools import ok_

from birdfeeder.parser import NetCDFParser

def test_netcdf_parser():
    parser = NetCDFParser(start_dir='.')
