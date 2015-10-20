# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import textwrap
import io

from fabric.api import sudo, cd, settings, shell_env, put
from fabric.contrib.files import upload_template

from ..fabian import (
    create_user,
    create_postgres_db,
    create_postgres_user,
    virtualenv,
    generate_password,
    git_clone,
)


def redmine_installer(user, port, prefix, **kwargs):
    """
    Create a new, user and database, and install redmine into that user's home directory.
    significant keyword args are
        - ``dbname``, ``db_host``, ``db_port``, ``db_user`` which all define postgres connection parameters.
        - ``ruby_version`` specifies a version of ruby to install from the system repository e.g. ``ruby_version='ruby2.1'``
        - ``redmine_dir`` an unqualified path into which redmine will be installed
        - ``redmine_revision`` the version of redmine to install (a git tag from the redmine repo.
        - ``
    """
    ruby = kwargs.get('ruby_version', 'ruby2.1')
    with shell_env(DEBIAN_FRONTEND='noninteractive'):
        with settings(warn_only=True):
            result = sudo("apt-get install -y %s ruby-dev rubygems" % ruby)
        if not result.succeeded:
            # ubuntu and debian seem to differ here; ubuntu14 doesn't ship ruby2.1
            sudo("apt-get install -y ruby ruby-dev rubygems-integration")

    db_password = kwargs.get('db_password', generate_password())
    db_name = kwargs.get('db_name', 'redmine_production')
    db_host = kwargs.get('db_host', '127.0.0.1')
    db_port = kwargs.get('db_port', 5432)
    db_user = kwargs.get('db_user', user)

    home = create_user(user)
    if not kwargs.get('db_host'):
        create_postgres_user(user, db_password)
        create_postgres_db(user, db_name)

    install_dir = '%s/%s' % (home, kwargs.get('redmine_dir', 'redmine'))

    redmine_db_conf = textwrap.dedent("""
        production:
            adapter: postgresql
            encoding: utf8
            reconnect: false
            database: {0}
            username: {1}
            password: {2}
            host: {3}
            port: {4}
        """).format(db_name, db_user, db_password, db_host, db_port)

    git_clone(install_dir, repo_url='https://github.com/redmine/redmine',
        revision=kwargs.get('redmine_revision', '3.1-stable'), user=user
    )

    with cd(install_dir), shell_env(GEM_HOME=home):
        with settings(sudo_user=user):
            sudo('gem install bundler')
        put(io.StringIO(redmine_db_conf), 'config/database.yml', mode=0600, use_sudo=True)
        sudo("chown %s config/database.yml" % user)
        put(io.StringIO("gem 'thin'\n"), 'Gemfile.local', use_sudo=True)
        sudo("chown %s Gemfile.local" % user)

        with settings(sudo_user=user),\
             shell_env(RAILS_ENV='production', REDMINE_LANG='en', GEM_HOME=home):
            path = "%s/bin/" % home
            sudo(path + "bundle install --path --without development test rmagick")
            sudo(path + "bundle exec rake generate_secret_token")
            sudo(path + "bundle exec rake db:migrate")
            sudo(path + "bundle exec rake redmine:load_default_data")

    return {
        'name': kwargs.get('appname', 'redmine-%s' % user),
        'directory': install_dir,
        'command': home + '/bin/bundle exec thin start -e production -a %s -p %s' % ('127.0.0.1', port),
        'environment': {'GEM_HOME': home, 'RAILS_ENV': 'production'},
        'static_dir': '%s/public' % install_dir,
    }
