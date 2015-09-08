# -*- coding: utf-8 -*-
import logging
from six import PY2, PY3
from peltak.actions import actions
from peltak.core import git, cstr, CommaSeparatedList
from peltak.common import prompt
from peltak.common.utils import extract_mr, mrdiff, resetmr_if_closed
from peltak.common.cache import CachedObj
from peltak.config import MR_CACHE_PATH
from peltak.system import forms
if PY2:
    from urlparse import urljoin
elif PY3:
    from urllib.parse import urljoin


@actions.register(
    'mr',
    desc=("Manage a Gitlab merge request. This will ask you all the details "
          "about the MR. The details can be "),

    cmdline=[{
        'args':     ('--ready',),
        'dest':     'ready',
        'action':   'store_true',
        'help': ("Mark merge request as ready. "
                 "This will remove [WIP] tag from the title")
    }, {
        'args':     ('-u', '--update'),
        'dest':     'force_update',
        'type':     CommaSeparatedList,
        'default':  [],
        'help': ("Comma separated list of fields to update in the description")
    }, {
        'args':     ('--skip-context',),
        'dest':     'skip_context',
        'action':   'store_true',
        'help': ("Skip filling template context")
    }]
)
def action_mr(app):
    if resetmr_if_closed(app):
        print("Resetting cache, merge reqeust {} has been merged".format)

    mrcache = CachedObj.load_file(MR_CACHE_PATH)

    mr_details_form(
        api          = app.gitlab,
        mrcache      = mrcache,
        ready        = app.cl.ready,
        skip_context = app.cl.skip_context,
        force_update = app.cl.force_update
    )

    prompt.print_mr(app, mrcache)
    if 'branch_exists' in mrcache:
        need_push = not mrcache.branch_exists
    else:
        mrcache.branch_exists = mrcache.source_branch  in (
            b.name for b in app.gitlab.list_branches(app.conf.project_id)
        )
        need_push = not mrcache.branch_exists

    if need_push:
        print(cstr("^1Remote branch^0 ^33{}^0 ^1does not exist.^0".format(
            git.current_branch()
        )))
        msg = "Push to ^34{}^0?".format(app.conf.gitlab_url)
        if prompt.yesno(msg, default=False):
            git.push_current()
            mrcache.branch_exists = True

    if mrcache.branch_exists:
        if 'remote_cache' not in mrcache:
            msg = "\nCreate merge request on ^34{}^39".format(
                app.conf.gitlab_url
            )
            if prompt.yesno(cstr(msg), default=False):
                set_assignee(app.gitlab, mrcache)
                create_mr(app, mrcache)
                print(cstr("\nMerge request ^32#{}^0 created: ^34{}^39".format(
                    mrcache.remote_cache.iid,
                    urljoin(app.conf.gitlab_url, url)
                )))
        else:
            url = '/{}/merge_requests/{}'.format(
                app.conf.project,
                mrcache.remote_cache.iid
            )
            # Update instead of creating
            msg = "\nUpdate merge request ^32#{} ^34{}^39".format(
                mrcache.remote_cache.iid,
                urljoin(app.conf.gitlab_url, url)
            )
            if prompt.yesno(cstr(msg), default=True):
                set_assignee(app.gitlab, mrcache)
                update_mr(app, mrcache)


def set_assignee(api, mrcache):
    if 'assignee' not in mrcache:
        user = prompt.autouser(api, 'Assign to')
        if user is not None:
            mrcache.assignee = user


def mr_details_form(api, mrcache, ready, skip_context, force_update):
    mrcache.source_branch = str(git.current_branch())

    # Title
    if 'title' not in mrcache or 'title' in force_update:
        prefix = '' if ready else '[WIP] '
        mrcache.title = prefix + raw_input(cstr('^1Title:^0 '))
    else:
        if not ready and not mrcache.title.startswith('[WIP] '):
            mrcache.title = '[WIP] ' + mrcache.title
        elif ready and mrcache.title.startswith('[WIP] '):
            mrcache.title = mrcache.title[6:]
        prompt.form_print('Title', mrcache.title)

    # Assign To
    if 'assignee' in force_update:
        user = prompt.autouser(api, 'Assign to')
        if user is not None:
            mrcache.assignee = user
    elif 'assignee' in mrcache:
        prompt.form_print('Assign to', mrcache.assignee.username)

    # Description
    mrcache.description = forms.mr_description(
        mrcache,
        skip_context=skip_context,
        force_update=force_update
    )

    return mrcache


def create_mr(app, mrcache):
    mr = extract_mr(mrcache)
    logging.debug("Creating merge request: {}".format(mr))
    mrcache.remote_cache = app.gitlab.create_mr(app.conf.project_id, mr)


def update_mr(app, mrcache):
    diff = mrdiff(mrcache)
    if not diff:
        print(cstr("^1No changes, skipping^0"))
    else:
        logging.debug("Updating Merge request {} with: {}".format(
            mrcache.remote_cache.id, diff
        ))
        mrcache.remote_cache = app.gitlab.update_mr(
            app.conf.project_id, mrcache.remote_cache.id, diff
        )

