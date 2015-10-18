#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry

# REDIS_SERVER="210.45.66.91"
# REDIS_PORT=6379
# MONGO_SERVER="210.45.66.91"
# MONGO_PORT=27017

import yaml

def check_config(filename):

    CONFIG=yaml.load(open(filename,'r'))

    for keyword in CONFIG:
        globals()[keyword]=CONFIG[keyword]

# check_config()



