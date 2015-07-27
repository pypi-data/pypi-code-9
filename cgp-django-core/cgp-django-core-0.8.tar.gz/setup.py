from setuptools import setup, find_packages

setup(
    name = 'cgp-django-core',
    packages = ['base_account', 'base_media', 'base_page', 'form', 'monomail', 'sharing', 'site_admin', 'tracking'],
    version = '0.8',
    description = 'Core CGP Django Libraries',
    author = 'Nina Pavlich',
    author_email='nina@cgparntersllc.com',
    url = 'https://bitbucket.org/cgpartners/cgp-django-core',
    keywords = ['libraries', 'web development'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ]
)