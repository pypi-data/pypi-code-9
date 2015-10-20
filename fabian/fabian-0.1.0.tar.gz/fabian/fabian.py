# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import itertools
import io
import textwrap
import string
import glob

from random import SystemRandom

from fabric.api import task, cd, env, put, get, run, sudo, settings, hide
from fabric.contrib.files import upload_template, append
from fabric.context_managers import shell_env


def _iter_to_cmdline(iterable):
    return ' '.join(x.strip() for x in iterable if not x.startswith('#'))


def file_exists_nonempty(path):
    with settings(warn_only=True, sudo_user='root'):
        result = sudo('stat --printf "%s" {}'.format(path))
    try:
        return result.succeeded and int(result) > 0
    except ValueError:
        return False


def get_home(user=None):
    user = user or env.user
    result = run('getent passwd %s' % user)
    return result.split(':')[5]


def generate_password(len=32):
    random = SystemRandom()
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(len))


def sys_update(*args, **kwargs):
    sudo('apt-get update -qq')


def sys_upgrade(*args, **kwargs):
    with shell_env(DEBIAN_FRONTEND='noninteractive'):
        sudo('apt-get upgrade -q -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confnew"')


def install_packages(packages):
    with shell_env(DEBIAN_FRONTEND='noninteractive'):
        if type(packages) in (list, tuple):
            for package in packages:
                if type(package) == dict:
                    longest_word = max(package['debconf'].split(), key=len)
                    heredoc = longest_word.upper() + 'EOF'
                    debconf_string = package['debconf']
                    sudo('debconf-set-selections <<%(heredoc)s\n'
                         '%(debconf_string)s\n'
                         '%(heredoc)s' % locals()
                    )
                    sudo('apt-get install -y -q %s' % package['package'])
                else:
                    sudo('apt-get install -y -q %s' % package)
        else:
            sudo('apt-get install -q -y -o'
                 ' Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confnew" ' + packages
            )


def sys_deps(config=None, extras=None):
    """
    Install core system dependencies, along with other packages specified in
    ``config.SYS_DEPS``
    any packages listed in ``extras`` are also installed.
    Default package-configuration questions are overridden with Dpkg::options.
    """
    extras = extras or list()
    if not hasattr(extras, '__iter__'):
        extras = [extras]
    extras += getattr(config, 'SYS_DEPS', [])

    install_packages('git-core python-dev postgresql-client ca-certificates'
            ' sqlite libxml2-dev libxslt1-dev build-essential python-pip'
            ' libmysqlclient-dev mysql-client libssl-dev libffi-dev'
            ' libz-dev pkg-config libpq-dev ssl-cert'
            ' supervisor ntp python-virtualenv nginx'
        )
    install_packages(extras)


def sys_firewall(config=None, **kwargs):
    # we have to put have a default ``INPUT ACCEPT`` Policy first
    # otherwise we don't have time to add the input rules for ssh and get totes borked
    sudo("""
        iptables -P INPUT ACCEPT; ip6tables -P INPUT ACCEPT
        iptables -P OUTPUT ACCEPT; ip6tables -P OUTPUT ACCEPT
        iptables -P FORWARD DROP; ip6tables -P FORWARD DROP
        iptables -F; ip6tables -F
        iptables -A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
        ip6tables -A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
        iptables -A INPUT -p tcp -m tcp --dport 22 -m conntrack --ctstate NEW -j ACCEPT
        iptables -A INPUT -i lo -j ACCEPT; ip6tables -A INPUT -i lo -j ACCEPT
        # Now replace the default input policy
        iptables -P INPUT DROP; ip6tables -P INPUT DROP
        """
    )
    for rule in getattr(config, 'IPTABLES_RULES', []):
        sudo('iptables %s' % rule)
        sudo('ip6tables %s' % rule)
    for port in getattr(config, 'OPEN_TCP_PORTS', []):
        sudo('ip6tables -A INPUT -p tcp -m tcp --dport %d -m conntrack --ctstate NEW -j ACCEPT' % int(port))
        sudo('iptables -A INPUT -p tcp -m tcp --dport %d -m conntrack --ctstate NEW -j ACCEPT' % int(port))
    sudo('iptables-save')
    sudo('ip6tables-save')
    with shell_env(DEBIAN_FRONTEND='noninteractive'):
        sudo('echo iptables-persistent iptables-persistent/autosave_v4 boolean true | debconf-set-selections')
        sudo('echo iptables-persistent iptables-persistent/autosave_v6 boolean true | debconf-set-selections')
        install_packages('iptables-persistent')


