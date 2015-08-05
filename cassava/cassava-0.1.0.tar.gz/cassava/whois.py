#!/usr/bin/env python
# whois.py
"""
Active whois queries for domains and IPs
"""

import ipwhois
import pythonwhois
from utils import is_ip
from dbcache import dbcache

@dbcache
def domain_whois(domain):
    return pythonwhois.get_whois(domain)

@dbcache
def ip_whois(ip):
    try:
        return ipwhois.IPWhois(ip).lookup_rws()
    except:
        return {'error' : ' Error looking up whois info'}
    return whois

def whois(indicator):
    if is_ip(indicator):
        return ip_whois(indicator)
    else:
        return domain_whois(indicator)
