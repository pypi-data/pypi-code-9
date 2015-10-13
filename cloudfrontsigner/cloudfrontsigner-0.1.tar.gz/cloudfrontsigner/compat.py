# -*- coding: utf-8 -*-

try:
    from urllib.parse import parse_qs, urlencode, urlparse
except ImportError:
    from urllib import parse_qs, urlencode, urlparse
