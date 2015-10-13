# Copyright (c) 2015, RedJack, LLC.
# All rights reserved.
#
# Please see the COPYING file in this distribution for license details.
from copy import deepcopy

import pytest


IP_RESP_PARSED = [
    # IPv4
    (
        '208.78.4.5',
        b'\x03\x00\x00\x00\x01C\x00\x00208.78.4.5domain=redjack.com\x00company=RedJack_LLC\x00country_code=US\x00region_code=MD\x00city=SILVERSPRING\x00dma=511\x00pmsa=8840\x00msa=8872\x00areacode=301\x00county=MONTGOMERY\x00fips=24031\x00lat=39.0245\x00long=-77.0094\x00timezone=EST\x00zip=20901-20908+20910-20911+20914-20916+20918+20993+20997\x00continent=NA\x00asnum=40287\x00throughput=vhigh\x00bw=5000\x00\x00',  # noqa
        {
            'default_answer': False,
            'domain': 'redjack.com',
            'company': 'RedJack_LLC',
            'country_code': 'US',
            'region_code': 'MD',
            'city': 'SILVERSPRING',
            'dma': 511,
            'pmsa': 8840,
            'msa': 8872,
            'areacode': [301],
            'county': ['MONTGOMERY'],
            'fips': ['24031'],
            'lat': 39.0245,
            'long': -77.0094,
            'timezone': 'EST',
            'zip': ['20901', '20902', '20903', '20904', '20905', '20906',
                    '20907', '20908', '20910', '20911', '20914', '20915',
                    '20916', '20918', '20993', '20997'],
            'continent': 'NA',
            'asnum': [40287],
            'throughput': 'vhigh',
            'bw': 5000,
        },
    ),
    # IPv6
    (
        '2001:4860:4801:5::89',
        b'\x03\x00\x00\x00\x01\x12\x00\x002001:4860:4801:5::89company=Google_Inc.\x00country_code=US\x00region_code=CA\x00city=MOUNTAINVIEW\x00dma=807\x00pmsa=7400\x00msa=7362\x00areacode=650\x00county=SANTACLARA\x00fips=06085\x00lat=37.4154\x00long=-122.0585\x00timezone=PST\x00zip=94035+94039-94043\x00continent=NA\x00asnum=15169\x00throughput=low\x00bw=1\x00\x00',  # noqa
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
    ),
    # Zip codes with leading zeroes
    (
        '192.250.175.25',
        b'\x03\x00\x00\x00\x01#\x00\x00192.250.175.25company=State_Street_Bank_and_Trust_Company\x00country_code=US\x00region_code=MA\x00city=CAMBRIDGE\x00dma=506\x00pmsa=1120\x00msa=1122\x00areacode=617\x00county=MIDDLESEX\x00fips=25017\x00lat=42.3802\x00long=-71.1347\x00timezone=EST\x00zip=02138-02142+02238\x00continent=NA\x00asnum=3738\x00throughput=vhigh\x00bw=5000\x00\x00',  # noqa
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
    ),
    # Puerto Rico IP
    (
        '66.50.137.144',
        b'\x03\x00\x00\x00\x01\x2f\x00\x0066.50.137.144domain=coqui.net\x00company=Datacom_Caribe_Inc.\x00country_code=PR\x00city=SANJUAN\x00pmsa=7440\x00msa=7442\x00areacode=787\x00county=SANJUAN\x00fips=72127\x00lat=18.4697\x00long=-66.1179\x00timezone=EST+1\x00zip=00901-00902+00933+00935-00937+00939-00940+00955+00975\x00continent=NA\x00asnum=10396\x00throughput=vhigh\x00bw=5000\x00\x00',  # noqa,
        {
            'default_answer': False,
            'domain': 'coqui.net',
            'company': 'Datacom_Caribe_Inc.',
            'country_code': 'PR',
            'city': 'SANJUAN',
            'pmsa': 7440,
            'msa': 7442,
            'areacode': [787],
            'county': ['SANJUAN'],
            'fips': ['72127'],
            'lat': 18.4697,
            'long': -66.1179,
            'timezone': 'EST+1',
            'zip': ['00901', '00902', '00933', '00935', '00936', '00937',
                    '00939', '00940', '00955', '00975'],
            'continent': 'NA',
            'asnum': [10396],
            'throughput': 'vhigh',
            'bw': 5000,
        },
    ),
    # Canadian zip codes
    (
        '192.206.151.131',
        b'\x03\x00\x00\x00\x01\x9a\x00\x00192.206.151.131company=Toronto_Star\x00country_code=CA\x00region_code=ON\x00city=TORONTO\x00lat=43.67\x00long=-79.42\x00timezone=EST\x00zip=M3H+M3M+M4B+M4C+M4E+M4G+M4H+M4J+M4K+M4L+M4M+M4N+M4P+M4R+M4S+M4T+M4V+M4W+M4X+M4Y+M5A+M5B+M5C+M5E+M5G+M5H+M5J+M5K+M5L+M5M+M5N+M5P+M5R+M5S+M5T+M5V+M5W+M5X+M6A+M6B+M6C+M6E+M6G+M6H+M6J+M6K+M6L+M6M+M6N+M6P+M6R+M6S+M7A+M7Y+M9M+M9N+M9P+M9W\x00continent=NA\x00asnum=10400\x00throughput=vhigh\x00bw=5000\x00\x00',  # noqa
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
    ),
    # Reserved non-canonical address
    (
        '10.0.0.001',
        b'\x03\x00\x00\x00\x01\x83\x00\x0010.0.0.001domain=reserved\x00company=Internet_Assigned_Numbers_Authority\x00country_code=reserved\x00region_code=reserved\x00city=reserved\x00dma=reserved\x00pmsa=reserved\x00msa=reserved\x00areacode=reserved\x00county=reserved\x00fips=reserved\x00lat=reserved\x00long=reserved\x00timezone=reserved\x00zip=reserved\x00continent=reserved\x00network=reserved\x00network_type=reserved\x00asnum=reserved\x00throughput=reserved\x00bw=reserved\x00\x00',  # noqa
        {
            'default_answer': False,
            'domain': 'reserved',
            'company': 'Internet_Assigned_Numbers_Authority',
            'country_code': 'reserved',
            'region_code': 'reserved',
            'city': 'reserved',
            'dma': 'reserved',
            'pmsa': 'reserved',
            'msa': 'reserved',
            'areacode': ['reserved'],
            'county': ['reserved'],
            'fips': ['reserved'],
            'lat': 'reserved',
            'long': 'reserved',
            'timezone': 'reserved',
            'zip': ['reserved'],
            'continent': 'reserved',
            'network': 'reserved',
            'network_type': 'reserved',
            'asnum': ['reserved'],
            'throughput': 'reserved',
            'bw': 'reserved',
        },
    ),
    # Non-US
    (
        '91.211.73.234',
        b'\x03\x00\x00\x00\x00\xb6\x00\x0091.211.73.234domain=gumtree.com\x00company=Marktplaats_B.V.\x00country_code=NL\x00city=AMSTERDAM\x00lat=52.35\x00long=4.92\x00timezone=GMT+1\x00continent=EU\x00asnum=41552\x00throughput=vhigh\x00bw=2000\x00\x00',  # noqa
        {
            'default_answer': False,
            'domain': 'gumtree.com',
            'company': 'Marktplaats_B.V.',
            'country_code': 'NL',
            'city': 'AMSTERDAM',
            'lat': 52.35,
            'long': 4.92,
            'timezone': 'GMT+1',
            'continent': 'EU',
            'asnum': [41552],
            'throughput': 'vhigh',
            'bw': 2000,
        },
    ),
    (
        # Default response from server, which has a status code of OK, not DEFAULT >_<
        '1.1.1.1',
        b'\x03\x00\x00\x00\x00\x3c\x00\x001.1.1.1default_answer=T\x00default_source=facilitator\x00\x00',  # noqa
        {
            'default_answer': True,
            'default_source': 'facilitator',
        },
    )
]