def install_pip_requirements_virtualenv(virtualenv_dir, requirements=None,
                                        user=None, config=None, update=False, **kwargs):
    """
    Given a python virtualenv and an (optional) set of ``requirements``
    install those requirememts into the virtualenv.
    """
    user = user or env.user
    update = update and '-U' or ''
    if requirements is None:
        with cd(virtualenv_dir), settings(sudo_user=user):
            return sudo('bin/pip install %s -r requirements.txt' % update)

    if type(requirements) == str:
        with cd(virtualenv_dir), settings(sudo_user=user):
            return sudo('bin/pip install %s -r %s' % (update, requirements))

    if type(requirements) in (list, tuple):
        sudo('bin/pip install %s %s' % (update, _iter_to_cmdline(requirements)))

    pip_requirements = getattr(config, 'PIP_REQUIREMENTS', [])
    if pip_requirements:
        return sudo('bin/pip install %s %s' % (update, requirements))


def virtualenv(install_dir, user=None, **kwargs):
    """
    Create a new virtualenv on the host, ``in install_dir`` owned by ``user``
    """
    if (not user) or user == env.user:
        return run('virtualenv --no-site-packages %s' % install_dir)
    with settings(sudo_user=user):
        return sudo('virtualenv --no-site-packages %s' % install_dir,)


def install_supervisor_app(user, basedir, command, environment, appname,
                           sudo_user='root', conf_dir=None, config=None, **kwargs):
    conf_dir = conf_dir or getattr(config, 'SUPERVISORD_CONF_DIR', '/etc/supervisor/conf.d/')
    app_config_path = '%s/%s.conf' % (conf_dir, appname)

    with settings(sudo_user=sudo_user):
        upload_template(
            'supervisor_app.conf.template',
            app_config_path,
            context={
                'name': appname,
                'user': user,
                'directory': basedir,
                'command': command,
                # supervisor needs percent signs escaped; see http://supervisord.org/configuration.html
                'environment': {k:str(v).replace('%', '%%') for k, v in environment.items()}
            },
            use_jinja=True,
            template_dir=os.path.join(os.path.dirname(__file__), 'templates'),
            use_sudo=sudo_user != env.user,
            mode=0400,
            backup=False
        )
    sudo("chown %s:%s '%s'" % (sudo_user, sudo_user, app_config_path))


def supervisord_reload_config(prog_name=None, **kwargs):
    sudo('supervisorctl reread')
    sudo('supervisorctl update')


def supervisord_restart_apps(apps=None):
    if type(apps) not in (str, tuple):
        apps = [apps]
    for app in apps:
        sudo('supervisorctl restart %s' % app)


def supervisord_purge_all(conf_dir=None, config=None, **kwargs):
    conf_dir = conf_dir or getattr(config, 'SUPERVISORD_CONF_DIR', '/etc/supervisor/conf.d/')
    sudo('supervisorctl stop all')
    sudo('rm -rf %s/*' % conf_dir)
    supervisord_reload_config(config=config)


def git_clone(into, repo_url, revision=None, user=env.user, **kwargs):
    with settings(sudo_user=user):
        sudo('git clone -q %s %s' % (repo_url, into))
        #checkout specified revision if it exists
        if revision is not None:
            with(cd(into)):
                sudo('git checkout --force %s' % revision)


