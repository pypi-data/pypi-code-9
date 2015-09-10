# -*- coding: utf-8 -*-
from peltak.config import MR_TEMPLATE_PATH, MR_CACHE_PATH
from .cache import CachedObj


def extract_mr(mrcache):
    mr = {
        'source_branch':    mrcache['source_branch'],
        'target_branch':    'master',
        'title':            mrcache['title'],
    }
    if 'description' in mrcache:
        mr['description'] = mrcache['description']

    if 'assignee' in mrcache:
        mr['assignee_id'] = mrcache['assignee'].id
    return mr


def _field_changed(name, current, remote):
    if name in current:
        if name not in remote:
            return True

        c, r = current[name], remote[name]
        if isinstance(c, dict) and isinstance(r, dict):
            return c.id != r.id
        return current[name] != remote[name]
    elif name in remote:
        return remote[name] is not None
    else:
        return True


def mrdiff(mrcache):
    """ Return the changes in the MR compared to the local cache. """
    changed = []
    for field in ('title', 'description', 'assignee'):
        if _field_changed(field, mrcache, mrcache.remote_cache):
            changed.append(field)

    ret = {}
    for field in changed:
        ret[field] = mrcache[field]

    return ret


def fetch_template(app):
    """ Fetch MR template from an gitlab issue.

    The issue should be labeled gitlab-cli and have a title equal to the
    value of ``config.mr_template_title``.
    """
    r = app.gitlab.api.get('issues?labels={}&state=opened'.format(
        app.conf.issue_label
    ))
    if r.status_code == 200:
        for issue in r.json():
            if issue['title'] == app.conf.mr_template_title:
                return issue['description'].replace('\r\n', '\n')
    return None


def resetmr_if_closed(app):
    """ Check if cached MR was closed. If so, reset the local MR cache.

    :return: ``True`` if MR was reset, ``False`` otherwise
    """
    mrcache = CachedObj.load_file(MR_CACHE_PATH)
    if 'remote_cache' in mrcache:
        mr = app.gitlab.get_mr(app.conf.project_id, mrcache.remote_cache.iid)
        if mr.state != "opened":
            mrcache.reset()
            return True
    return False

