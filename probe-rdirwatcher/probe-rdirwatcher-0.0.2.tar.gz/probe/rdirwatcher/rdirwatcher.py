import paramiko
import logging
import logging.config
import time
import re
import pkg_resources

logging_cfg_path = pkg_resources.resource_filename(__name__, 'cfg/rdirwatcher_logging.cfg')
logging.config.fileConfig(logging_cfg_path)
logger = logging.getLogger(__name__)

class RDirWatcher(object):

    def __init__(self, cfg):
        self.key = paramiko.RSAKey.from_private_key_file(cfg['pkey_file'])
        self.hostname = cfg['hostname']
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
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_system_host_keys()
        ssh.connect(self.hostname, self.port, pkey=self.key)

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
                    comps = self.get_comps_in_file(filename, ssh)

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