def git_checkout_rev(user, repo_path, revision='master', remote='origin'):
    """Given an existing git repository ``repo_path``, checkout the given
    ``revision`` or 'master' from the given ``remote`` or 'origin``
    WARNING: Any local changes to the repository will be discarded.
    """
    with cd(repo_path), settings(sudo_user=user):
        sudo('git checkout -f && git pull %s && git' % revision)


def user_exists(user):
    """ripped straight out of fabtools"""
    with settings(hide('running', 'stdout', 'warnings'), warn_only=True):
        return run('getent passwd %s' % user).succeeded


def delete_user(user):
    """deletes the given user (and home directory)"""
    if user_exists(user):
        sudo('deluser --remove-home %s' % user)


def create_user(user, authorized_keys=None):
    """
    Creates the given user on the host (password-disabled) and copies local SSH
    public keys to remote's `authorized_keys` file.

    Returns the new user's home directory path.
    authorized_keys can be a list of paths to public key strings,
    a list of public key strings, or a combination.
    We try to open each string as a file first, so if there is a file with the
    name of your public keys string in the local path, all bets are off.
    """
    authorized_keys = authorized_keys or []
    keys = []
    for f in authorized_keys:
        try:
            with open(f) as fp:
                keys.append(fp.read())
        except IOError:
            keys.append(authorized_keys)

    if not user_exists(user):
        sudo('adduser --gecos "" --quiet --disabled-password %s' % user)

    home = get_home(user)
    # Always update ssh keys for now
    sudo('mkdir -p %s/.ssh' % home)
    put(
        io.StringIO('\n'.join(keys)),
        remote_path='/%s/.ssh/authorized_keys' % home,
        mode=600,
        use_sudo=True
    )
    ssh_dir = '%s/.ssh' % home
    sudo('chown -R %s:%s %s' % (user, user, ssh_dir))
    sudo('chmod 700 %s' % ssh_dir)
    sudo('chmod 600 %s/*' % ssh_dir)

    return home


def delete_psql_user_and_databases(user, db):
    if type(db) not in (list, tuple):
        db = (db,)
    sudo('psql -c "DROP DATABASE IF EXISTS %s;"' % db, user='postgres')
    sudo('psql -c "DROP USER IF EXISTS %s;"' % user, user='postgres')


def create_postgres_db(owner, dbname, encoding='UTF8', **kwargs):
    with settings(sudo_user='postgres'):
        sudo('''psql -c "CREATE DATABASE %s WITH ENCODING='%s' OWNER %s"''' %
        (dbname, encoding, owner),
    )


def create_postgres_user(user, password):
    with settings(sudo_user='postgres'), shell_env(HISTFILE='/dev/null'):
        sudo('psql -c "CREATE USER %s WITH NOCREATEDB NOCREATEUSER ENCRYPTED PASSWORD E\'%s\';"' %
        (user, password),
        user='postgres'
    )


def clean_install(config=None, **kwargs):
    sys_update(config, **kwargs)
    sys_firewall(config, **kwargs)
    sys_upgrade(config, **kwargs)
    sys_deps(config, extras=kwargs.get('extras'))


