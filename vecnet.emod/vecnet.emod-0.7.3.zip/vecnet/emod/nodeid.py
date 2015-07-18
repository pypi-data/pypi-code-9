#
# This file is part of the vecnet.emod package.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/vecnet/vecnet.emod
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License (MPL), version 2.0.  If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.


def nodeIDToLatLong(nodeID, resolution):
    """
    Get latitude and longitude of a EMOD demographics node based on it's ID and grid resolution

    Please refer to
    http://idmod.org/emoddoc/#EMOD/FileFormatLayouts/IdReference Types and NodeID.htm
    for additional information about IdReference Types and NodeID Generation

    :param nodeID: node ID in demographics file
    :param resolution: Geospatial resolution of the grid. Example: "2.5 arcmin"
    :type resolution: str
    :return: latitude, longitude
    :rtype: tuple
    """
    try:
        nodeID = int(nodeID)
    except ValueError:
        raise ValueError("nodeID must be an integer or a string of an integer")

    resolution = getParsedResolution(resolution)

    return getLatitudeAndLongitude(nodeID, resolution)


def latLongToNodeID(latitude, longitude, resolution):
    try:
        latitude = float(latitude)
    except ValueError:
        raise ValueError("latitude must be a float or a string of a float")
    try:
        longitude = float(longitude)
    except ValueError:
        raise ValueError("longitude must be a float or a string of a float")

    resolution = getParsedResolution(resolution)

    return getNodeID(latitude, longitude, resolution)


def getParsedResolution(resolutionText):
    split_resolution = resolutionText.split(" ")

    if len(split_resolution) != 2:
        raise ValueError("Resolution is invalid. It must be in the form of: Value Type. Example: 2.5 arcmin")

    try:
        resolution = float(split_resolution[0])
    except ValueError:
        raise ValueError("resolution value must be an integer or float. Example: 2.5 arcmin")

    if split_resolution[1] == "degree":
        return resolution
    elif split_resolution[1] == "arcmin":
        return resolution / 60.0
    elif split_resolution[1] == "arcsec":
        return resolution / 3600.0
    else:
        raise ValueError("resolution type must be degree, arcmin, or arcsec. Example: 2.5 arcmin")


def getLatitudeAndLongitude(nodeID, resolution):
    x_factor = (nodeID - 1) / (2**16)
    y_factor = (nodeID - 1) % (2**16)
    longitude = (x_factor * resolution) - 180
    latitude = (y_factor * resolution) - 90
    return latitude, longitude


def getNodeID(latitude, longitude, resolution):
    x_factor = round((longitude + 180.0) / resolution)
    y_factor = round((latitude + 90.0) / resolution)
    return int(x_factor * (2**16) + y_factor + 1)
