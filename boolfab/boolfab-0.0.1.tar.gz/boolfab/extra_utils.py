from __future__ import print_function
from contextlib import contextmanager
from fabric.api import *
from fabric.colors import green, red
from fabric.utils import warn

def quiet_run(cmd, *args, **kwargs):
    with quiet():
        return run(cmd, *args, **kwargs)

def mkdir_p(p):
    run('mkdir -p {}'.format(p))

def ensure_prepend(filepath, line, use_sudo=False):
    fn = sudo if use_sudo else run
    fn("grep -q -x -F \'{s}\' {p} || sed -i '1s;^;{s}\\n;' {p}".format(p=filepath, s=line))

def ensure_appended(filepath, line, use_sudo=False):
    fn = sudo if use_sudo else run
    fn('grep -q -x -F \'{s}\' {p} || echo \'{s}\' | cat >> {p}'.format(p=filepath, s=line))

def read_ssh_conf(p):
    ssh_config = local('cat {}'.format(p), capture=True)
    conf = {}
    for line in ssh_config.splitlines():
        key, value = line.split()
        conf[key] = value.replace('"', '')
    return conf

@contextmanager
def switch_user(user):
    pre = env.user
    env.user = user
    yield
    env.user = pre

@contextmanager
def use_ssh_conf(ssh_conf_dict):
    pre_env = {'u': env.user, 'p': env.port, 'h': env.host_string, 'k': env.key_filename}
    env.user = ssh_conf_dict['User']
    env.port = ssh_conf_dict['Port']
    env.host_string = ssh_conf_dict['HostName']
    env.key_filename = ssh_conf_dict['IdentityFile']
    yield
    env.user = pre_env['u']
    env.port = pre_env['p']
    env.host_string = pre_env['h']
    env.key_filename = pre_env['k']

def expect_contains(cmd, exp_outs, error_msg="", check_msg=""):
    print('Checking {}..'.format(cmd if not check_msg else check_msg), end="")
    if isinstance(exp_outs, basestring):
        exp_outs = [exp_outs]
    with settings(warn_only=True):
        out = run(cmd)
        all_ok = True
        for exp_out in exp_outs:
            if exp_out in out:
                print(exp_out, green('OK'))
            else:
                print(red("FAIL!!"), exp_out)
                print(error_msg)
                all_ok = False
        return all_ok

def md5_is_ok(filepath, exp):
    md5 = run('md5sum {}'.format(filepath)).lower().split()[0]
    is_ok = exp.lower() == md5
    if not is_ok:
        warn('bad md5 at "{}" was: {}, expected: {}'.format(filepath, repr(md5), repr(exp)))
    return is_ok

def render_template(fp, kv):
    """ fp: path to text file. kv: dict like 
        return: content of file where variables have been rendered according to dict
        e.g.: if content is "hello {word}" and kv is {word: "hello"} it will return "hello world"
    """
    with open(fp) as f:
        return f.read().format(**kv)

def write(fp, what):
    with open(fp, 'w') as f:
        f.write(what)
