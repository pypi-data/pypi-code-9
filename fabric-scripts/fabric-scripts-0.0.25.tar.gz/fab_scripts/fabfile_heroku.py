# coding: utf-8
from __future__ import with_statement
from functools import wraps
import codecs
import json
import os
import platform
import re
import subprocess
import sys
import time

from fabric.api import *
from fabric.colors import *
from fabric.utils import abort
from fabric.contrib.console import confirm

from .fab_utils import *
from .fabfile_s3 import *

# Examples of Usage
# fab -f fabfile_heroku.py --list
# fab --list
# fab localhost bootstrap
# fab localhost info
# fab localhost test
# fab localhost start_server
# fab production/staging bootstrap_heroku
# fab production/staging upload_static_files
# fab production/staging set_env_vars
# fab production/staging deploy
# fab production/staging rollback
# fab production/staging logs
# fab production/staging ssh
# fab localhost/production/staging ping
# fab localhost/production/staging warmup
# fab localhost/production/staging benchmark
# fab localhost/production/staging browse


# Environments

@task
def localhost():
    common()
    read_config_file('_localhost.json')
    env.heroku_app_git_remote = None
    env.heroku_worker_git_remote = None
    env.heroku_deploy_branch = None
    env.aws_bucket = 'codeart-localhost'
    print(blue("Localhost"))

@task
def staging():
    common()
    if current_git_branch() != 'staging':
        if not confirm('Using staging environment without staging branch (%s). Are you sure?' % current_git_branch()):
            abort('cancelled by the user')
    env.venv = 'envstaging'
    read_config_file('_staging.json')
    env.heroku_app_git_remote = 'heroku-staging'
    env.heroku_worker_git_remote = 'heroku-worker-staging'
    env.heroku_deploy_branch = 'staging:master'
    env.aws_bucket = env.heroku_app
    print(blue("Staging"))

@task
def production():
    common()
    if current_git_branch() != 'master':
        if not confirm('Using production environment without master branch (%s). Are you sure?' % current_git_branch()):
            abort('cancelled by the user')
    read_config_file('_production.json')
    env.heroku_app_git_remote = 'heroku'
    env.heroku_worker_git_remote = 'heroku-worker'
    env.heroku_deploy_branch = 'master'
    env.aws_bucket = env.heroku_app
    print(blue("Production"))

def common():
    env.python = 'python2.7'
    env.url = 'http://localhost:8000'
    env.host = 'localhost'
    env.port = 8000
    env.heroku_app = None
    env.heroku_app_addons = []
    env.heroku_worker = None
    env.heroku_worker_addons = []
    env.heroku_cedar = None
    env.paths = []
    env.vars = {}
    env.shared_vars = []

    env.run = local
    env.sudo = local
    env.cd = lcd
    env.venv = 'env'


# Utilities

def prepare_heroku(app_name, addons, branch=None, domain=None, cedar=None):
    print(red("Configuring heroku"))
    with settings(warn_only=True):
        env.run('heroku apps:create %s' % app_name)
        if branch:
            env.run('git remote add %s git@heroku.com:%s.git' % (branch, app_name))
        if cedar:
            env.run('heroku stack:set %s --app %s' % (cedar, app_name))
        for addon in addons:
            env.run('heroku addons:create %s --app %s' % (addon, app_name))
            if addon == 'newrelic':
                with prefix(venv()):
                    newrelic_key = env.run('heroku config:get NEW_RELIC_LICENSE_KEY --app %s' % (app_name), capture=True)
                    env.run('newrelic-admin generate-config %s newrelic.ini' % newrelic_key)
        if domain and not domain.endswith('herokuapp.com'):
            env.run('heroku domains:add %s --app %s' % (domain, app_name))
    print(green("Bootstrap success"))

# Tasks Localhost

@task
def bootstrap():
    print(red("Configuring application"))
    env.run('virtualenv %(env)s -p %(python)s --no-site-package' % dict(env=env.venv, python=env.python))
    with prefix(venv()):
        env.run('pip install -r requirements.txt')
        start_server()
    print(green("Bootstrap success"))

@task
def info():
    with prefix(venv()):
        env.run(python('--version'))
    if env.heroku_app:
        env.run('heroku config --app %s' % env.heroku_app)
    if env.heroku_worker:
        env.run('heroku config --app %s' % env.heroku_worker)

