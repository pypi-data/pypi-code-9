"""
metrics_collector (InfluxDB System Monitoring Client) by Evan Darwin

Usage:
	metrics_collector [-h | --help] [--config=<config>] (start|stop|restart)

Options:
	-h --help	   Display this message
	-V --version	Display the application version
	-v --verbose	Display verbose logging information

	-d			  Detach and run as a daemon
	--dump		  Dumps the JSON data to be sent (warning: spammy!)
"""

VERSION = "0.1.0"

import os
import sys
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append('./')

from docopt import docopt
import config
from client import Worker
from common import daemon

def main():
	args = docopt(__doc__, version='metrics_collector version ' + VERSION)
	if args['--config']:
		config_path = args['--config']
	else:
		config_path = '/etc/metrics_collector/config.ini'
	cfg = config.DaemonConfig(os.path.abspath(config_path))
	worker = Worker(cfg)
	if config.DEBUG:
		worker.collect()
	else:
		client = daemon.Daemon(worker.collect, cfg.pid_file_path, cfg.daemon_log_path)
		if args['start']:
			client.start()
		elif args['stop']:
			client.stop()
		elif args['restart']:
			client.restart()
