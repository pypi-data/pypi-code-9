#!/usr/bin/env python

try:
    from urllib import request
except:
    import urllib2 as request

import json

from .choices import FUEL_TYPES

TOKEN = '6M5jaVAzPS'


def get(fuel_type, commune=None, dist=None):
    result = {}
    url = 'http://api.cne.cl/api/listaInformacion/%s' % TOKEN

    with request.urlopen(url) as response:
        encoding = response.headers['content-type'].split('charset=')[-1]
        res = json.loads(response.read().decode(encoding))

        if res.get('estado') != 'OK':
            return {}

        data = res.get('data')

        if commune:
            data = filter(
                lambda x: x['nombre_comuna'].lower() == commune, data)

        if dist:
            data = filter(
                lambda x: x['nombre_distribuidor'].lower() == dist, data)

        if fuel_type in FUEL_TYPES:
            data = list(filter(
                lambda x: fuel_type in x['precio_por_combustible'], data))

            if len(data) > 0:
                result = min(
                    data,
                    key=lambda x: x['precio_por_combustible'][fuel_type])

    return result
