# -*- coding: utf-8 -*-
from __future__ import absolute_import
import re
from six import PY2, PY3
from collections import OrderedDict
from ..core import git
from ..core.api import Gitlab
from ..common.cache import CachedObj
from ..config import CONFIG_PATH
from ..actions import actions
from . import forms
actions.discover()
if PY2:
    from urlparse import urlparse
elif PY3:
    from urllib.parse import urlparse


class AppContext(object):
    """

    **Members**
    :conf:      App config. Will save changes to disk on every update.
    :cl:        Parsed command line arguments.
    :gilab:     Gitlab API client.
    """
    def __init__(self, cmdline):
        self.conf = CachedObj.load_file(CONFIG_PATH)
        self.cl = cmdline
        self.gitlab = None
        self.load_config()

    def _parse_origin(self, origin):
        m = re.match(r'.*?@(?P<url>[^:]+):(?P<project>.*?).git', origin)
        if m:
            url = 'https://{}'.format(m.group('url'))
            project = m.group('project')
        else:
            url = urlparse(origin)
            if url.path.endswith('.git'):
                project = url.path[1:-4]
            else:
                project = url.path[1:]
            url = '{url.scheme}://{url.hostname}'.format(url=url)

        return url, project

    def load_config(self):
        url, project = self._parse_origin(git.get_origin())
        defaults = OrderedDict({
            'project':           project,
            'gitlab_url':        '{url}'.format(url=url),
            'mr_template_title': 'mr-template',
            'issue_label':       'peltak',
            'verify_ssl':        True,
        })
        for name, value in defaults.items():
            if name not in self.conf:
                setattr(self.conf, name, value)

    def authenticate(self, get_user_details_fn=forms.login):
        """ This should authenticate the user against gitlab.

        :arg cmdline:   The return value from ArgumentParser.parse_args()
        :return:    Authenticated Gitlab instance ready for communication with
                    the API.

        It can be an interactive process where user provides his details.
        """
        token = self.conf.get('token')
        self.gitlab = Gitlab(
            url        = self.conf.gitlab_url,
            token      = token,
            verify_ssl = self.conf.verify_ssl
        )
        if not self.gitlab.logged_in:
            user, pw, save = get_user_details_fn()
            user = self.gitlab.login(user, pw)
            self.gitlab.token = user.private_token
            if save:
                self.conf.token = self.gitlab.token

        # Cache current project ID if missing
        if 'project_id' not in self.conf:
            project = self.gitlab.get_project(self.conf.project)
            self.conf.project_id = project.id

