from distutils.core import setup
setup(
    name='oinkwall',
    packages=['oinkwall'],
    version='0.3.1a1',
    description='Python module for programmatically creating low level iptables rule sets.',
    author='Hans van Kranenburg',
    author_email='hans@knorrie.org',
    url='https://github.com/knorrie/python-oinkwall',
    download_url='https://github.com/knorrie/python-oinkwall/tarball/v0.3.1a1',
    keywords=['firewall', 'iptables', 'ipv6'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Topic :: System :: Systems Administration',
        'Topic :: System :: Networking',
    ],
)