class TestIPLookup(object):

    @pytest.mark.parametrize('ip,resp,parsed_data', deepcopy(IP_RESP_PARSED) + [
        # Default response
        (
            '123.123.123.123',
            b'\x03\x00\x00\x00\x00\x17\x01\x00123.123.123.123',
            {'default_answer': True, 'default_source': 'client'}
        ),
    ])
    def test_ip_lookup(self, edgescape_server, ip, resp, parsed_data):
        from akadata import EdgeScape

        # ip_lookup() adds the ip address to the parsed data
        parsed_data['ip'] = ip

        edgescape_server.responses.append(resp)

        es = EdgeScape(*edgescape_server.server_address)

        result = es.ip_lookup(ip)

        assert result == parsed_data

    def test_ip_lookup_timeout(self):
        from contextlib import closing
        import socket
        from akadata import EdgeScape

        with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as sock:
            sock.bind(('localhost', 0))
            host, port = sock.getsockname()

            es = EdgeScape(host, port)

            with pytest.raises(socket.timeout):
                es.ip_lookup('192.168.1.1', timeout=0.1)

    @pytest.mark.parametrize('ip', [
        '999.999.999.999',
        'not-an-ip',
    ])
    def test_ip_lookup_invalid_ip(self, ip):
        from akadata import EdgeScape

        es = EdgeScape()

        with pytest.raises(ValueError):
            es.ip_lookup(ip)


