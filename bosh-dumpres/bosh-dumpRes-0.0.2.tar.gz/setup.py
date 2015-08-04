from setuptools import setup, find_packages

setup(
    name='bosh-dumpRes',
    version='0.0.2',
    packages=find_packages(),

    install_requires=[
	'requests',
        'openpyxl'
    ],

    author='MacroData Inc',
    author_email='info@macrodatalab.com',
    description='dump BigObject query result as a file',
    license='Apache 2.0',
    keywords=[
        'bigobject',
        'macrodata',
        'dump',
        'command line tool',
	'CSV',
	'XLSX',
    ],
    url='https://github.com/macrodatalab/dumpRes.git',

    zip_safe=False
)
