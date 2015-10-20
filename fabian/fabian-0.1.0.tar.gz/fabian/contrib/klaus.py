# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from fabric.api import sudo, cd, settings, shell_env, put
from fabric.contrib.files import upload_template

from ..fabian import (
    create_user,
    virtualenv,
    generate_password,
    git_clone,
)


def klaus_installer(user, port, prefix, **kwargs):
    """
    simple installer for klaus, a simple git viewer.
    https://github.com/jonashaag/klaus
    """
    host =  kwargs.get('host', '127.0.0.1')
    repo_path = kwargs.get('repo_path', '/srv')
    klaus_env = {
        'KLAUS_REPOS': repo_path,
        'KLAUS_SITE_NAME': kwargs.get('appname', 'Klaus'),
        'KLAUS_USE_SMARTHTTP': kwargs.get('KLAUS_USE_SMARTHTTP', True),
        'SCRIPT_NAME': prefix,
    }
    klaus_env.update({k: v for k, v in kwargs.items() if k.startswith('KLAUS_')})

    home = create_user(user)
    install_dir = home + '/klaus'    
    sudo("mkdir -p %s" % repo_path)
    virtualenv(install_dir, user)

    with cd(install_dir), settings(sudo_user=user):
        sudo('bin/pip install klaus gunicorn')
    
    return {
        'name': kwargs.get('appname', 'klaus-%s' % user),
        'directory': install_dir,
        'command': '%s/bin/gunicorn klaus.contrib.wsgi:application -b %s:%s' % (
            install_dir, host, port
        ),
        'environment': klaus_env,
    }
