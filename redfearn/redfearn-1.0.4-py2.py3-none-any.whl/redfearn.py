# Copyright 2015, Phil Howarth (phil@plaintech.net.au)
#
# This file is part of Redfearn.
# Redfearn is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Redfearn is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Redfearn.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division
import math
from collections import namedtuple


DMS = namedtuple('DMS', 'degrees minutes seconds')


def merge_two_dicts(x, y):
    """ Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z


def decdeg2dms(dd):
    """ Converts a decimal degree value of the for -37.4568 into a DMS namedtuple type with degrees, minutes, seconds.
    :param dd: float
    :return: namedtuple DMS
    """
    negative = dd < 0
    dd = abs(dd)
    minutes, seconds = divmod(dd*3600, 60)
    degrees, minutes = divmod(minutes, 60)
    if negative:
        if degrees > 0:
            degrees = -degrees
        elif minutes > 0:
            minutes = -minutes
        else:
            seconds = -seconds
    return DMS(degrees, minutes, seconds)


def dms2decdeg(dms):
    """ Converts the DMS namedtuple into a decimal expansion of the degrees.
    :param dms: namedtuple DMS
    :return: float
    """
    dd = abs(dms.degrees) + abs(dms.minutes)/60 + abs(dms.seconds)/3600
    if dms.degrees < 0 or dms.minutes < 0 or dms.seconds < 0:
        dd = -dd
    return dd


def ellipsoid_constants(name):
    """ Gets known ellipsoid constants vor various coordinate systems as defined in "Geocentric Datum of Australia, Technical Manual, Version 2.3 Amendment 1".
    :param name: string
    :return: dict
    """
    if name == 'GRS80':
        semi_major_axis = 6378137.000
        inverse_flattening = 298.257222101000
    elif name == 'WGS84':
        semi_major_axis = 6378137.000
        inverse_flattening = 298.257223563000
    elif name == 'ANS':
        semi_major_axis = 6378160.000
        inverse_flattening = 298.25
    elif name == 'Clarke 1858':
        semi_major_axis = 6378293.645
        inverse_flattening = 294.26
    else:
        raise ValueError('invalid ellipsoid name: "{}"'.format(name))
    return {'semi_major_axis': semi_major_axis, 'inverse_flattening': inverse_flattening}


def tm_constants(name):
    """ Gets known transverse mercator projection constants vor various coordinate systems as defined in "Geocentric Datum of Australia, Technical Manual, Version 2.3 Amendment 1".
    :param name: string
    :return: dict
    """
    if name == 'GDA-MGA':
        false_easting = 500000.0000
        false_northing = 10000000.0000
        central_scale_factor = 0.9996
        zone_width_degrees = 6
        longitude_of_the_central_meridian_of_zone_1_degrees = -177
    elif name == 'ANG':
        false_easting = 300000.0000
        false_northing = 5000000.0000
        central_scale_factor = 0.99994
        zone_width_degrees = 2
        longitude_of_the_central_meridian_of_zone_1_degrees = 141
    elif name == 'ISG':
        false_easting = 365760.0000
        false_northing = 4495019.83
        central_scale_factor = 1.0
        zone_width_degrees = 5
        longitude_of_the_central_meridian_of_zone_1_degrees = 116
    else:
        raise ValueError('invalid transverse mercator name: "{}"'.format(name))
    return {
        'false_easting': false_easting,
        'false_northing': false_northing,
        'central_scale_factor': central_scale_factor,
        'zone_width_degrees': zone_width_degrees,
        'longitude_of_the_central_meridian_of_zone_1_degrees': longitude_of_the_central_meridian_of_zone_1_degrees
    }


def coordinate_system_constants(name):
    """ Collates the known ellipsoid and transverse mercator projection constants for various coordinate systems
    :param name:
    :return: dict
    """
    if name == 'GDA/MGA' or name == 'GDA-MGA' or name == 'GDA' or name == 'MGA':
        ellipsoid = 'GRS80'
        tm = 'GDA-MGA'
    elif name == 'WGS84':
        ellipsoid = 'WGS84'
        tm = 'GDA-MGA'
    elif name == 'AGD/AMG' or name == 'AGD' or name == 'AMG':
        ellipsoid = 'ANS'
        tm = 'GDA-MGA'
    elif name == 'ANG':
        ellipsoid = 'Clarke 1858'
        tm = 'ANG'
    elif name == 'ISG':
        ellipsoid = 'ANS'
        tm = 'ISG'
    else:
        raise ValueError('unknown coordinate system: "{}"'.format(name))

    e_constants = ellipsoid_constants(ellipsoid)
    t_constants = tm_constants(tm)
    return merge_two_dicts(e_constants, t_constants)


def check_latlon_type(val):
    """ Checks whether a given latitude or longitude is a float or a DMS type and returns the decimal value
    :param val: float or DMS
    :return: float
    """
    try:
        r = float(val)
    except TypeError:
        try:
            r = dms2decdeg(val)
        except ValueError:
            raise
    return r


# latitude and longitude should be in degrees
def latlon2grid(latitude, longitude, coordinate_system=None, zone=None):
    """ Convert latitude and longitude to grid coordinates using the Redfearn Formula
    :param latitude: float (decimal degrees i.e. from dms2decdeg(dms))
    :param longitude: float (decimal degrees i.e. from dms2decdeg(dms))
    :param coordinate_system: str
    :param zone: int
    :return: dict
    """
    if coordinate_system is None:
        coordinate_system = 'GDA-MGA'
    constants = coordinate_system_constants(coordinate_system)

    # check whether latitude and longitude are in decimal form
    try:
        latitude = check_latlon_type(latitude)
        longitude = check_latlon_type(longitude)
    except ValueError:
        raise ValueError('latitude and longitude should be decimal degrees or DMS types as returned by dms2decdeg and decdeg2dms')
    # refer to Geocentric Datum of Australia, Technical Manual, Version 2.3 Amendment 1
    # pages 18 - 21

    # latitude in radians
    latitude_rad = math.radians(latitude)
    s = math.sin(latitude_rad)
    s2 = math.pow(s, 2)
    c = math.cos(latitude_rad)
    c3 = math.pow(c, 3)
    c5 = math.pow(c, 5)
    c7 = math.pow(c, 7)
    t = math.tan(latitude_rad)
    t2 = math.pow(t, 2)
    t4 = math.pow(t, 4)
    t6 = math.pow(t, 6)
    a = constants['semi_major_axis']
    i_f = constants['inverse_flattening']
    # flattening
    f = 1/i_f
    # semi-minor axis
    b = a*(1-f)
    # eccentricity squared, ^4, ^6
    e2 = (math.pow(a, 2) - math.pow(b, 2))/math.pow(a, 2)
    e4 = math.pow(e2, 2)
    e6 = math.pow(e2, 3)

    longitude_of_western_edge_of_zone_zero_degrees = constants['longitude_of_the_central_meridian_of_zone_1_degrees'] - (1.5 * constants['zone_width_degrees'])
    central_meridian_of_zone_zero_degrees = longitude_of_western_edge_of_zone_zero_degrees + (constants['zone_width_degrees'] / 2)
    zone_no_real = (longitude - longitude_of_western_edge_of_zone_zero_degrees) / constants['zone_width_degrees']
    if zone is None:
        zone = int(math.floor(zone_no_real))
    central_meridian = (zone * constants['zone_width_degrees']) + central_meridian_of_zone_zero_degrees

    # calculate meridian distance
    a0 = 1 - (e2/4) - (3*e4/64) - (5*e6/256)
    a2 = (3/8)*(e2 + e4/4 + 15*e6/128)
    a4 = (15/256)*(e4 + 3*e6/4)
    a6 = 35*e6/3072
    # meridian distance
    m = a*(a0*latitude_rad - a2*math.sin(2*latitude_rad) + a4*math.sin(4*latitude_rad) - a6*math.sin(6*latitude_rad))

    # calculate radius of curvature
    rho = a*(1-e2) / math.pow(1-e2*s2, 3/2)
    nu = a / math.sqrt(1-e2*s2)
    # radius of curvature
    psi = nu / rho
    psi2 = math.pow(psi, 2)
    psi3 = math.pow(psi, 3)
    psi4 = math.pow(psi, 4)
    omega = math.radians(longitude - central_meridian)
    omega2 = math.pow(omega, 2)
    omega4 = math.pow(omega, 4)
    omega6 = math.pow(omega, 6)
    omega8 = math.pow(omega, 8)

    # Easting
    easting_term1 = (omega2/6)*c3*(psi-t2)
    easting_term2 = (omega4/120) * c5 * (4*psi3*(1-6*t2) + psi2*(1+8*t2) - psi*2*t2 + t4)
    easting_term3 = (omega6/5040)*c7*(61-479*t2+179*t4-t6)
    eprime = (constants['central_scale_factor'] * nu * omega) * (c + easting_term1 + easting_term2 + easting_term3)
    easting = eprime + constants['false_easting']

    # Northing
    northing_term1 = (omega2/2)*nu*s*c
    northing_term2 = (omega4/24)*nu*s*c3*(4*psi2 + psi - t2)
    northing_term3 = (omega6/720)*nu*s*c5*(8*psi4*(11-24*t2) - 28*psi3*(1-6*t2) + psi2*(1-32*t2) - psi*(2*t2) + t4)
    northing_term4 = (omega8/40320)*nu*s*c7*(1385 - 3111*t2 + 543*t4 - t6)
    true_northing = constants['central_scale_factor']*(m + northing_term1 + northing_term2 + northing_term3 + northing_term4)
    northing = true_northing + constants['false_northing']

    # grid convergence
    gc_term1 = 1
    gc_term2 = (omega2/3)*c3*(2*psi2 - psi)
    gc_term3 = (omega4/15)*c5*(psi4*(11-24*t2) - psi3*(11-36*t2) + 2*psi2*(1-7*t2) + psi*t2)
    gc_term4 = (omega6/315)*c7*(17 - 26*t2 + 2*t4)
    gc = math.degrees((-omega*s)*(gc_term1 + (1/c)*(gc_term2 + gc_term3 + gc_term4)))

    # point scale factor
    psf_term1 = (omega2/2)*psi*c
    psf_term2 = (omega4/24)*c3*(4*psi3*(1-6*t2) + psi2*(1+24*t2) - 4*psi*t2)
    psf_term3 = (omega6/720)*c5*(61 - 148*t2 + 16*t4)
    psf = constants['central_scale_factor']*(1 + c*(psf_term1 + psf_term2 + psf_term3))

    return {
        'easting': easting,
        'northing': northing,
        'zone': zone,
        'grid_convergence': gc,
        'point_scale_factor': psf
    }


def grid2latlon(easting, northing, zone, coordinate_system=None):
    """ Converts grid coordinates to latitude and longitude values using the Redfearn Formula
    :param easting: float
    :param northing: float
    :param zone: int
    :param coordinate_system: string
    :return: dict
    """
    if coordinate_system is None:
        coordinate_system = 'GDA-MGA'
    constants = coordinate_system_constants(coordinate_system)
    # refer to Geocentric Datum of Australia, Technical Manual, Version 2.3 Amendment 1
    # pages 18 - 21

    # semi-major axis
    a = constants['semi_major_axis']
    # inverse flattening
    i_f = constants['inverse_flattening']
    # flattening
    f = 1/i_f
    # semi-minor axis
    b = a*(1-f)
    # eccentricity squared, ^4, ^6
    e2 = (math.pow(a, 2) - math.pow(b, 2))/math.pow(a, 2)

    eprime = easting - constants['false_easting']
    eprime_scaled = eprime/constants['central_scale_factor']
    nprime = northing - constants['false_northing']
    nprime_scaled = nprime/constants['central_scale_factor']

    # Calculate Foot-point latitude
    n = (a-b)/(a+b)
    n2 = math.pow(n, 2)
    n3 = math.pow(n, 3)
    n4 = math.pow(n, 4)
    g = a * (1-n) * (1-n2) * (1 + (9/4)*n2 + (225/64)*n4) * (math.pi/180)
    sigma = math.radians(nprime_scaled / g)
    fpl = sigma + ((3*n/2) - (27*n3/32))*math.sin(2*sigma) + ((21*n2/16) - (55*n4/32))*math.sin(4*sigma) + (151*n3/96)*math.sin(6*sigma) + (1097*n4/512)*math.sin(8*sigma)
    s = math.sin(fpl)
    s2 = math.pow(s, 2)
    sec = 1 / math.cos(fpl)
    t = math.tan(fpl)
    t2 = math.pow(t, 2)
    t4 = math.pow(t, 4)
    t6 = math.pow(t, 6)

    # calculate radius of curvature
    rho = a*(1-e2) / math.pow(1-e2*s2, 3/2)
    nu = a / math.sqrt(1-e2*s2)
    x = eprime_scaled / nu
    x3 = math.pow(x, 3)
    x5 = math.pow(x, 5)
    x7 = math.pow(x, 7)
    # radius of curvature
    psi = nu / rho
    psi2 = math.pow(psi, 2)
    psi3 = math.pow(psi, 3)
    psi4 = math.pow(psi, 4)

    # latitude
    latitude_term1 = -((t/(constants['central_scale_factor']*rho))*x*eprime/2)
    latitude_term2 = (t/(constants['central_scale_factor'] * rho)) * (x3 * eprime / 24) * (-4 * psi2 + 9 * psi * (1 - t2) + 12 * t2)
    latitude_term3 = -(t/(constants['central_scale_factor']*rho))*(x5*eprime/720)*(8*psi4*(11-24*t2)-12*psi3*(21-71*t2)+15*psi2*(15-98*t2+15*t4)+180*psi*(5*t2-3*t4)+360*t4)
    latitude_term4 = (t/(constants['central_scale_factor']*rho)) * (x7*eprime/40320) * (1385 + 3633*t2 + 4095*t4 + 1575*t6)
    latitude = math.degrees(fpl + latitude_term1 + latitude_term2 + latitude_term3 + latitude_term4)

    # longitude
    central_meridian_deg = (zone*constants['zone_width_degrees']) + constants['longitude_of_the_central_meridian_of_zone_1_degrees'] - constants['zone_width_degrees']
    central_meridian_rad = math.radians(central_meridian_deg)
    longitude_term1 = sec*x
    longitude_term2 = -sec*(x3/6) * (psi + 2*t2)
    longitude_term3 = sec*(x5/120) * (-4*psi3 * (1 - 6*t2) + psi2*(9 - 68*t2) + 72*psi*t2 + 24*t4)
    longitude_term4 = -sec*(x7/5040) * (61 + 662*t2 + 1320*t4 + 720*t6)
    longitude = math.degrees(central_meridian_rad + longitude_term1 + longitude_term2 + longitude_term3 + longitude_term4)

    # grid convergence
    gc_term1 = -x*t
    gc_term2 = (t*x3/3) * (-2*psi2 + 3*psi + t2)
    gc_term3 = -(t*x5/15) * (psi4*(11 - 24*t2) - 3*psi3*(8 - 23*t2) + 5*psi2*(3 - 14*t2) + 30*psi*t2 + 3*t4)
    gc_term4 = (t*x7/315) * (17 + 77*t2 + 105*t4 + 45*t6)
    grid_convergence = math.degrees(gc_term1 + gc_term2 + gc_term3 + gc_term4)

    # point scale factor
    pc_factor1 = pow(eprime_scaled, 2) / (rho*nu)
    pc_factor2 = pow(pc_factor1, 2)
    pc_factor3 = pow(pc_factor1, 3)
    pc_term1 = 1 + pc_factor1/2
    pc_term2 = (pc_factor2/24) * (4 * psi * (1 - 6*t2) - 3*(1 - 16*t2) - 24*t2/psi)
    pc_term3 = pc_factor3/720
    point_scale = constants['central_scale_factor'] * (pc_term1 + pc_term2 + pc_term3)

    return {
        'latitude': latitude,
        'longitude': longitude,
        'grid_convergence': grid_convergence,
        'point_scale_factor': point_scale
    }