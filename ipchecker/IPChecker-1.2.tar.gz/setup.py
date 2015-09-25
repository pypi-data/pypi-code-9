from  distutils.core import setup
setup(
	name="IPChecker",
	version="1.2",
	author = "Boumediene Kaddour",
	author_email="snboumediene@gmail.com",
	packages=["IPChecker"],
	scripts=[],
	url='http://pypi.python.org/pypi/IPchecker',
	license="LICENSE.txt",
	description="Check if an IPv4 is Private, Public, Multicats or Invalid",
	long_description=open('README.txt').read(),
	install_requires=[],)
