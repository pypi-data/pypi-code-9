# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

from bson.json_util import dumps as bson_dumps, object_hook as bson_object_hook
from json import loads as json_loads
from bson import SON

#Need to hack json_util to preserve order of object fields
def loads(*args, **kwargs):
    kwargs['object_pairs_hook'] = lambda x: bson_object_hook(SON(x))
    return json_loads(*args, **kwargs)
  
def dumps(*args, **kwargs):
    return bson_dumps(*args, **kwargs)
  