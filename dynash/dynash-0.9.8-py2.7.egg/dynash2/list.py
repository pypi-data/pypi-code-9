#!/usr/bin/env python

from __future__ import print_function

import boto.dynamodb2
from boto.dynamodb2.table import Table

import sys
import time

def set_environment(env):
    found = False
    for section in ['Credentials', 'DynamoDB']:
        env_section = "%s.%s" % (env, section)

        if boto.config.has_section(env_section):
            found = True
            if not boto.config.has_section(section):
                boto.config.add_section(section)
            for o in boto.config.options(env_section):
                boto.config.set(section, o, boto.config.get(env_section, o))
    return found


if not set_environment("p"):
    print("cannot set environment", file=sys.stderr)
    sys.exit(1)

item_table = Table("prod-skybox-items_by_object_id")
count = 0

def read_batch(id_list):
    start_time = time.time()
    for i in item_table.batch_get(keys=id_list):
        user, _ = i["_id"].split(":")
        rid = i["id"]
        print("%s:%s" % (user, rid))
    delta = time.time() - start_time
    if delta < 1:
        time.sleep(1)

    global count
    count += len(id_list)
    print("processed %d" % count, file=sys.stderr)

with open("userlist", "r") as f:
    id_list = []

    for u in f.xreadlines():
        id_list.append({"_id": "%s@AdobeID:SKYBOX" % u.strip()})

        if len(id_list) == 100:
            read_batch(id_list)
            del id_list[:]

if id_list:
    read_batch(id_list)
