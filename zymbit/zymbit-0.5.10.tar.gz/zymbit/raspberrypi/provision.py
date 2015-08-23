from __future__ import absolute_import

import inspect
import os
import shutil

from zymbit.util import run_command

from . import config
from . import util


def call_distro_fn(*args, **kwargs):
    distro = util.get_distro()

    last_frame = inspect.currentframe().f_back
    fn_name = inspect.getframeinfo(last_frame).function
    distro_fn_name = '{}_{}'.format(fn_name, distro)

    return globals()[distro_fn_name](*args, **kwargs)


def enable_init_script():
    return call_distro_fn()


def enable_init_script_arch():
    command = ('/usr/bin/systemctl', 'enable', 'zymbit')

    return run_command(command)


def enable_init_script_raspbian():
    os.chmod(config.INIT_SCRIPT_PATH, 0755)

    script_dir = os.path.dirname(config.INIT_SCRIPT_PATH)

    command = ('/usr/sbin/update-service', '--add', script_dir)

    return run_command(command)


def setup_metrics():
    return call_distro_fn()


def setup_metrics_arch():
    return 0  # the file is already in the correct location


def setup_metrics_raspbian():
    dest = '/etc/collectd/collectd.conf'

    dest_dir = os.path.dirname(dest)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    shutil.move('/etc/collectd.conf', dest)

    return 0


def start_metrics():
    return call_distro_fn()


def start_metrics_arch():
    # restart because the collectd service is presumably already installed
    # and we're restarting it so it loads our config.
    command = ('/usr/bin/systemctl', 'restart', 'collectd')

    return run_command(command)


def start_metrics_raspbian():
    # restart because the collectd service is presumably already installed
    # and we're restarting it so it loads our config.
    command = ('/etc/init.d/collectd', 'restart')

    return run_command(command)


def start_service():
    return call_distro_fn()


def start_service_arch():
    command = ('/usr/bin/systemctl', 'start', 'zymbit')

    return run_command(command)


def start_service_raspbian():
    script_dir = os.path.dirname(config.INIT_SCRIPT_PATH)
    command = ('/usr/bin/supervise', script_dir)

    return run_command(command)
