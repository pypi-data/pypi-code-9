from __future__ import print_function
import requests
import h5py
import os
import numpy
from PIL import Image
import time

from enums import *
from Request import *

def get_info(token, server=DEFAULT_SERVER):
    """
    Get information about a dataset from its token, using the /info endpoint.

    Arguments:
        :token:     ``string`` The token identifying the dataset to investigate

    Returns:
        JSON object containing the content of the /info page.
    """
    url = '/'.join([server, 'ocp', 'ca', token, 'info', ''])
    req = requests.get(url)
    return req.json()



def snap_to_cube(q_start, q_stop, chunk_depth=16, q_index=1):
    """
    For any q in {x, y, z, t}
    Takes in a q-range and returns a 1D bound that starts at a cube
    boundary and ends at another cube boundary and includes the volume
    inside the bounds. For instance, snap_to_cube(2, 3) = (1, 17)

    Arguments:
        :q_start:       `int` The lower bound of the q bounding box of volume
        :q_stop:        `int` The upper bound of the q bounding box of volume
        :chunk_depth:   `int : CHUNK_DEPTH` The size of the chunk in this volume (use ``get_info()``)
        :q_index:       `int : 1` The starting index of the volume (in q)
    Returns:
        :2-tuple: ``(lo, hi)`` bounding box for the volume
    """
    lo = 0; hi = 0
    # Start by indexing everything at zero for our own sanity
    q_start -= q_index; q_stop -= q_index

    if q_start % chunk_depth == 0:
        lo = q_start
    else:
        lo = q_start - (q_start % chunk_depth)

    if q_stop % chunk_depth == 0:
        hi = q_stop
    else:
        hi = q_stop + (chunk_depth - q_stop % chunk_depth)

    return (lo + q_index, hi + q_index + 1)


def get_data(token,
             channel,
             x_start, x_stop,
             y_start, y_stop,
             z_start, z_stop,
             resolution,
             fmt=DEFAULT_FORMAT,
             server=DEFAULT_SERVER,
             location="./",
             ask_before_writing=False,
             chunk_depth=CHUNK_DEPTH):
    """
    Get data from the OCP server.

    Arguments:
        :server:                ``string : DEFAULT_SERVER`` Internet-facing server. Must include protocol (e.g. ``https``).
        :token:                 ``string`` Token to identify data to download
        :channel:               ``string`` Channel
        :fmt:                   ``string : 'hdf5'`` The desired output format
        :resolution:            ``int`` Resolution level
        :Q_start:               ``int`` The lower bound of dimension 'Q'
        :Q_stop:                ``int`` The upper bound of dimension 'Q'
        :location:              ``string : './'`` The on-disk location where we'll create /hdf5
        :ask_before_writing:    ``boolean : False`` Whether to ask (y/n) before creating directories. Default value is `False`.

    Returns:
        :``string[]``: Filenames that were saved to disk.
    """

    total_size = (x_stop - x_start) * (y_stop - y_start) * (z_stop - z_start) * (14./(1000.*1000.*16.))
    print("Downloading approximately " + str(total_size) + " MB.\n")

    # Remember cwd so that we can cd back to it after we finish.
    cur_dir = os.getcwd()

    # Figure out where we'll be saving files. If the directories don't
    # exist, let's create them now.
    location = location if location else os.getcwd()
    try:
        os.mkdir(location)
    except Exception as e:
        print("Directory /" + location + " already exists, not creating.")

    os.chdir(location)

    try:
        os.mkdir('hdf5');
    except Exception as e:
        print("Data directory already exists, not creating /hdf5.")

    if ask_before_writing:
        confirm = raw_input("The data will be saved to /" + location + ".\n" +
              "Continue? [yn] ")
        if confirm is 'n':
            return False;

    fmt = "hdf5" # Hard-coded for now to minimize server-load

    # The array of local files that we create
    local_files = []
    failed_files = []


    proj_info = get_info(token=token, server=server)
    z_cube_size = proj_info['dataset']['cube_dimension'][str(resolution)][2]
    z_index = proj_info['dataset']['offset'][str(resolution)][2]
    z_bounds = snap_to_cube(z_start, z_stop, chunk_depth=z_cube_size, q_index=z_index)

    # Cursor to keep track of progress through volume
    cursor = z_start

    if z_stop - z_start <= z_cube_size:
        result = _download_data(server, token, channel, fmt, resolution,
                                x_start, x_stop, y_start, y_stop, z_start, z_stop, "hdf5")
        if result[0] is False:
            print(" !! Failed on " + result[1])
            failed_files.append(result[1])
        else:
            local_files.append(result[1])
    else:
        result = _download_data(server, token, channel, fmt, resolution,
                        x_start, x_stop, y_start, y_stop, z_start, z_bounds[0] + z_cube_size, "hdf5")
        cursor = z_bounds[0] + z_cube_size
        if result[0] is False:
            print(" !! Failed on " + result[1])
            failed_files.append(result[1])
        else:
            local_files.append(result[1])

        while cursor < z_stop:
            stop_at = min(z_stop, cursor + z_cube_size)
            result = _download_data(server, token, channel, fmt, resolution,
                                    x_start, x_stop, y_start, y_stop, cursor, stop_at, "hdf5")
            cursor = stop_at
            if result[0] is False:
                print(" !! Failed on " + result[1])
                failed_files.append(result[1])
            else:
                local_files.append(result[1])

    # We now have an array, `local_files`, holding all of the
    # files that we downloaded, as well as a list of `failed_files`
    # that were not downloaded successfully. That is, there SHOULD
    # have been files named as per failed_files, but they did not
    # succeeed. (See Request.Request for a way to convert them to urls)

    # Return to starting directory
    os.chdir(cur_dir)
    return (local_files, failed_files)



def _download_data(server, token, channel, fmt, resolution, x_start, x_stop, y_start, y_stop, z_start, z_stop, location):
    """
    Download the actual data from the server. Uses 1MB chunks when saving.
    Returns the filename stored locally. Specify a save-location target in get_data.
    """
    print("Downloading " + str(z_start) + "-" + str(z_stop))
    # Build a string that holds the full URL to request.

    req = Request(
        server = server,
        token = token,
        channel = channel,
        format = fmt,
        resolution = resolution,
        x_start = x_start,
        x_stop = x_stop,
        y_start = y_start,
        y_stop = y_stop,
        z_start = z_start,
        z_stop = z_stop
    )

    request_url = req.to_url()
    file_name   = location + "/" + req.to_filename()

    # Create a `requests` object.
    req = requests.get(request_url, stream=True)
    if req.status_code is not 200:
        print(" !! Error encountered... Trying again in 5s...")
        # Give the server five seconds to catch its breath
        # TODO: ugh
        time.sleep(5)
        req2 = requests.get(request_url, stream=True)
        if req2.status_code is not 200:
            return (False, file_name)
        else:
            req = req2
    # Now download (chunking to 1024 bytes from the stream)
    with open(file_name, 'wb+') as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()

    return (True, file_name)
