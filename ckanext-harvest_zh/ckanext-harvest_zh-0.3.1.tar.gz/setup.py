from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

version = '0.3.1'

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
	name='ckanext-harvest_zh',
	version=version,
	description="An improved harvest package to collect Chinese language data sets for CKAN. ",
	long_description=long_description,

	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='ckan, Linked-data, harvest',
	author='CKAN, Bing-Si Ni, Bo-Han Wu',
	url='https://dsp.im',
	license='MIT',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	# namespace_packages=['ckanext', 'ckanext.harvest'],
	include_package_data=True,
	zip_safe=False,
	install_requires=[
	        # dependencies are specified in pip-requirements.txt 
	        # instead of here
	],
	tests_require=[
		'nose',
		'mock',
	],
	test_suite = 'nose.collector',
	entry_points=\
	"""
    [ckan.plugins]
	# Add plugins here, eg
	harvest=ckanext.harvest.plugin:Harvest
	ckan_harvester=ckanext.harvest.harvesters:CKANHarvester
	dsp_ckan_harvester=ckanext.harvest.harvesters:DSPCKANHarvester
	tp_ckan_harvester=ckanext.harvest.harvesters:TaipeiHarvester
    [ckan.test_plugins]
	test_harvester=ckanext.harvest.tests.test_queue:TestHarvester
	test_action_harvester=ckanext.harvest.tests.test_action:MockHarvesterForActionTests
	[paste.paster_command]
	harvester = ckanext.harvest.commands.harvester:Harvester
    [babel.extractors]
    ckan = ckan.lib.extract:extract_ckan
	""",
    message_extractors={
        'ckanext': [
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('**/templates_new/**.html', 'ckan', None),
        ],
    }
)
