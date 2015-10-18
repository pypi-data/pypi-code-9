import paramiko
import logging
import logging.config
import time
import re

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler)

class RDirWatcher(object):

    def __init__(self, cfg):
        logger.debug('cfg: %s', repr(cfg))
        self.key = paramiko.RSAKey.from_private_key_file(cfg['pkey_file'])
        self.hostnames = cfg['hostnames']
        self.port = 22
        self.username = cfg['username']
        self.watch_dir = cfg['watch_dir']
        self.watch_pattern = cfg['watch_pattern']
        self.watch_pattern_compile = re.compile(self.watch_pattern)
        self.watch_max_age = cfg['watch_max_age']

    @staticmethod
    def check_stderr(cmd, stderr):
        stderr = stderr.readlines()
        logger.debug('cmd: {}, stderr: {}'.format(cmd, stderr))
        if stderr != []:
            raise CmdError(cmd, stderr)

    def check(self):

        comps = set()
        for hostname in self.hostnames:
            logger.info('checking hostname %s', hostname)

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.load_system_host_keys()
            ssh.connect(hostname, self.port, pkey=self.key)

            cmd = 'ls {}'.format(self.watch_dir)
            _, stdout, stderr = ssh.exec_command(cmd)
            self.check_stderr(cmd, stderr)

            for line in stdout:
                filename = line.strip()
                logger.debug('filename: {}'.format(filename))

                if self.watch_pattern_compile.match(filename):
                    logger.info('file match: {}'.format(filename))

                    delta_secs = self.get_last_modification_of_file(filename, ssh)
                    if delta_secs < self.watch_max_age:
                        comps_in_file = self.get_comps_in_file(filename, ssh)
                        logger.debug('comps_in_file: %s', comps_in_file)
                        comps = comps.union(set(comps_in_file))

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
        logger.debug('cmd_stat: {}'.format(cmd))
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
