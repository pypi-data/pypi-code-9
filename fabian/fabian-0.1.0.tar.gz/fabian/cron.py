# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re
import io

from fabric.api import put, settings, sudo


"""
CRON DOCUMENTATION FROM THE DEBIAN MAN PAGE REASONING OUR LOCATION CHOICES:
Support  for /etc/cron.hourly, /etc/cron.daily, /etc/cron.weekly and
 /etc/cron.monthly is provided in Debian through the default setting
 of the /etc/crontab file (see the system-wide example in crontab(5)).
 The default system-wide crontab contains four tasks: run every hour,
 every  day,  every  week  and  every month.  Each  of  these  tasks
 will execute run-parts providing each one of the directories as an
 argument. These tasks are disabled if anacron is installed (except
 for the hourly task) to prevent conflicts between both daemons.
 As described above, the files under these directories have to be pass
 some sanity checks including the following: be executable, be owned by
 root,  not  be writable  by  group  or other and, if symlinks, point
 to files owned by root. Additionally, the file names must conform to
 the filename requirements of run-parts: they must be entirely made up
 of letters, digits and can only contain the special signs underscores
 ('_') and hyphens ('-'). Any file that  does  not conform  to these
 requirements will not be executed by run-parts.  For example, any file
 containing dots will be ignored.  This is done to prevent cron from
 running any of the files that are left by the Debian package management
 system when handling files in /etc/cron.d/ as configuration files
 (i.e. files ending in .dpkg-dist, .dpkg-orig, and .dpkg-new).


This  feature  can  be used by system administrators and packages to include
tasks that will be run at defined intervals. Files created by packages in these
directories should be named after the package that supplies them.

"""

CRONTAB_LOCATIONS = {
    'hourly': '/etc/cron.hourly',
    'daily': '/etc/cron.daily',
    'weekly': '/etc/cron.weekly',
    'monthly': '/etc/cron.monthly',
}


def crontab(func, basename, frequency='daily', **kwargs):
    """
    Install a script into the system package crontab whose body is returned
    from the call ``func(**kwargs)``, The script will be run with the
    frequency ``frequency`` (one of 'hourly', 'daily', 'weekly', 'monthly').
    ``basename`` will be used as the filename name for the script file.
    The script returned by ``func(**args)`` must have a valid shebang.
    """
    script = func(**kwargs)
    if not script.startswith('#!/'):
        raise ValueError("script has no shebang")

    try:
        name = re.match('^[\w\d_-]*$', basename).group()
    except AttributeError:
        raise ValueError("invalid script name")

    path = '%s/%s' % (CRONTAB_LOCATIONS[frequency], name)
    #override any overridden env
    with settings(sudo_user='root'):
        put(
            io.StringIO(script),
            remote_path=path,
            use_sudo=True,
            mode=0500,
        )

        # scripts in /etc/cron.* must be owned by root.
        sudo('chown root:root %s' % path)
