from enums import *

class Request(object):

    def __init__(self, *args, **kwargs):
        if len(args) == 1:
            if type(args[0]) is str:
                url = args[0]
                if url.startswith('http'):
                    self._init_from_url(url)
                else:
                    self._init_from_filename(url)
            elif type(args[0]) is tuple:
                self._init_from_ordered_tuple(args[0])
            else:
                raise ValueError("Unsupported constructor for type {0}".format(type(args[0])))
        else:
            self._init_from_individual_values(**kwargs)

    def _init_from_filename(self, fname):
        # Remove file extension
        fname = ''.join(fname.split('.')[:-1])
        self._init_from_url(fname, delimiter="-")

    def _init_from_url(self, url, delimiter='/'):
        """
        protocol://server/ocp/ca/token/fmt/res/x_start,x_stop/y_start,y_stop/z_start,z_stop/
        """
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
                        server=DEFAULT_SERVER, token="",
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
        self.x_start = x_start
        self.x_stop = x_stop
        self.y_start = y_start
        self.y_stop = y_stop
        self.z_start = z_start
        self.z_stop = z_stop
        self.resolution = resolution
        self.format = format

    def to_url(self):
        return '/'.join([
            self.protocol + ":/",
            self.server,
            "ocp",
            "ca",
            self.token,
            self.format,
            str(self.resolution),
            str(self.x_start) + "," + str(self.x_stop),
            str(self.y_start) + "," + str(self.y_stop),
            str(self.z_start) + "," + str(self.z_stop),
        ""])

    def to_filename(self):
        return '-'.join([
            self.server,
            "ocp",
            "ca",
            self.token,
            self.format,
            str(self.resolution),
            str(self.x_start).zfill(6) + "," + str(self.x_stop).zfill(6),
            str(self.y_start).zfill(6) + "," + str(self.y_stop).zfill(6),
            str(self.z_start).zfill(6) + "," + str(self.z_stop).zfill(6) + "." + self.format
        ])
