#!/usr/bin/env python
"""
Conventions:

* Each service has a dedicated *nix user
* Use systemd
* No sudo, use root account when run system command
"""
from fabric.api import *

""" Custom variables """
class _X:
    app= None
    base_port= 7000
    n_instances= 2
    remote_path= '/home/'
    wait= 3
    excludes=('.*', 'tmp', '__pycache__', '*.pyc', 'upload', 'cache')
env.x = _X()

import datetime
import contextlib
import os, fnmatch
import shutil, time
from tempfile import NamedTemporaryFile as _Temp
import fabric.contrib.files as files
import fabric.context_managers as fab_context
import fabric.contrib.project as fab_project

def pwd(base_file):
    _pwd = os.path.dirname(base_file)
    os.chdir(_pwd)

def with_root():
    env.user = 'root'

@contextlib.contextmanager
def on_remote(path=''):
    with cd(os.path.join(env.x.remote_path, path)):
        yield

@contextlib.contextmanager
def venv(inside=''):
    with prefix('source {remote}/bin/activate' \
    .format(remote=env.x.remote_path)), cd(env.x.remote_path + inside):
        yield

def up_tokit():
    'git clone --single-branch --branch master https://github.com/manhg/tokit.git'
    with on_remote('tokit'):
        run('git fetch')
        run('git reset --hard origin/master')

def sync(dirs=None):
    if dirs:
        dirs = dirs.split(',')
    else:
        dirs = ['config', 'src', 'doc']
    for d in dirs:
        fab_project.rsync_project(remote_dir=env.x.remote_path, local_dir=d, exclude=env.x.excludes)

def pack():
    """ (1) Pack source code and send to remote server """
    # Alternative: Use fab_project.upload
    release_path = env.x.remote_path + '/tmp/%s_release.tgz' % env.x.app
    # To get UID: remote_uid = run('id -u')
    with _Temp(delete=False, suffix='.tgz') as tmp:
        local('tar cf {temp} src config doc'.format(temp=tmp.name))
        put(tmp.name, release_path)
    with on_remote():
        if files.exists('rollback'):
            run('rm -Rf rollback')
        if files.exists('config'):
            run('rm -Rf config')
        if files.exists('src'):
            run('mv src rollback')
        run('tar --extract --no-same-owner --preserve-permissions --file {release}'\
            .format(release=release_path))
        run('rm ' + release_path)

def backend(action='restart'):
    """ (3) Start services """
    with_root()
    systemd_reload()
    for instance in range(env.x.n_instances):
        run('systemctl {action} {app}@{port}.service'.format(
            action=action,
            app=env.x.app,
            port=env.x.base_port + instance))
        time.sleep(env.x.wait)

def config():
    """ (3) Link configs """
    with_root()
    with on_remote():
        # TODO sym link is better
        for instance in range(env.x.n_instances):
            service_file = "/etc/systemd/system/multi-user.target.wants/{app}@{port}.service" \
                .format(app=env.x.app, port=env.x.base_port + instance)
            run("ln -s -f {path}/config/app@.service {dest}" \
                .format(path=env.x.remote_path, dest=service_file))
        run('ln -s -f {path}/config/nginx.conf /etc/nginx/conf.d/{app}.conf' \
            .format(app=env.x.app, path=env.x.remote_path))

def rollback():
    with on_remote():
        run('mv src src-fail && mv rollback src')
        backend('restart')

def deploy():
    static_link()
    doc_gen()
    sync()
    requirements()
    backend('restart')
    static_copy()

def requirements():
    """ (2) Update dependancies """
    with on_remote():
        if not files.exists('bin'):
            run('pyvenv .')
        with venv('/src'):
            run('pip3 install --upgrade -r requirements.txt')
            # TODO update DB

def setup():
    """ (0) Init """
    # adduser
    # su
    # ssh-keygen
    # authorized_keys
    with on_remote():
        run('mkdir -p {tmp,shared,src}')

def static_copy():
    with_root()
    run('mkdir -p /var/www/{app}'.format(app=env.x.app))
    run('cp -R {path}/src/static /var/www/{app}/'.format(path=env.x.remote_path, app=env.x.app))
    run('chown -R nginx /var/www/{app}/'.format(path=env.x.remote_path, app=env.x.app))

def systemd_reload():
    with_root()
    run('systemctl daemon-reload')

def up_file(name):
    os.path.dirname(name)
    rel = os.path.relpath(name, PWD)
    print(put(name, os.path.join(env.x.remote_path, rel)))

def up_python():
    with_root()
    backend('restart')

def up_nginx():
    # Pitfall
    with_root()
    config()
    systemd_reload()
    run('nginx -t && systemctl reload nginx.service')


def nginx(action='restart'):
    with_root()
    # PITFALL: first start must be a restart, not reload
    run('nginx -t && systemctl ' + action + ' nginx.service')

def find_files(directory, patterns):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            for pattern in patterns:
                if fnmatch.fnmatch(basename, pattern):
                    yield (root, basename)

def pack_config():
    pass

def up_project():
    fab_project.rsync_project(
        remote_dir=env.x.remote_path, local_dir='src',
        upload=True, extra_opts='-a', exclude=('__pycache__'))

def doc_gen():
    with fab_context.lcd('doc'):
        local('make')

def doc():
    """ Generate and display document in browser"""
    doc_gen()
    with fab_context.lcd('doc'):
        local('cd _build/html && python3 -m http.server 7359 >/dev/null 2>&1 &')
        local('open http://localhost:7359/')

def pg_dump_schema(db=None):
    import getpass
    local_username = getpass.getuser()
    if not db:
        db = env.x.app
    local('pg_dump -s %s  > config/schema.sql' % db)
    local('sed -i s/{local}/{remote}/g config/schema.sql'.format(local=local_username, remote=env.x.app))

def pg_sync_schema():
    with _Temp(delete=False, suffix='.dat') as tmp:
        local('pg_dump -F c -Z 9 -f {temp} {db}'.format(temp=tmp.name, db=env.x.app))
        remote_sql = '{path}/tmp/schema.dat'.format(path=env.x.remote_path)
        put(tmp.name, remote_sql)
        run('pg_restore -d {app} --role={app} {sql}'.format(sql=remote_sql, app=env.x.app))

def static_link():
    """ Link static files in brick """
    original_dir = 'src'
    link_dir = 'static'
    for brick_path, basename in find_files(original_dir, ['*.css', '*.js', '*.tag']):
        static_path = brick_path.replace(original_dir, link_dir)
        if not os.path.exists(static_path):
            os.makedirs(static_path)
        # Make symlinks
        rel_path = os.path.relpath(original_dir, static_path)
        rel = os.path.join(brick_path.replace(original_dir, rel_path), basename)
        dst = os.path.join(static_path, basename)
        print(rel, dst)
        if not os.path.islink(dst):
            os.symlink(rel, dst)
    with fab_context.lcd(link_dir):
        # Remove all broken links
        local('find -xtype l -delete')
