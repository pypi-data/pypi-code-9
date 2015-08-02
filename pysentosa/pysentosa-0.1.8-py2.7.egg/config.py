#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import os
import yaml
import netifaces as ni

ni.ifaddresses('eth0')
LOCALIP = ni.ifaddresses('eth0')[2][0]['addr']

YMD=datetime.now().strftime("%Y-%m-%d")

CONFDIR='/singapore/config/' if os.name=='posix' else "c:\\singapore\\config\\"

yml_sentosa=yaml.load(open(CONFDIR+'sentosa.yml'))
yml_holiday=yaml.load(open(CONFDIR+'holiday.yml'))

_node = yml_sentosa['strategies']
if _node.has_key("singleta"):
    SYMBOLS=_node['singleta']
if _node.has_key("pairs"):
    [SYMBOLS.extend(s.split('|')[1:3]) for s in _node['pairs']]
SYMBOLS=list(set(SYMBOLS))

ACCOUNT = yml_sentosa['global']['account']
TRADEINFODIR = yml_sentosa['linux']['TRADEINFODIR'] + os.sep + ACCOUNT
