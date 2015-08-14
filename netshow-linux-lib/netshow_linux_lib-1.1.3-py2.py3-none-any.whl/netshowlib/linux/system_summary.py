# http://pylint-messages.wikidot.com/all-codes
# disable too few public methods message
# pylint: disable=R0903
"""
System Overview:  Uptime, OS Distribution and CPU Architecture
"""
from netshowlib.linux import common
import platform
import io


class SystemSummary(object):
    """
    Class provides some details regarding the system OS

    * **uptime**: uptime of the linux device
    * **arch**: CPU architecture
    * **version**: OS Distribution Version
    * **os_name**: OS Distribution Name
    * **os_build**: OS Build number if available.
    """

    def __init__(self):
        self.lsb_release_loc = '/etc/lsb-release'
        self.arch = None
        self._uptime = None
        self.os_name = None
        self.os_version = None
        self.os_build = None
        self.version = None

    def run(self):
        try:
            self.parse_lsb_release_exec()
        except common.ExecCommandException:
            # only works on debian based systems
            self.parse_lsb_release_file()
        self.arch = platform.machine()
        self._uptime = None

    def parse_lsb_release_file(self):
        """
        parse  /etc/lsb/file
        DISTRIB_ID="Cumulus Networks"
        DISTRIB_RELEASE=2.5.3
        DISTRIB_DESCRIPTION=2.5.3-c4e83ad-201506011818-build
        """
        try:
            lsb_output = io.open(self.lsb_release_loc, 'r').read()
        except IOError:
            return

        fileio = io.StringIO(lsb_output)
        for _line in fileio:
            _line = _line.strip()
            if _line.startswith('DISTRIB_ID'):
                self.os_name = _line.split('=')[1]
            elif _line.startswith('DISTRIB_RELEASE'):
                self.version = _line.split('=')[1]
            elif _line.startswith('DISTRIB_DESCRIPTION'):
                self.os_build = _line.split('=')[1]

    def parse_lsb_release_exec(self):
        """
        parse lsb release exec
        """
        lsb_output = common.exec_command('/usr/bin/lsb_release -a')
        for _line in lsb_output.split('\n'):
            if _line.startswith('Distributor'):
                self.os_name = _line.split()[2]
            elif _line.startswith('Description'):
                self.os_build = _line.split(':')[1].strip()
            elif _line.startswith('Release'):
                self.version = _line.split(':')[1].strip()

    @property
    def uptime(self):
        """
        :return: uptime of the linux device in seconds
        """
        filepath = '/proc/uptime'
        uptime = common.read_file_oneline(filepath)
        self._uptime = uptime.split()[0]
        return self._uptime
