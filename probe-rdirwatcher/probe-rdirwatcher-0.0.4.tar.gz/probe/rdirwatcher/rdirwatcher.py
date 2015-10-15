import os
import paramiko
import logging
import logging.config
import time
import re
from ConfigParser import SafeConfigParser

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler)

class RDirWatcher(object):

    def __init__(self, cfg_path):
        cfg = self.get_config(cfg_path)
        logger.debug('cfg: %s', repr(cfg))
        self.key = paramiko.RSAKey.from_private_key_file(cfg['pkey_file'])
        self.hostnames = cfg['hostnames']
        self.port = 22
        self.username = cfg['username']
        self.watch_dir = cfg['watch_dir']
        self.watch_pattern = cfg['watch_pattern']
        self.watch_pattern_compile = re.compile(self.watch_pattern)
        self.watch_max_age = cfg['watch_max_age']

    def get_config(self, cfg_path):

        parser = SafeConfigParser()
        parser.read(cfg_path)

        #pkey_file
        opt_pkey_file = '{}/.ssh/id_rsa'.format(os.environ['HOME'])
        if parser.has_option('ssh', 'pkey_file'):
            opt_pkey_file = parser.get('ssh', 'pkey_file')

        #hostnames
        opt_hostname = parser.get('ssh', 'hostnames', None)
        if opt_hostname is not None:
            opt_hostnames = opt_hostname.split(',')
            opt_hostnames = [hostname.strip() for hostname in opt_hostnames]

        #username
        opt_username = os.environ['USER']
        if parser.has_option('ssh', 'username'):
            opt_username = parser.get('ssh', 'username')

        #watch_dir
        opt_watch_dir = None
        if parser.has_option('watch', 'watch_dir'):
            opt_watch_dir = parser.get('watch', 'watch_dir')
        if opt_watch_dir is None:
            opt_watch_dir = '/tmp'

        #watch_pattern
        opt_watch_pattern = parser.get('watch', 'watch_pattern')

        #watch_max_age
        opt_watch_max_age = float(parser.get('watch', 'watch_max_age'))

        return {
            'pkey_file' : opt_pkey_file,
            'hostnames' : opt_hostnames,
            'username' : opt_username,
            'watch_dir' : opt_watch_dir,
            'watch_pattern' : opt_watch_pattern,
            'watch_max_age' : opt_watch_max_age,
        }

    @staticmethod
    def check_stderr(cmd, stderr):
        stderr = stderr.readlines()
        logger.debug('cmd: {}, stderr: {}'.format(cmd, stderr))
        if stderr != []:
            raise CmdError(cmd, stderr)

    def check(self):

        comps = set()
        for hostname in self.hostnames:

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.load_system_host_keys()
            ssh.connect(hostname, self.port, pkey=self.key)

            cmd = 'ls {}'.format(self.watch_dir)
            _, stdout, stderr = ssh.exec_command(cmd)
            self.check_stderr(cmd, stderr)

            comps = None
            for line in stdout:
                filename = line.strip()
                logger.debug('filename: {}'.format(filename))

                if self.watch_pattern_compile.match(filename):
                    logger.info('file match: {}'.format(filename))

                    delta_secs = self.get_last_modification_of_file(filename, ssh)
                    if delta_secs < self.watch_max_age:
                        comps.union(set(self.get_comps_in_file(filename, ssh)))

            ssh.close()

        return comps

    def get_comps_in_file(self, filename, ssh):
        cmd = 'cat {}/{}'.format(self.watch_dir, filename)
        logger.debug('cmd_cat: {}'.format(cmd))
        _, stdout, stderr = ssh.exec_command(cmd)
        self.check_stderr(cmd, stderr)

        comps = list()
        for line_cat in stdout:
            comp = line_cat.strip()
            logger.debug('computer: {}'.format(comp))
            comps.append(comp)

        return comps

    def get_last_modification_of_file(self, filename, ssh):
        # %Y returns time of last modification of the file as seconds
        # since epoch
        cmd = 'stat --format "%Y" {}/{}'.format(self.watch_dir, filename)
        logger.info('cmd_stat: {}'.format(cmd))
        _, stdout, stderr = ssh.exec_command(cmd)
        self.check_stderr(cmd, stderr)

        line_stat = stdout.readline()
        logger.debug('line_stat: {}'.format(line_stat))

        last_modification_secs = float(line_stat.strip())
        logger.debug('last_modification_secs: {}'.format(last_modification_secs))

        now_secs = time.time()
        logger.debug('now_secs: {}'.format(now_secs))

        delta_secs = now_secs - last_modification_secs
        logger.info('seconds since last modification: {}'.format(delta_secs))

        return delta_secs


class CmdError(Exception):

    def __init__(self, cmd, stderr):
        Exception.__init__(self)
        self.cmd = cmd
        self.stderr = stderr

    def __str__(self):
        'CmdError: Cmd: {}, stderr: {}'.format(self.cmd, self.stderr)
