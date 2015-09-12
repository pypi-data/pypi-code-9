DEFAULT_PROTOCOL =  'http'
DEFAULT_SERVER =    'http://openconnecto.me'
DEFAULT_FORMAT =    'hdf5'
CHUNK_DEPTH    =    16

class DataSizeError(Exception):
    """
    An exception to raise when a dataset mismatches its Request,
    or more data is posted than there is 'space' for in the Request.
    Often a result of requesting data and failing with a broken pipe,
    or trying to POST 2D data into a 3D Request.
    """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