@task
def test():
    with prefix(venv()):
        env.run(vrun('tox'))

@task
def start_server(foreman=True, app='app.py'):
    with prefix(venv()):
        if foreman:
            env.run('foreman start -p %s' % env.port)
        else:
            env.run('python %s' % app)

# Tasks Production/Staging

@task
def bootstrap_heroku():
    if env.heroku_app:
        prepare_heroku(env.heroku_app, env.heroku_app_addons,
            branch=env.heroku_app_git_remote, domain=env.host, cedar=env.heroku_cedar)
    if env.heroku_worker:
        prepare_heroku(env.heroku_worker, env.heroku_worker_addons,
            branch=env.heroku_worker_git_remote, cedar=env.heroku_cedar)

@task
def set_env_vars():
    def vars_line(data):
        return ' '.join(['%s="%s"' % (var, value) for var, value in data.items()])

    for var_name, value in env.vars.items():
        if value.startswith('$'):
            env.vars[var_name] = os.getenv(value[1:], '') or ''

    varsline = vars_line(env.vars)
    if env.heroku_app and varsline:
        env.run('heroku config:set %(vars)s --app %(app)s' % dict(vars=varsline, app=env.heroku_app))
    if env.heroku_worker:
        if varsline:
            env.run('heroku config:set %(vars)s --app %(app)s' % dict(vars=varsline, app=env.heroku_worker))
        if env.heroku_app:
            shared_vars = {}
            for var_name in env.shared_vars:
                value = env.run('heroku config:get %(var)s --app %(app)s' % dict(var=var_name, app=env.heroku_app), capture=True)
                shared_vars[var_name] = value
            varsline = vars_line(shared_vars)
            if varsline:
                env.run('heroku config:set %(vars)s --app %(app)s' % dict(vars=varsline, app=env.heroku_worker))

@task
def deploy(tag=None, folder='static'):
    print(red("Deploying"))
    with prefix(venv()):
        upload_static_files(folder=folder)

    if env.heroku_app:
        set_env_vars()
        env.run('git push %s %s' % (env.heroku_app_git_remote, env.heroku_deploy_branch))
        env.run('heroku ps:scale web=1 --app %s' % env.heroku_app)
        if env.heroku_worker:
            env.run('heroku ps:scale worker=0 --app %s' % env.heroku_app)

    if env.heroku_worker:
        env.run('git push %s %s' % (env.heroku_worker_git_remote, env.heroku_deploy_branch))
        if env.heroku_app:
            env.run('heroku ps:scale web=0 --app %s' % env.heroku_worker)
        env.run('heroku ps:scale worker=1 --app %s' % env.heroku_worker)

    warmup()

    if tag:
        reset_tag(tag)
        create_tag(tag)
    else:
        last_tag = last_git_tag()
        if last_tag:
            tag = autoincrement_tag(last_tag)
        else:
            tag = '0.0.0'
        create_tag(tag)

    print(green("Deploy success (%s)" % tag))

@task
def rollback(tag=None, worker=False):
    app = env.heroku_worker if worker else env.heroku_app
    env.run('heroku releases --app %s' % app)
    if not confirm('Rollback (tag %s). Are you sure?' % tag):
        abort('cancelled by the user')
    if tag:
        env.run('heroku rollback --app %s' % app)
    else:
        env.run('heroku rollback %s --app %s' % (tag, app))

@task
def logs(worker=False):
    app = env.heroku_app if not worker else env.heroku_worker
    env.run('heroku logs -n 100 --app %s' % app)
    env.run('heroku logs --tail --app %s' % app)

@task
def console(worker=False):
    if env.heroku_worker or worker:
        env.run('heroku run python --app %s' % env.heroku_worker)
    else:
        env.run('heroku run python --app %s' % env.heroku_app)

# Tasks Localhost/Production/Staging

@task
def ping(time=3):
    env.run('ping -c %(time)s %(host)s:%(port)s' % dict(time=time, host=env.host, port=env.port))

@task
def warmup():
    for path in env.paths:
        weighttp(env.url + path, requests=5000, concurrency=10)

@task
def benchmark():
    for path in env.paths:
        weighttp(env.url + path, requests=10000, concurrency=50)

@task
def browse():
    env.run('open %s' % env.url)
