# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os

from fabric.api import sudo, cd, settings
from fabric.contrib.files import upload_template

from ..fabian import (
    create_user,
    create_postgres_db,
    create_postgres_user,
    virtualenv,
    generate_password,
)


def sentry_installer(user, port, prefix, **kwargs):
    home = create_user(user)
    install_dir = '%s/sentry' % home
    host = kwargs.get('host', '127.0.0.1')
    db_password = kwargs.get('db_password', generate_password())
    db_host = kwargs.get('db_host', '127.0.0.1')
    db_port = kwargs.get('db_port', 5432)
    db_user = kwargs.get('db_user', user)
    db_name = kwargs.get('db_name', 'sentry')
    secret_key = kwargs.get('secret_key', generate_password(128))
    extra_config_statements = ('%s = %s' % (str(k), repr(v)) for k, v in kwargs.get('config_extra', {}).items())

    if not kwargs.get('db_host'):
        create_postgres_user(db_user, db_password)
        create_postgres_db(db_user, db_name)

    config_path = "%s/.sentry/sentry.conf.py" % home
    with cd(home), settings(sudo_user=user):
        virtualenv(install_dir, user)
        sudo(install_dir + '/bin/pip install sentry==%s psycopg2' % kwargs.get('sentry_version', '<8'))
        sudo("mkdir -p %s/.sentry" % home)

    SENTRY_URL_PREFIX = kwargs.get('sentry_url_prefix')
    if not SENTRY_URL_PREFIX:
        SENTRY_URL_PREFIX = raw_input("please enter the sentry_url_prefix (no trailing slash)")
    upload_template(
        'sentry.conf.template',
        config_path,
        context={
            'SECRET_KEY': secret_key,
            'SENTRY_URL_PREFIX': kwargs.get('sentry_url_prefix', prefix),
            'SENTRY_WEB_PORT': port,
            'DATABASES': repr({
                'default':{
                    'ENGINE': 'django.db.backends.postgresql_psycopg2',
                    'NAME': db_name,
                    'USER': db_user,
                    'PASSWORD': db_password,
                    'HOST': db_host,
                    'PORT': db_port,
                    'OPTIONS': {'autocommit': True,}
                }
            }),
            'ALLOWED_HOSTS': kwargs.get('ALLOWED_HOSTS', ['*']),
        },
        use_jinja=True,
        use_sudo=True,
        mode=0600,
        backup=False,
        template_dir=os.path.dirname(__file__)
    )
    sudo("chown %s:%s %s" % (user, user, config_path))
    with cd("%s/%s/" %(home, install_dir)), settings(sudo_user=user):
        sudo("bin/sentry syncdb --noinput")
        sudo("bin/sentry migrate --noinput")

    return {
        'name': 'sentry_%s' % user,
        'directory': install_dir,
        'command': install_dir + '/bin/sentry start http',
        'environment': {},
    }
