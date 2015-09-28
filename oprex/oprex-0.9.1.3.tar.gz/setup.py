from distutils.core import setup

setup(
    name='oprex',
    packages = ['oprex'],
    version='0.9.1.3',
    author='Ron Panduwana',
    author_email='panduwana@gmail.com',
    include_package_data=True,
    url='https://github.com/rooney/oprex',
    download_url='https://github.com/rooney/oprex/tarball/0.9.2',
    license='LICENSE',
    description='Regex alternative syntax. Make regex readable.',
	keywords = ['regex'],
	classifiers = ['Development Status :: 4 - Beta'],
    install_requires=[
		'ply>=3.4',
		'regex==2015.7.19',
    ],
)
