import os
import re

from subprocess import PIPE, Popen

CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_ID_RE = re.compile(r'(?P<device>\w+).* HWaddr (?P<mac>[0-9a-fA-F:]+).*')
MAC_CLIENT_ID_RE = re.compile(r'(?P<device>\w+): .*')
MAC_MAC_RE = re.compile(r'\s+ether (?P<mac>[0-9a-fA-F:]+).*')

IGNORED_DEVICES = (
    'docker0',
)

def get_output(command):
    proc = Popen(command, stdout=PIPE)

    return proc.communicate()[0].splitlines()


def get_client_id():
    global CLIENT_ID

    if CLIENT_ID:
        return CLIENT_ID

    devices = {}

    _device_name = None

    lines = get_output('/sbin/ifconfig')
    for line in lines:
        matches = CLIENT_ID_RE.match(line)
        if matches:
            t = matches.groupdict()
            devices[t['device']] = t['mac']
            continue

        matches = MAC_CLIENT_ID_RE.match(line)
        if matches:
            _device_name = matches.group('device')
            continue

        matches = MAC_MAC_RE.match(line)
        if matches and _device_name and _device_name not in IGNORED_DEVICES:
            devices[_device_name] = matches.group('mac')
            _device_name = None

    if not devices:
        raise Exception('Unable to find client ID')

    if 'eth0' in devices:
        CLIENT_ID = devices['eth0']
    elif 'en0' in devices:
        CLIENT_ID = devices['en0']
    else:
        CLIENT_ID = devices.values()[0]

    return CLIENT_ID


if __name__ == '__main__':
    print get_client_id()
