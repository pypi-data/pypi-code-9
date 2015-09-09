# -*- coding: utf-8 -*-
from peltak.actions import actions
from peltak.config import MR_CACHE_PATH
from peltak.common.cache import CachedObj


@actions.register(
    'mr-reset',
    desc=("Reset local merge request cache. This will erase the local copy of "
          "the current merge request.")
)
def resetmr(app):
    mrcache = CachedObj.load_file(MR_CACHE_PATH)
    mrcache.reset()

