# -*- coding: utf-8 -*-
from igor.jsutil import json_dumps
from peltak.actions import actions
from peltak.common.cache import CachedObj
from peltak.config import MR_CACHE_PATH


@actions.register(
    'mr-get',
    desc="""
    Get remote merge request and save it in local cache. The description will
    probably have to be redone if you want to edit it using this app but at
    least the local cache will be connected to the selected repository. This
    is mostly useful after mr-reset  if you want to continue to work on a
    given merge request.
    """,
    cmdline=[{
        'args':     ('id',),
        'type':     int,
        'help':     "Merge request #ID"
    }]
)
def get_mr(app):
    mr = app.gitlab.get_mr(app.conf.project_id, app.cl.id)
    print(json_dumps(mr))

    mrcache = CachedObj.load_file(MR_CACHE_PATH)
    mrcache.reset()
    mrcache.remote_cache = mr
    #mrcache = CachedObj.load_file(MR_CACHE_PATH)
    #mrcache.remote_cache = mr
    #mr = extract_mr(mrcache)
    #mrcache.remote_cache = app.gitlab.create_mr(app.conf.project_id, mr)
    pass