# All packed IPs are generated by the Akamai-provided PHP client.
@pytest.mark.parametrize('ip,packed', [
    (
        '208.78.4.5',
        b'\x03\x00\x00\x00\x04\x00\x00\x00208.78.4.5'
    ),
    (
        '2001:4860:4801:5::89',
        b'\x03\x00\x00\x00\x04\x00\x00\x002001:4860:4801:5::89'
    ),
    (
        '2001:4860:4801:5:0:0:0:89',
        b'\x03\x00\x00\x00\x04\x00\x00\x002001:4860:4801:5:0:0:0:89'
    ),
    (
        '192.168.1.1',
        b'\x03\x00\x00\x00\x04\x00\x00\x00192.168.1.1'
    ),
    (
        '8.8.8.8',
        b'\x03\x00\x00\x00\x04\x00\x00\x008.8.8.8'
    ),
    (
        '216.164.57.14',
        b'\x03\x00\x00\x00\x04\x00\x00\x00216.164.57.14'
    ),
    (
        'not-an-ip',
        b'\x03\x00\x00\x00\x04\x00\x00\x00not-an-ip'
    ),
    (
        '1.2.3.4.5',
        b'\x03\x00\x00\x00\x04\x00\x00\x001.2.3.4.5'
    ),
    (
        '999.999.999.999',
        b'\x03\x00\x00\x00\x04\x00\x00\x00999.999.999.999'
    ),
    (
        '255.255.255.0',
        b'\x03\x00\x00\x00\x04\x00\x00\x00255.255.255.0'
    ),
])
def test__pack_ip(ip, packed):
    from akadata import _pack_ip

    assert _pack_ip(ip) == packed