def generate_self_signed_ssl(basename, key_dir='/etc/ssl/private',
                             cert_dir='/etc/ssl/certs', owner='root',
                             algorithm='RSA', bits=2048, days=365):
    """
    Generate a new SSL certificate and key of RSA, or ECDSA public key ``algorithm``,
    with the given key ``bits``. ``bits`` is currently ignored for EC certificates
    The installed key will be readable only by ``owner``.
    The generated key and certificate will be stored in ``key_dir`` and ``cert_dir`` respectively.
    Certificate will be valid for ``days``
    """
    algorithm = algorithm.upper()
    assert algorithm in ('ECDSA', 'RSA')

    key_path = '%s/%s.key' % (key_dir, basename)
    cert_path = '%s/%s.pem' % (cert_dir, basename)
    with settings(sudo_user=owner):
        sudo('touch %s' % key_path)
        sudo('chmod 0600 %s' % key_path)
        if algorithm == 'ECDSA':
            sudo('openssl ecparam -genkey -nodes -out {key_path} -name prime256v1'.format(key_path=key_path))
            sudo('openssl req -new -key {key_path} -x509 -days {days} -out {cert_path}'.format(
                    key_path=key_path,
                    cert_path=cert_path,
                    days=days
                )
            )
        elif algorithm == 'RSA':
            sudo('openssl req -x509 -newkey rsa:{bits} -keyout {key_path} '
                 '-nodes -out {cert_path} -days {days}'.format(
                    key_path=key_path,
                    cert_path=cert_path,
                    bits=bits,
                    days=days
                )
            )

    sudo('chown root:ssl-cert %s' % key_path)

    return key_path, cert_path


def generate_dhparams(basename, key_dir='/etc/ssl/private', bits=2048, owner='root'):
    """
    Generate Diffie-Hellman parameters in pem format for TLS.
    """
    key_path = '%s/%s_dhparam.pem' % (key_dir, basename)

    with settings(sudo_user=owner):
        if not file_exists_nonempty(key_path):
            sudo('touch %s' % key_path)
            sudo('chmod 0600 %s' % key_path)
            sudo('chown root:ssl-cert %s' % key_path)
            sudo('openssl dhparam -out %s %s' % (key_path, bits))

    return key_path


def install_nginx_host_conf(hostname, applications, config=None, restart=False,
                            dh_params_path=None, ssl_key_cert_pair=None,
                            no_gen_dhparams=False, no_gen_ssl_cert=False,
                            no_rewrite_https=False, no_hsts=False,
                            delete_default_vhost=False, raw_server_directives='', **kwargs):
    """
    Installs an nginx virtualhost config for the given ``hostname``
    with a decent SSL setup (decent as of the time of writing).

    For each of ``applications``, will create a new reverse-proxy setup, to point
    the url ``prefix`` to the given origin server (the actual application).
    If there is no ``listen`` field in a given application, a static-only
    application served directly by nginx is created.

    required fields of ``applications`` are:
        - ``prefix`` the url path for the application.
        - ``name`` a name to give to each application block.

    optional ``applications`` fields:
        - ``listen``/``port`` If the application is to be reverse-proxied;
            these entries must **both** be present or **neither** present
        - ``port`` see above.
        - ``raw_location_directives`` text here will be copied verbatim
            into the nginx ``@location`` block for the given app.
        - ``static_dir`` The directory for the application's public assets.
            If not given, defaults the server root.
        - ``headers`` a dictionary of headers for nginx to set in the app's ``@location`` block.

    We also generate new Diffie-Helman ``dh_params_path`` parameters.
    If no SSL ``ssl_keypair`` tuple (secret key, and certificate bundle path) are available,
    we generate a new RSA self-signed certificate and key and install to `/etc/ssl/`.

    """
    certificate_bundle = None
    key_path = None
    hostname = hostname or ''
    cert_basename = hostname.replace('.', '_')
    if dh_params_path is None and (not no_gen_dhparams):
        dh_params_path = generate_dhparams(cert_basename)

    if ssl_key_cert_pair is None and (not no_gen_ssl_cert):
        key_path, certificate_bundle = generate_self_signed_ssl(cert_basename)
    elif not no_gen_ssl_cert:
        key_path, certificate_bundle = ssl_key_cert_pair

    nginx_virtualhost_dir = kwargs.get(
        'nginx_virtualhost_dir',
        getattr(config, 'NGINX_SITES_DIR', '/etc/nginx/sites-enabled/')
    )

    context={
        'applications': applications,
        'hostname': hostname,
        'certificate_bundle': certificate_bundle,
        'private_key': key_path,
        'dh_params_path': dh_params_path,
        'no_rewrite_https': no_rewrite_https,
        'no_hsts': no_rewrite_https,
        'raw_server_directives': raw_server_directives,
    }
    if kwargs.get('nginx_server_root'):
        context['root'] = kwargs['nginx_server_root']
    if hostname:
        vhost_config_path = '%s/%s.vhost' % (nginx_virtualhost_dir, hostname)
    else:
        vhost_config_path = '%s/default' % nginx_virtualhost_dir
    with settings(sudo_user='root'):
        upload_template(
            'nginx.conf.template',
            vhost_config_path,
            context=context,
            use_jinja=True,
            use_sudo=True,
            mode=0644,
            backup=False,
            template_dir=os.path.join(os.path.dirname(__file__), 'templates')
        )
        sudo('chown root:root %s' % vhost_config_path)
    if restart:
        sudo('service nginx restart')


