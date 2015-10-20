from setuptools import setup

setup(
	name='rtq',
	version = '1.0',
	scripts=['rtqinfo.py'],
	install_requires=['yahoo_finance', 'BeautifulSoup', 'argparse', 'urllib3'])
 


