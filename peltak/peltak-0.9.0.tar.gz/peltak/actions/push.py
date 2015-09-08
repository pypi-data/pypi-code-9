# -*- coding: utf-8 -*-
from peltak.actions import actions
from peltak.core import git, cstr
from peltak.config import MR_CACHE_PATH
from peltak.system import forms
from peltak.common.cache import CachedObj
from peltak.common.utils import resetmr_if_closed


@actions.register(
    'push',
    desc=('Push the current branch to origin. This will go throught the '
          'checklist if it exists in the template. Each question only has '
          'to be answered once. That answer is cached and for the moment '
          'cannot be changed (Feature planned for the future).')
)
def action_push(app):
    resetmr_if_closed(app)
    mrcache = CachedObj.load_file(MR_CACHE_PATH)

    forms.mr_description(mrcache,
                         skip_context=True,
                         force_update=[])

    try:
        print(cstr("Pushing ^33{}^0 to ^34{}^0 ^1(^^C to skip)^0".format(
            git.current_branch(), app.conf.gitlab_url
        )))
        if git.push_current() == 0:
            mrcache.branch_exists = True
    except KeyboardInterrupt:
        pass

