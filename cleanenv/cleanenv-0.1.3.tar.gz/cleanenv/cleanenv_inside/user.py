# FIXME 'id -Gn' lists somewhat more when special network groups are used.
import grp
import os
import pwd
import re


_pattern       = r'(system:)?(?:(\d+)?:)?([^:]+)?$'

# see http://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap03.html#tag_03_278
_safe_usergroup_char = r'a-zA-Z0-9._-'


def _posix_name(name):
    """Convert a username/groupname into a posix compliant name.
    """
    if len(name) >= 32:
        name = name[:32]
    return re.sub(r'[^%s]' % _safe_usergroup_char, '_', name)


def _group_item(group):
    gr_name = _posix_name(group.gr_name)

    item = {'gid': group.gr_gid, 'name': gr_name}
    if gr_name != group.gr_name:
        item['comment'] = group.gr_name
    return item


def _groups(username):
    result = []

    try:
        group = grp.getgrnam(username)
        result.append(_group_item(group))
    except KeyError:
        pass

    for group in grp.getgrall():
        for member in group.gr_mem:
            if member == username or member.endswith('+' + username):
                result.append(_group_item(group))

    return result


def username_from_config(config):
    value = config['global'].get('user')
    if not value:
        return None
    match = re.match(_pattern, value)
    if not match:
        return None
    return match.group(3)


def expand_user(config):
    """Detect username, userid and its associated groups (including group ids)
    from the user in config['global']['user']. If none is set, the current
    logged in user is used.

    Returns a dictionary with 'uid', 'name', 'system' flag and its 'groups'.
    """
    user = config['global'].get('user')

    match = re.match(_pattern, user)
    if not match:
        raise ValueError('Invalid user: %s' % user)

    sudo     = config['global'].get('sudo', False)
    system   = bool(match.group(1))
    gid      = match.group(2)
    username = match.group(3)

    if not username:
        username = getlogin()

    if gid:
        userid = int(gid)
    else:
        try:
            userid = pwd.getpwnam(username).pw_uid
        except KeyError:
            # no such user
            userid = None

    groups = _groups(username)

    fixed_username = _posix_name(username)
    result = {
        'name': fixed_username,
        'uid': userid,
        'system': system,
        'sudo': sudo,
        'groups': groups}

    if fixed_username != username:
        result['comment'] = username

    return result


def getlogin():
    # os.getlogin() is not always working properly on all systems
    return pwd.getpwuid(getuid()).pw_name

def getuid():
    return os.geteuid()
