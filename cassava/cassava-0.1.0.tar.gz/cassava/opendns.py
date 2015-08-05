#!/usr/bin/env python
# investigate.py
"""
Interface for the OpenDNS Investigate API. Allows bulk
lookups of domains and IPs.
"""


import config
import investigate
from dbcache import dbcache

@dbcache
def get_categorization(domain):
    '''Get the domain status and categorization of a domain or list of
        domains.'''
    inv = investigate.Investigate(config.OPENDNS_APIKEY)
    results = inv.categorization(domain, labels=True)[domain]
    if 'status' in results and results['status'] == 1:
        del results['status']
    else:
        results = results
    return results

@dbcache
def get_cooccurrences(domain):
    '''Get the cooccurrences of the given domain.'''
    inv = investigate.Investigate(config.OPENDNS_APIKEY)
    results = inv.cooccurrences(domain)
    if 'found' in results and results['found'] is True and 'pfs2' in results:
            results = [r[0] for r in results['pfs2']]
    else:
        results = {}
    return results

@dbcache
def get_related_domains(domain):
    '''Get the related domains of the given domain.'''
    inv = investigate.Investigate(config.OPENDNS_APIKEY)
    results = inv.related(domain)
    if 'found' in results and results['found'] is True and 'tb1' in results:
        results = [r[0] for r in results['tb1']]
    else:
        results = {}
    return results

@dbcache
def get_security_info(domain):
    '''Get the Security Information for the given domain.'''
    inv = investigate.Investigate(config.OPENDNS_APIKEY)
    results = inv.security(domain)
    if 'found' in results and results['found'] is True:
        del results['found']
        results = results
    else:
        results = results
    return results

@dbcache
def get_latest_malicious_domains(ip):
    '''Gets the latest known malicious domains associated with the given
        IP address, if any. Returns the list of malicious domains.
    '''
    inv = investigate.Investigate(config.OPENDNS_APIKEY)
    results = inv.latest_domains(ip)
    return results

@dbcache
def rr_history_ip(ip, query_type):
    inv = investigate.Investigate(config.OPENDNS_APIKEY)
    results = inv.rr_history(ip, query_type=query_type)['rrs']
    names = []
    ips = []
    for r in results:
        names.append(r['rr'])
        #ips.append(r['name'])
    return list(set(names+ips))

@dbcache
def rr_history_domain(domain, query_type):
    inv = investigate.Investigate(config.OPENDNS_APIKEY)
    results = inv.rr_history(domain, query_type=query_type)['rrs_tf']
    rrs = [r['rrs'] for r in results]
    rr_ips = []
    for entry in rrs:
        for rr in entry:
            rr_ips.append(rr['rr'])
    return list(set(rr_ips))

@dbcache
def domain_whois(domains):
    '''Gets whois information for a domain'''
    inv = investigate.Investigate(config.OPENDNS_APIKEY)
    if isinstance(domains, list):
        return [inv.domain_whois(d) for d in domains]
    else:
        return inv.domain_whois(domains)

@dbcache
def ns_whois(nameservers):
    '''Gets the domains that have been registered with a nameserver or
    nameservers'''
    inv = investigate.Investigate(config.OPENDNS_APIKEY)
    return inv.ns_whois(nameservers)

@dbcache
def email_whois(emails):
    '''Gets the domains that have been registered with a given email
    address'''
    inv = investigate.Investigate(config.OPENDNS_APIKEY)
    return inv.email_whois(emails)
