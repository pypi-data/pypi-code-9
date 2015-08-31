from setuptools import setup, find_packages

setup(
    name='bosh-db2bt',
    version='0.0.5',
    packages=find_packages(),

    install_requires=[
	'requests',
	'PyMySQL',
    ],

    author='MacroData Inc',
    author_email='info@macrodatalab.com',
    description='copy mysql/postgresql tables to BigObject server',
    license='Apache 2.0',
    keywords=[
        'bigobject',
        'macrodata',
        'database',
        'command line tool',
	'mysql',
	'postgresql',
    ],
    url='https://github.com/macrodatalab/db2bt.git',

    zip_safe=False
)
