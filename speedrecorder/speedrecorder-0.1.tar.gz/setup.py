from setuptools import setup,find_packages
setup(
    name = 'speedrecorder',
    url = 'https://github.com/rweyant/speedtest-cli',
    description='A function that records your internet speed',
    version = '0.1',
    packages = find_packages(),
    install_requires=[
    'ipgetter',
    'requests']
)
