# Python 2/3 support for loading ConfigParser
try:
	import configparser
except ImportError:
	import ConfigParser as configparser

import socket

DEBUG = False

LOGGER_CONFIG = {
	'log_dir': '',
	'sentry_dsn': ''
}

class DaemonConfig(object):
	""" The configuration container for the daemon """

	def __init__(self, path):
		""" Create a new daemon configuration context """

		parser = configparser.RawConfigParser()
		parser.read(path)

		#daemon config
		self.pid_file_path = parser.get('Daemon', 'PidFile') or '/var/run/garena_metrics_collector/daemon.pid'
		self.daemon_log_path = parser.get('Daemon', 'LogPath') or '/var/run/garena_metrics_collector/daemon.log'

		#log config
		LOGGER_CONFIG['sentry_dsn'] = parser.get('Log', 'SentryDSN')
		LOGGER_CONFIG['log_dir'] = parser.get('Log', 'LogDir') or '/var/run/garena_metrics_collector/log'
		from common.logger import init_logger
		init_logger(**LOGGER_CONFIG)

		# Configuration options specific to interacting with InfluxDB
		self.influxdb = {
			# Get server connection info
			'host': parser.get('InfluxDB', 'Host') or '127.0.0.1',
			'port': parser.get('InfluxDB', 'Port') or 8086,
			'database': parser.get('InfluxDB', 'Database') or None,

			# Get authentication info
			'user': parser.get('InfluxDB', 'User') or None,
			'pass': parser.get('InfluxDB', 'Pass') or None
		}

		# Configuration options for controlling collection and the daemon
		self.metrics_collector = {
			# Get hostname override (if set)
			'hostname': parser.get('MetricsCollector', 'Hostname') or socket.gethostname(),

			'collectors': parser.get('MetricsCollector', 'Collectors').split(',') or None,
		}

		if self.metrics_collector['collectors'] is None:
			raise Exception("A list of collectors MUST be provided.")

		if self.influxdb['user'] is None and self.influxdb['pass'] is None:
			raise Exception("A username and password must be provided.")
