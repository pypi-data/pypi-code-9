from enums import *

class Request(object):
    """
    A ocpy Request holds an absolute URL that can be used
    to access a unique datum. Requests can be thought of as
    a Python class wrapper for a RESTful endpoint.
    """
    def __init__(self, *args, **kwargs):
        """
        There are three ways of creating a Request; by URL,
        by filename, by an ordered tuple (in the order of the
        URL, incidentally) or by named variables. For example:

        ``Request('http://openconnecto.me/ocp/ca/tokenName/channelName/hdf5/1/0,10/0,10/0,10/')``

        ``Request('openconnecto.me-ocp-ca-tokenName-channelName-hdf5-1-0,10-0,10-0,10.hdf5')``

        ``Request('http://openconnecto.me', 'tokenName', 'channelName', 'hdf5', '1', '0', '10', '0', '10', '0', '10')``


        ``Request('server=http://openconnecto.me', token='tokenName', channel='channelName', format='hdf5', resolution='1', x_start='0', x_stop='10', y_start='0', y_stop='10', z_start='0', z_stop='10')``

        ...are all equivalent ways of creating a Request.

        These requests are currently all Image/Dense Requests... In a subsequent release, DenseRequest will inherit from a general Request class.
        """
        if len(args) == 1:
            if type(args[0]) is str:
                # Either URL or filename.
                url = args[0]
                if url.startswith('http'):
                    self._init_from_url(url)
                else:
                    self._init_from_filename(url)
            elif type(args[0]) is tuple:
                # Parse from an ordered tuple
                self._init_from_ordered_tuple(args[0])
            else:
                # There is no other way to create a Request from a single argument. Fail here.
                raise ValueError("Unsupported constructor for type {0}".format(type(args[0])))
        else:
            # We should expect named variables for each attribute.
            self._init_from_individual_values(**kwargs)

    def _init_from_filename(self, fname):
        # Remove file extension
        fname = ''.join(fname.split('.')[:-1])
        self._init_from_url(fname, delimiter="-")

    def _init_from_url(self, url, delimiter='/'):
        """
        protocol://server/ocp/ca/token/channel/fmt/res/x_start,x_stop/y_start,y_stop/z_start,z_stop/
        """
        # The delimiter argument is so that we can use the same
        # function for URL and Filename parsing.
        url = url.strip(delimiter)
        split_url = url.split('://')
        if len(split_url) == 2:
            self.protocol, url = split_url
        else:
            self.protocol = DEFAULT_PROTOCOL

        self.server, _, _, self.token, self.format, self.resolution, x_range, y_range, z_range = url.split(delimiter)

        self.x_start, self.x_stop = x_range.split(',')
        self.y_start, self.y_stop = y_range.split(',')
        self.z_start, self.z_stop = z_range.split(',')

    def _init_from_ordered_tuple(self, tuple):
        raise NotImplementedError("Not yet implemented.")

    def _init_from_individual_values(self,
                        server=DEFAULT_SERVER, token="", channel="",
                        x_start="", x_stop="",
                        y_start="", y_stop="", z_start="", z_stop="",
                        resolution="", format=DEFAULT_FORMAT):
        split_server = server.split('://')
        if len(split_server) == 2:
            self.protocol, self.server = split_server
        elif len(split_server) == 1:
            self.protocol = DEFAULT_PROTOCOL
            self.server = server
        else:
            raise ValueError("Invalid server name: {0}".format(server))

        self.token = token
        self.channel = channel
        self.x_start = x_start
        self.x_stop = x_stop
        self.y_start = y_start
        self.y_stop = y_stop
        self.z_start = z_start
        self.z_stop = z_stop
        self.resolution = resolution
        self.format = format

    def to_url(self):
        """
        Output a URL that can be used to execute this Request.

        Arguments:
            None.
        Returns:
            ``str`` RESTful endpoint URL.
        """
        return '/'.join([
            self.protocol + ":/",
            self.server,
            "ocp",
            "ca",
            self.token,
            self.channel,
            self.format,
            str(self.resolution),
            str(self.x_start) + "," + str(self.x_stop),
            str(self.y_start) + "," + str(self.y_stop),
            str(self.z_start) + "," + str(self.z_stop),
        ""])


    def to_filename(self):
        """
        Output a filename that can be used to save data from this
        request and can later be used to create a new Request (using
        the _init_from_filename constructor) to download identical
        data. In that regard, we can use a filename as a unique
        'hash' of its data.

        Arguments:
            None.
        Returns:
            ``str`` Suggested filename for data that has been
            downloaded by this Request.
        """
        return '-'.join([
            self.server,
            "ocp",
            "ca",
            self.token,
            self.channel,
            self.format,
            str(self.resolution),
            str(self.x_start).zfill(6) + "," + str(self.x_stop).zfill(6),
            str(self.y_start).zfill(6) + "," + str(self.y_stop).zfill(6),
            str(self.z_start).zfill(6) + "," + str(self.z_stop).zfill(6) + "." + self.format
        ])
