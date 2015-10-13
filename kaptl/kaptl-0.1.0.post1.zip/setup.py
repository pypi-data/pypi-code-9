try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='kaptl',
    version='0.1.0.post1',
    packages=['app'],
    url='',
    license='MIT',
    author='Stanislav Demchuk',
    author_email='stas@8sph.com',
    description='KAPTL generator CLI',
    install_requires=[
        'docopt==0.6.1',
        'requests==2.8.0',
        'pyprind==2.9.2',
        'autoupgrade==0.2.0'
    ],
    entry_points={
        'console_scripts': ['kaptl=app.main:main']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
)
