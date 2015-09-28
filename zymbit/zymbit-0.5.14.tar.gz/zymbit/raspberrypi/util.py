from zymbit.linux.util import *


def get_distro():
    distro = None

    issue_path = '/etc/issue'
    if os.path.exists(issue_path):
        with open(issue_path, 'rb') as fh:
            content = fh.read().lower()
            for _distro in ('raspbian', 'arch'):
                if _distro in content:
                    distro = _distro
                    break

    return distro
