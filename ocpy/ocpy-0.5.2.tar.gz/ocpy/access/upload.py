from __future__ import print_function
import requests
import h5py
import os
import numpy
from PIL import Image
import time

from enums import *
from Request import *


def put_data(token, channel, data, x_start, y_start, z_start, channel_type="image", server=DEFAULT_SERVER, x_stop=0, y_stop=0, z_stop=0, filename="tmp.hdf5"):
    """
    Upload data onto the OCP server.

    Arguments:
        :server:        ``string : ocpy.access.enums.DEFAULT_SERVER`` The server to access
        :token:         ``string`` The token to upload (must be read/write)
        :channel:       ``string`` The token to upload (must be read/write)
        :data:          ``numpy.ndarray`` The data to upload
        :q_start:       ``int`` Lower bound of Q dimension
        :q_stop:        ``int : 0`` Upper bound of Q dimension. If omitted, is
                        autopopulated to contain q_start + data-size.
        :filename:      A temporary HDF5 file to stream to the server.

    Returns:
        : bool : Success of the call (True/False).
    """

    # Handle unset q_stops for dimension 'q'
    if x_stop == 0: x_stop = x_start + data.shape[0]
    if y_stop == 0: y_stop = y_start + data.shape[1]
    if z_stop == 0: z_stop = z_start + data.shape[2]

    # Throw exceptions if there has been a set dataset shape that
    # is not matched by the shape of the data
    if (x_stop - x_start) != data.shape[0]:
        raise DataSizeError("Bad fit: x-range")
    if (y_stop - y_start) != data.shape[1]:
        raise DataSizeError("Bad fit: y-range")
    if (z_stop - z_start) != data.shape[2]:
        raise DataSizeError("Bad fit: z-range")

    # TODO: Use h5py dataset casting
    datatype = 'u' + data.dtype.name if '64' in data.dtype.name else 'uint32'
    datatype = 'uint32'

    # Create an HDF5 file that holds the data in order to send it
    fout = h5py.File(filename, driver="core", backing_store=True)
    fgroup = fout.create_group(channel)
    fgroup.create_dataset("CUTOUT", data.shape, data.dtype, compression="gzip", data=data)
    fgroup.create_dataset("DATATYPE", (1,), dtype=h5py.special_dtype(vlen=str), data=datatype)
    fgroup.create_dataset("CHANNELTYPE", (1,), dtype=h5py.special_dtype(vlen=str), data=channel_type)
    fout.close()

    # Create a request that holds the URL of the API endpoint
    req = Request(
        token =         token,
        channel =       channel,
        x_start =       x_start,
        x_stop =        x_stop,
        y_start =       y_start,
        y_stop =        y_stop,
        z_start =       z_start,
        z_stop =        z_stop,
        resolution =    "0",
        format =        "hdf5"
    )

    url = req.to_url()

    with open(filename, 'rb') as payload:
        req = requests.post(url, data=payload.read())

    # If we return !200, clearly something went wrong...
    if req.status_code == 200:
        return True
    else:
        o = open('out.html', 'w+')
        o.write(req.text)
        return req.status_code
