#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Safecast Tracker commands."""

__author__ = 'Greg Albrecht W2GMD <gba@orionlabs.co>'
__copyright__ = 'Copyright 2015 Orion Labs, Inc.'
__license__ = 'All rights reserved. Do not redistribute.'


import argparse
import logging
import logging.handlers
import time

import aprs
import aprs.util

import safecast_tracker
import safecast_tracker.constants


def setup_logging(log_level=None):
    """
    Sets up logging.

    :param log_level: Log level to setup.
    :type param: `logger` level.
    :returns: logger instance
    :rtype: instance
    """
    log_level = log_level or safecast_tracker.constants.LOG_LEVEL

    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(safecast_tracker.constants.LOG_FORMAT)
    logger.addHandler(console_handler)
    logger.propagate = False

    return logger


def sc_tracker():
    """Safecast Tracker Command Line interface for APRS."""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--debug', help='Enable debug logging', action='store_true'
    )
    parser.add_argument(
        '-c', '--callsign', help='callsign', required=True
    )
    parser.add_argument(
        '-p', '--passcode', help='passcode', required=True
    )
    parser.add_argument(
        '-m', '--mac_address', help='mac_address', required=True
    )
    parser.add_argument(
        '-i', '--interval', help='interval', default=0
    )
    parser.add_argument(
        '-u', '--ssid', help='ssid', default='1'
    )

    opts = parser.parse_args()

    if opts.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logger = setup_logging(log_level)

    sc_p = safecast_tracker.BGeigieNanoPoller(opts.mac_address)
    sc_p.start()

    time.sleep(aprs.constants.GPS_WARM_UP)

    aprs_i = aprs.APRS(opts.callsign, opts.passcode)
    aprs_i.connect()

    src_callsign = aprs.util.full_callsign(
        {'callsign': opts.callsign, 'ssid': opts.ssid})

    try:
        while 1:
            gps_valid = sc_p.bgn_props['gps_valid'] == 'A'
            rad_valid = sc_p.bgn_props['rad_valid'] == 'A'

            if gps_valid and rad_valid:
                aprs_latitude = None
                aprs_longitude = None

                gps_latitude = sc_p.bgn_props['latitude']
                gps_hemisphere = sc_p.bgn_props['hemisphere']
                gps_longitude = sc_p.bgn_props['longitude']
                gps_ew = sc_p.bgn_props['east_west']

                if gps_latitude is not None and gps_hemisphere is not None:
                    aprs_latitude = "%04.02f%s" % (
                        gps_latitude, gps_hemisphere)
                if gps_longitude is not None and gps_ew is not None:
                    aprs_longitude = "%04.02f%s" % (gps_longitude, gps_ew)

                if aprs_latitude is not None and aprs_longitude is not None:
                    frame = aprs.util.create_location_frame(
                        source=src_callsign,
                        destination='APRS',
                        latitude=aprs_latitude,
                        longitude=aprs_longitude,
                        course=0,
                        speed=0,
                        altitude=sc_p.bgn_props.get('altitude', 0),
                        symboltable='\\',
                        symbolcode='c',
                        comment="Safecast did=%s rtc=%s cp5s=%s cpm=%s" % (
                            sc_p.bgn_props['device_id'],
                            sc_p.bgn_props['rad_total_count'],
                            sc_p.bgn_props['rad_5_secs'],
                            sc_p.bgn_props['rad_1_min']
                        )
                    )

                    logger.info('frame=%s', frame)
                    aprs_i.send(frame)

                    if opts.interval == 0:
                        break
                    else:
                        time.sleep(float(opts.interval))

    except KeyboardInterrupt:
        sc_p.stop()
    finally:
        sc_p.stop()
