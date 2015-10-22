from setuptools import setup


setup(
    name='cts-smsteknik',
    version='1.0.6',
    description='Unofficial SMS Teknik client',
    url='http://cross-solutions.com',
    author='Cross Solutions',
    packages=['smsteknik'],
    license='ISC',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Topic :: Communications :: Telephony'

    ],
    entry_points={
        'console_scripts': [
            'smsteknik = smsteknik:main'
        ]
    }
)
