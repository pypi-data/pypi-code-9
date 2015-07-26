# -*- coding: UTF-8 -*-
import logging

try:
    import requests
except ImportError:
    pass
import json
import StringIO
import csv

__author__ = 'johan'


def get_data(url):
    r = requests.get(url)
    return r.content


def fetch_sites(sl_site_data_url):
    json_response = json.loads(get_data(sl_site_data_url))
    sites = json_response['ResponseData']['Result']
    site_id_to_stop_area = dict()
    for s in sites:
        site_id = s['SiteId']
        if site_id not in site_id_to_stop_area:
            site_id_to_stop_area[site_id] = list()
        site_id_to_stop_area[site_id].append(s['StopAreaNumber'])
    return site_id_to_stop_area


def fetch_agency_stops(sl_gtfs_agency_stop_url):
    f = StringIO.StringIO(get_data(sl_gtfs_agency_stop_url))
    reader = csv.DictReader(f, delimiter=',')
    agency_stop_id_to_stop_id = dict()
    for row in reader:
        agency_stop_id = row['agency_stop_id']
        if agency_stop_id not in agency_stop_id_to_stop_id:
            agency_stop_id_to_stop_id[agency_stop_id] = list()
        agency_stop_id_to_stop_id[agency_stop_id].append(row['stop_id'])
    return agency_stop_id_to_stop_id


def make_mapping(sl_site_data_url, sl_gtfs_agency_stop_url):
    """ Creates a mapping for site id to gtfs stop id.

    Returns a list of tuples of site_id, stop_id.
    """
    site_id_to_stop_area = fetch_sites(sl_site_data_url)
    agency_stop_id_to_stop_id = fetch_agency_stops(sl_gtfs_agency_stop_url)
    site_id_to_gtfs_id = []  # A list with a tuple of site_id, stop_id
    for site_id in site_id_to_stop_area:
        for stop_area in site_id_to_stop_area[site_id]:
            if stop_area not in agency_stop_id_to_stop_id:
                logging.debug('%s is missing in gtfs source' % stop_area)
                continue
            for gtfs_id in agency_stop_id_to_stop_id[stop_area]:
                site_id_to_gtfs_id.append((site_id, gtfs_id))

    return site_id_to_gtfs_id
