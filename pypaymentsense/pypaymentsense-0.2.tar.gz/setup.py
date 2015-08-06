from setuptools import setup, find_packages
setup(
	name='pypaymentsense',
	version='0.2',
	description='Python libary for payment sense hosted forms',
	url='https://github.com/crooksey/pyPaymentSense',
	author='Luke Crooks',
	author_email='luke@pumalo.org',
	license='MIT',

	keywords='paymentsense payment sense',
	install_requires=['pytz', 'requests'],
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 2.7'
	],

	packages=find_packages(),
	zip_safe=False,)