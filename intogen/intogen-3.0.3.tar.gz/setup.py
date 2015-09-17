import sys

from setuptools import setup, find_packages
from intogen import __version__

if sys.hexversion < 0x03000000:
    raise RuntimeError('This package requires Python 3.0 or later.')

setup(
    name='intogen',
    version=__version__,
    packages=find_packages(),
    url='http://www.intogen.org',
    license='UPF Free Source Code',
    author='Biomedical Genomics Group',
    author_email='nuria.lopez@upf.edu',
    description='',
    install_requires=[
        'configobj >= 5.0.6',
        'drmaa >= 0.7.6',
        'ruffus >= 2.5',
        'numpy >= 1.9.0',
        'scipy >= 0.14.0',
        'pandas >= 0.15.2',
        'statsmodels >=0.6.0',
        'ago >= 0.0.6',
        'pyliftover >= 0.3',
        'networkx >= 1.10',
        'bgdata >= 0.6.0',
        'oncodrivefm >= 1.0.1',
        'oncodriveclust >= 1.0.0'
    ],
    include_package_data=True,
    package_data={'intogen': ['*.template']},
    scripts=[
        'bin/intogen'
    ],

    entry_points={
        'console_scripts': [
            'intogen-variants = intogen.tasks.variants:cmdline',
            'intogen-split = intogen.tasks.split:cmdline',
            'intogen-functional_impact = intogen.tasks.functional_impact:cmdline',
            'intogen-concat = intogen.tasks.concat:cmdline',
            'intogen-geneimpact = intogen.tasks.geneimpact:cmdline',
            'intogen-oncodrivefm = intogen.tasks.oncodrivefm:cmdline',
            'intogen-oncodriveclust = intogen.tasks.oncodriveclust:cmdline',
            'intogen-mutsigcv = intogen.tasks.mutsigcv:cmdline',
            'intogen-recurrences = intogen.tasks.recurrences:cmdline',
            'intogen-gene-results = intogen.tasks.gene_results:cmdline',
            'intogen-gene-combinations = intogen.tasks.gene_combinations:cmdline',
            'intogen-transcript-combinations = intogen.tasks.transcript_combinations:cmdline',
            'intogen-pool-drivers = intogen.tasks.pool_drivers:cmdline',
            'intogen-project-summary = intogen.tasks.project_summary:cmdline',
            'intogen-summary_combinations = intogen.tasks.summary_combinations:cmdline',
            'intogen-quality-control = intogen.qc.quality_control:cmdline'
        ]
    }

)
