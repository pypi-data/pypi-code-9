from datetime import datetime

try:
    # python3
    from xmlrpc.client import DateTime
except ImportError:
    # python2
    from xmlrpclib import DateTime


def list(options):
    return [{'authinfo': 'abcdef0001',
             'autorenew': None,
             'zone_id': 424242,
             'tags': 'bla',
             'contacts': {'owner': {'handle': 'AA1-GANDI'},
                          'admin': {'handle': 'AA2-GANDI'},
                          'bill': {'handle': 'AA3-GANDI'},
                          'reseller': {'handle': 'AA4-GANDI'},
                          'tech': {'handle': 'AA5-GANDI'}},
             'date_created': datetime(2010, 9, 22, 15, 6, 18),
             'date_delete': datetime(2015, 10, 19, 19, 14, 0),
             'date_hold_begin': datetime(2015, 9, 22, 22, 0, 0),
             'date_registry_creation': datetime(2010, 9, 22, 13, 6, 16),
             'date_registry_end': datetime(2015, 9, 22, 0, 0, 0),
             'date_updated': datetime(2014, 9, 21, 3, 10, 7),
             'nameservers': ['a.dns.gandi.net', 'b.dns.gandi.net',
                             'c.dns.gandi.net'],
             'services': ['gandidns'],
             'fqdn': 'iheartcli.com',
             'id': 236816922,
             'status': [],
             'tld': 'com'},
            {'authinfo': 'abcdef0002',
             'autorenew': None,
             'contacts': {'admin': {'handle': 'PXP561-GANDI', 'id': 2920674},
                          'bill': {'handle': 'PXP561-GANDI', 'id': 2920674},
                          'owner': {'handle': 'PXP561-GANDI', 'id': 2920674},
                          'reseller': None,
                          'tech': {'handle': 'PXP561-GANDI', 'id': 2920674}},
             'date_created': DateTime('20130410T12:46:05'),
             'date_delete': DateTime('20160507T07:14:00'),
             'date_hold_begin': DateTime('20160410T00:00:00'),
             'date_registry_creation': DateTime('20140410T10:46:04'),
             'date_registry_end': DateTime('20140410T00:00:00'),
             'date_updated': DateTime('20150313T10:30:05'),
             'date_hold_end': DateTime('20151020T20:00:00'),
             'date_pending_delete_end': DateTime('20151119T00:00:00'),
             'date_renew_begin': DateTime('20120101T00:00:00'),
             'date_restore_end': DateTime('20151119T00:00:00'),
             'fqdn': 'cli.sexy',
             'id': 3412062241,
             'nameservers': ['a.dns.gandi.net', 'b.dns.gandi.net',
                             'c.dns.gandi.net'],
             'services': ['gandidns', 'gandimail', 'paas'],
             'status': [],
             'tags': [],
             'tld': 'sexy',
             'zone_id': 431190141}]


def info(id):
    domain = dict([(domain['fqdn'], domain) for domain in list({})])
    return domain[id]


def available(domains):

    ret = {}
    for domain in domains:
        if 'unavailable' in domain:
            ret[domain] = 'unavailable'
        elif 'pending' in domain:
            ret[domain] = 'pending'
        else:
            ret[domain] = 'available'

    return ret


def create(domain, params):
    return {'id': 400, 'step': 'WAIT'}


def renew(domain, params):
    return {'id': 400, 'step': 'WAIT'}
