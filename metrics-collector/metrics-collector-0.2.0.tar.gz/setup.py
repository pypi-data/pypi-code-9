from setuptools import setup

setup(name='metrics-collector',
	version='0.2.0',
	author='Jia Mengchi',
	author_email='jiam@garena.com',
	description="System monitoring daemon that logs to InfluxDB",
	url="http://git.garena.com/core-services/metrics_collector",
	packages=['metrics_collector', 'metrics_collector.collectors', 'metrics_collector.common'],
	install_requires=[
		'psutil>=3.0.1',
		'docopt',
		'influxdb>=2.9.1',
		'raven>=5.3.1',
		'importlib>=1.0.3',
	],
	entry_points={'console_scripts': ['metrics_collector = metrics_collector.main:main']},
	data_files=[
		('/etc/metrics_collector', ['config.ini']),
		('/var/run/metrics_collector', []),
		('/var/log/metrics_collector', [])
	]
)
