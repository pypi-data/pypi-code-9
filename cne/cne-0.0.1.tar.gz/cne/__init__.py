#!/usr/bin/env python

import requests
from pydash import find, filter_

TOKEN = '6M5jaVAzPS'
FUEL_TYPES = (
    'gasolina_93',
    'gasolina_95',
    'gasolina_97',
    'petroleo_diesel',
    'kerosene',
)


def get(commune=None, distributor=None, fuel_type=None):
    r = requests.get('http://api.cne.cl/api/listaInformacion/%s' % TOKEN)
    res = r.json()

    if res.get('estado') != 'OK':
        return []

    data = res.get('data')
    result = None

    if commune is None and distributor is None:
        data = [find(data, {'id': 'co01001'})]

    else:
        if commune:
            data = filter_(data, {'nombre_comuna': commune})

        if distributor:
            data = filter_(data, {'nombre_distribuidor': distributor})

    if len(data) > 0:
        data = data[0]

        if fuel_type in FUEL_TYPES:
            result = data.get('precio_por_combustible').get(fuel_type)

        else:
            result = data.get('precio_por_combustible')

    return result
