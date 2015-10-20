# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os

from fabric.api import settings, sudo
from fabric.contrib.files import upload_template

from ..fabian import get_home, install_packages


def install_s3_tools(aws_access_key_id, aws_secret_access_key, user='root'):

    home = get_home(user)
    path = '%s/.s3cfg' % home

    install_packages('s3cmd')
    with settings(sudo_user=user):
        upload_template(
            's3cfg.conf.template',
            path,
            context={
                'AWS_ACCESS_KEY_ID': aws_access_key_id,
                'AWS_SECRET_ACCESS_KEY': aws_secret_access_key,
            },
            use_jinja=True,
            use_sudo=True,
            mode=0600,
            backup=False,
            template_dir=os.path.dirname(__file__)
    )

    sudo('chown %s:%s %s' % (user, user, path))