def reverse_proxied_webapp(user, port, prefix, installer, appname=None, **kwargs):
    """
    Install a webapp behind nginx, in ``user``'s home directory with the given url ``prefix``
    using the ``installer`` callback to handle the application installation.
    ``kwargs`` will be passed directly to the ``installer`` callback.
    ``installer`` should return a dictionary with the following *mandatory* keys:
        ``command``: The command needed to run your application.
        ``environment``: The a dictionary of environment variables used by your application.
    The following keys are also significant (optional):
        ``name``: The name of your application as handled by supervisor. If not g
        ``directory`` The directory from which your app will be launched.
        If not given will default to ``user``'s home directory.
        ``
    E.G. to install a python hello world application for the user ``donny`` listening on port 10200
    you might do the following:

        def make_python_hello_world(user, port, prefix, **kwargs):
            import texwrap
            import io

            app_source = textwrap.dedent(
                '''
                import os
                from wsgiref import simple_server

                application = simple_server.make_server(
                    '127.0.0.1',
                    int(os.environ['LISTEN_PORT']), simple_server.demo_app
                )
                application.serve_forever()
                '''
            )

            home = create_user(user)
            put(
                io.StringIO(app_source),
                remote_path='/%s/myapp.py' % home,
                mode=0755,
                use_sudo=True
            )
            return {
                'command': 'python %s/myapp.py' % home,
                'environment': {'LISTEN_PORT': port, 'SCRIPT_NAME': prefix},
                'prefix': prefix,
            }


        install_nginx_host_conf(
            'example.com',
            [reverse_proxied_webapp('donny', 8000, '/', make_python_hello_world)]
        )
    """

    app = installer(user, port, prefix, **kwargs)
    app['name'] = app.get('name', user + '-app')
    app['directory'] = app.get('directory', get_home(user))
    app['listen'] = kwargs.get('listen', '127.0.0.1')
    app['port'] = port
    app['prefix'] = prefix
    app['user'] = user
    install_supervisor_app(
        app['user'],
        app['directory'],
        app['command'],
        app['environment'],
        app['name'],
        **kwargs
    )

    return app


def pgp_trust_key(user, key_id, fingerprint, trustlevel=3, keyserver='pgp.mit.edu'):
    """
    Install the public key identified by ``key_id`` (a 64bit PGP key)
    into ``user's`` keyring on the remote, and verify the key's signature, before
    trusting this key (``trustlevel`` defaults to 'marginal' in GPG parlance).
    """
    fingerprint = fingerprint.upper().replace(' ', '')
    assert trustlevel in range(1, 7)
    assert int(fingerprint, 16) # fingerprints are hexadecimal
    with settings(sudo_user=user):
        sudo('gpg --keyserver=%(keyserver)s --recv-keys %(key_id)s' % locals())
        sudo('echo %(fingerprint)s:%(trustlevel)s: | gpg --batch --import-ownertrust' % locals())


def reboot():
    sudo('reboot')