# Responses are generated by the Akamai-provided Perl client and edited as
# needed to raise error conditions.
@pytest.mark.parametrize('ip,resp,expected_result,status_code,exc_class,exc_kwargs', [
    # Valid IPv4 response
    (
        '208.78.4.5',
        b'\x03\x00\x00\x00\x01C\x00\x00208.78.4.5domain=redjack.com\x00company=RedJack_LLC\x00country_code=US\x00region_code=MD\x00city=SILVERSPRING\x00dma=511\x00pmsa=8840\x00msa=8872\x00areacode=301\x00county=MONTGOMERY\x00fips=24031\x00lat=39.0245\x00long=-77.0094\x00timezone=EST\x00zip=20901-20908+20910-20911+20914-20916+20918+20993+20997\x00continent=NA\x00asnum=40287\x00throughput=vhigh\x00bw=5000\x00\x00',  # noqa
        'domain=redjack.com\x00company=RedJack_LLC\x00country_code=US\x00region_code=MD\x00city=SILVERSPRING\x00dma=511\x00pmsa=8840\x00msa=8872\x00areacode=301\x00county=MONTGOMERY\x00fips=24031\x00lat=39.0245\x00long=-77.0094\x00timezone=EST\x00zip=20901-20908+20910-20911+20914-20916+20918+20993+20997\x00continent=NA\x00asnum=40287\x00throughput=vhigh\x00bw=5000\x00\x00',  # noqa
        0,
        None,
        None
    ),
    # Valid IPv6 response
    (
        '2001:4860:4801:5::89',
        b'\x03\x00\x00\x00\x01\x12\x00\x002001:4860:4801:5::89company=Google_Inc.\x00country_code=US\x00region_code=CA\x00city=MOUNTAINVIEW\x00dma=807\x00pmsa=7400\x00msa=7362\x00areacode=650\x00county=SANTACLARA\x00fips=06085\x00lat=37.4154\x00long=-122.0585\x00timezone=PST\x00zip=94035+94039-94043\x00continent=NA\x00asnum=15169\x00throughput=low\x00bw=1\x00\x00',  # noqa
        'company=Google_Inc.\x00country_code=US\x00region_code=CA\x00city=MOUNTAINVIEW\x00dma=807\x00pmsa=7400\x00msa=7362\x00areacode=650\x00county=SANTACLARA\x00fips=06085\x00lat=37.4154\x00long=-122.0585\x00timezone=PST\x00zip=94035+94039-94043\x00continent=NA\x00asnum=15169\x00throughput=low\x00bw=1\x00\x00',  # noqa
        0,
        None,
        None
    ),
    # AKAMAI_DEFAULT status code
    (
        '123.123.123.123',
        b'\x03\x00\x00\x00\x00\x17\x01\x00123.123.123.123',
        '',
        1,
        None,
        None,
    ),
    # Invalid version
    (
        '123.123.123.123',
        b'\x02\x00\x00\x00\x00\x17\x00\x00123.123.123.123',
        None,
        None,
        'InvalidVersion',
        {'query_version': 3, 'result_version': 2, 'status_code': 0}
    ),
    # Invalid flags
    (
        '123.123.123.123',
        b'\x03\x06\x00\x00\x00\x17\x00\x00123.123.123.123',
        None,
        None,
        'EdgeScapeException',
        {'status_code': 0}
    ),
    # Invalid size
    (
        '123.123.123.123',
        b'\x03\x00\x00\x00\x00\x12\x00\x00123.123.123.123',
        None,
        None,
        'EdgeScapeException',
        {'status_code': 0}
    ),
    # Wrong address
    (
        '123.123.123.123',
        b'\x03\x00\x00\x00\x00\x17\x00\x00100.100.100.100',
        None,
        None,
        'InvalidAddress',
        {'query_address': '123.123.123.123', 'result_address': '100.100.100.100',
         'status_code': 0}
    ),
    # Non-success status code
    (
        '123.123.123.123',
        b'\x03\x00\x00\x00\x00\x17\x04\x00123.123.123.123',
        None,
        None,
        'EdgeScapeException',
        {'status_code': 4}
    ),
])
def test__validate_result(ip, resp, expected_result, status_code, exc_class, exc_kwargs):
    from importlib import import_module
    from akadata import _validate_result

    if expected_result is not None:
        assert _validate_result(resp, ip) == (expected_result, status_code)
    elif exc_class is not None:
        exceptions = import_module('akadata.exceptions')
        exc_class = getattr(exceptions, exc_class)

        with pytest.raises(exc_class) as excinfo:
            _validate_result(resp, ip)

        for attr, val in exc_kwargs.items():
            assert getattr(excinfo.value, attr) == val
    else:
        assert False, "No 'result' or 'exc_class' in the test!"


@pytest.mark.parametrize('ip,resp,parsed_data', deepcopy(IP_RESP_PARSED))
def test__edgescape_result_to_dict(ip, resp, parsed_data):
    from akadata import _edgescape_result_to_dict

    # _edgescape_result_to_dict expects a string (not bytes) with the
    # response header and IP address stripped.
    resp = resp.decode('utf-8', errors='ignore').split(ip, 1)[-1]

    assert _edgescape_result_to_dict(resp) == parsed_data
