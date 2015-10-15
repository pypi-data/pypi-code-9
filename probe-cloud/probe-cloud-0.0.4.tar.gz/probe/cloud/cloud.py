from probe.rdirwatcher import RDirWatcher
import logging
import subprocess
from multiprocessing import Process, Pipe
import time
import socket
import psutil
from psutil import NoSuchProcess, AccessDenied
from ConfigParser import SafeConfigParser
import sys, os

logger = logging.getLogger()
logger.addHandler(logging.NullHandler)

def run_cmd(pipe, cmd, stdout=None):
    '''
    This function starts a Popen process with specified command. Command has to be
    list of individual arguments (example: cmd = ['cat', 'a.out']). Note that stderr
    is automatically redirected to stdout. Stdout is by default printed to the screen,
    but can be redirected somewhere else. To do that, use `stdout` kwarg (it can be
    unix file descriptor or python file object). Pipe argument is a duplex, immediatelly
    after the command is executed, it's pid is send using duplex to the parent process
    (process that called this function).

    Args:
        pipe        duplex
        cmd         command to be executed
    Kwargs:
        stdout      where to redirect stdout from the command
    '''
    try:
        logger.info('CHILD: starting simulation with cmd: %s', cmd)
        sim = subprocess.Popen(cmd, stdout=stdout, stderr=subprocess.STDOUT)
        # send sim id to parent
        logger.info('CHILD: sim.pid: %s', sim.pid)
        pipe.send(sim.pid)
        sim.wait()
    except Exception as e:
        logger.exception('CHILD: Exception: %s', e)
        raise

class Cloud(object):

    def __init__(self, cfg):
        logger.debug('initializing Cloud object')
        logger.debug('cfg: %s', cfg)
        self.cfg = self.get_config(cfg)
        logger.debug('self.cfg: %s', self.cfg)
        self.rdirwatcher = RDirWatcher(cfg)
        sys.exit(0)

    def check(self):
        logger.info('going to check')
        comps = self.rdirwatcher.check()
        logger.debug('checked, comps: %s', comps)
        return comps

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

        #command to be executed
        opt_cmd = parser.get('watch', 'cmd')
        opt_cmd = [it.strip() for it in opt_cmd.split(',')]

        return {
            'pkey_file' : opt_pkey_file,
            'hostnames' : opt_hostnames,
            'username' : opt_username,
            'watch_dir' : opt_watch_dir,
            'watch_pattern' : opt_watch_pattern,
            'watch_max_age' : opt_watch_max_age,
            'cmd': opt_cmd,
        }

    def run_simulation(self):

        parent_conn, child_conn = Pipe()
        simulation = Process(target=run_cmd, args=(child_conn, self.cfg['cmd']))
        simulation.start()
        sim_pid = parent_conn.recv()
        logger.info('PAREND: child.pid: %s', simulation.pid)
        logger.info('PARENT: sim.pid: %s', sim_pid)

        # hostname of this computer
        hostname = socket.gethostname()
        logger.info('PARENT: hostname: %s', hostname)
        simulation = psutil.Process(sim_pid)
        logger.info('PARENT: simulation: %s', simulation)

        is_simulation_suspended = False

        while True:
            logger.info('PARENT: going to check computers')
            comps = self.check()
            logger.info('checked: %s', comps)

            if hostname in comps and not is_simulation_suspended:
                logger.info('suspending simulation')
                try:
                    simulation.suspend()
                    is_simulation_suspended = True
                except NoSuchProcess as e:
                    logger.exception('PARENT: NoSuchProces Exception, e: %s', e)
                except AccessDenied as e:
                    logger.exception('PARENT: AccessDenied Exception, e: %s', e)

            if hostname not in comps and is_simulation_suspended:
                logger.info('resuming simulation')
                try:
                    simulation.resume()
                except NoSuchProcess as e:
                    logger.exception('PARENT: NoSuchProces Exception, e: %s', e)
                except AccessDenied as e:
                    logger.exception('PARENT: AccessDenied Exception, e: %s', e)

                is_simulation_suspended = False

            time.sleep(5)

