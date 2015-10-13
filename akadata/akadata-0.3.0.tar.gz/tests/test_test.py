# Copyright (c) 2015, RedJack, LLC.
# All rights reserved.
#
# Please see the COPYING file in this distribution for license details.
import pytest


@pytest.fixture
def client(edgescape_server):
    from akadata import EdgeScape

    return EdgeScape(edgescape_server.host, edgescape_server.port)


@pytest.mark.parametrize('ip,data,expected_bytes', [
    # IPv4
    (
        '192.250.175.25',
        {
            'default_answer': False,
            'company': 'State_Street_Bank_and_Trust_Company',
            'country_code': 'US',
            'region_code': 'MA',
            'city': 'CAMBRIDGE',
            'dma': 506,
            'pmsa': 1120,
            'msa': 1122,
            'areacode': [617],
            'county': ['MIDDLESEX'],
            'fips': ['25017'],
            'lat': 42.3802,
            'long': -71.1347,
            'timezone': 'EST',
            'zip': ['02138', '02139', '02140', '02141', '02142', '02238'],
            'continent': 'NA',
            'asnum': [3738],
            'throughput': 'vhigh',
            'bw': 5000,
        },
        b'\x03\x00\x00\x00\x015\x00\x00192.250.175.25areacode=617\x00asnum=3738\x00bw=5000\x00city=CAMBRIDGE\x00company=State_Street_Bank_and_Trust_Company\x00continent=NA\x00country_code=US\x00county=MIDDLESEX\x00dma=506\x00fips=25017\x00lat=42.3802\x00long=-71.1347\x00msa=1122\x00pmsa=1120\x00region_code=MA\x00throughput=vhigh\x00timezone=EST\x00zip=02138+02139+02140+02141+02142+02238\x00\x00',  # noqa
    ),
    # IPv6
    (
        '2001:4860:4801:5::89',
        {
            'default_answer': False,
            'company': 'Google_Inc.',
            'country_code': 'US',
            'region_code': 'CA',
            'city': 'MOUNTAINVIEW',
            'dma': 807,
            'pmsa': 7400,
            'msa': 7362,
            'areacode': [650],
            'county': ['SANTACLARA'],
            'fips': ['06085'],
            'lat': 37.4154,
            'long': -122.0585,
            'timezone': 'PST',
            'zip': ['94035', '94039', '94040', '94041', '94042', '94043'],
            'continent': 'NA',
            'asnum': [15169],
            'throughput': 'low',
            'bw': 1,
        },
        b'\x03\x00\x00\x00\x01$\x00\x002001:4860:4801:5::89areacode=650\x00asnum=15169\x00bw=1\x00city=MOUNTAINVIEW\x00company=Google_Inc.\x00continent=NA\x00country_code=US\x00county=SANTACLARA\x00dma=807\x00fips=06085\x00lat=37.4154\x00long=-122.0585\x00msa=7362\x00pmsa=7400\x00region_code=CA\x00throughput=low\x00timezone=PST\x00zip=94035+94039+94040+94041+94042+94043\x00\x00'  # noqa
    ),
    # Canadian Zip Codes
    (
        '192.206.151.131',
        {
            'default_answer': False,
            'company': 'Toronto_Star',
            'country_code': 'CA',
            'region_code': 'ON',
            'city': 'TORONTO',
            'lat': 43.67,
            'long': -79.42,
            'timezone': 'EST',
            'zip': ['M3H', 'M3M', 'M4B', 'M4C', 'M4E', 'M4G', 'M4H', 'M4J',
                    'M4K', 'M4L', 'M4M', 'M4N', 'M4P', 'M4R', 'M4S', 'M4T',
                    'M4V', 'M4W', 'M4X', 'M4Y', 'M5A', 'M5B', 'M5C', 'M5E',
                    'M5G', 'M5H', 'M5J', 'M5K', 'M5L', 'M5M', 'M5N', 'M5P',
                    'M5R', 'M5S', 'M5T', 'M5V', 'M5W', 'M5X', 'M6A', 'M6B',
                    'M6C', 'M6E', 'M6G', 'M6H', 'M6J', 'M6K', 'M6L', 'M6M',
                    'M6N', 'M6P', 'M6R', 'M6S', 'M7A', 'M7Y', 'M9M', 'M9N',
                    'M9P', 'M9W'],
            'continent': 'NA',
            'asnum': [10400],
            'throughput': 'vhigh',
            'bw': 5000,
        },
        b'\x03\x00\x00\x00\x01\x9a\x00\x00192.206.151.131asnum=10400\x00bw=5000\x00city=TORONTO\x00company=Toronto_Star\x00continent=NA\x00country_code=CA\x00lat=43.67\x00long=-79.42\x00region_code=ON\x00throughput=vhigh\x00timezone=EST\x00zip=M3H+M3M+M4B+M4C+M4E+M4G+M4H+M4J+M4K+M4L+M4M+M4N+M4P+M4R+M4S+M4T+M4V+M4W+M4X+M4Y+M5A+M5B+M5C+M5E+M5G+M5H+M5J+M5K+M5L+M5M+M5N+M5P+M5R+M5S+M5T+M5V+M5W+M5X+M6A+M6B+M6C+M6E+M6G+M6H+M6J+M6K+M6L+M6M+M6N+M6P+M6R+M6S+M7A+M7Y+M9M+M9N+M9P+M9W\x00\x00'  # noqa
    ),
    # No IP in 'data'
    (
        '8.8.8.8',
        {
            'just': 'some',
            'data': 'data',
            'without': 'ip_address',
            'default_answer': False,
        },
        b'\x03\x00\x00\x00\x007\x00\x008.8.8.8data=data\x00just=some\x00without=ip_address\x00\x00'  # noqa
    ),
    # No 'default_answer' in data
    (
        '8.8.8.8',
        {
            'ip': '8.8.8.8',
            'just': 'some',
            'data': 'data',
            'without': 'default_answer',
        },
        b'\x03\x00\x00\x00\x00;\x00\x008.8.8.8data=data\x00just=some\x00without=default_answer\x00\x00'  # noqa
    ),
    # 'default_answer == True'
    (
        '1.1.1.1',
        {
            'default_answer': True,
            'default_source': 'facilitator',
        },
        b'\x03\x00\x00\x00\x00\x3c\x00\x001.1.1.1default_answer=T\x00default_source=facilitator\x00\x00'  # noqa
    ),
])
def test_format_edgescape_response(ip, data, expected_bytes, edgescape_server,
                                   client):
    from akadata.test import format_edgescape_response

    formatted = format_edgescape_response(ip, data)
    assert formatted == expected_bytes

    edgescape_server.responses.append(formatted)

    # We should get the same results from parsing the formatted bytes
    lookup_from_formatted = client.ip_lookup(ip)

    # Remove optional keys from `data` and `lookup_from_formatted` to make
    # comparison easier.
    for d in (data, lookup_from_formatted):
        d.pop('ip', None)

        if d.get('default_answer') is False:
            del d['default_answer']

    assert data == lookup_from_formatted
