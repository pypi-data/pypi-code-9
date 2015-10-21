 # -*- coding: utf-8 -*-
from __future__ import unicode_literals
from flask.ext.redis import Redis
from glb.core.db import DB

redis = Redis()
db = DB(redis)
