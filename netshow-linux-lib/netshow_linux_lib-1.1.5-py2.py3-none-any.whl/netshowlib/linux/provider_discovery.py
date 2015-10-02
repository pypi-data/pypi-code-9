"""
This modules run a OS discovery check for Linux
"""

try:
    import netshowlib.linux.common as common_mod
except ImportError:
    common_mod = None


def check():
    """
    Linux Provider Check
    :return: name of OS found if check is true
    """

    # if netshowlib.linux.common module is not found..return None
    if not common_mod:
        return None
    try:
        uname_output = common_mod.exec_command('/bin/uname')
    except common_mod.ExecCommandException:
        return None
    os_name = uname_output.decode('utf-8').strip()
    os_name = os_name.lower()
    if os_name == 'linux':
        return os_name
    return None


def name_and_priority():
    """
    name and priority for Linux provider
    name = Linux
    priority = 0. Lower priority means less likely candidate
    """
    os_name = check()
    if os_name:
        return {os_name: '0'}
    return None
