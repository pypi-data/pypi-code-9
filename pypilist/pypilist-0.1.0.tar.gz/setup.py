from setuptools import setup

setup(name='pypilist',
    description='list pypi packages',
    version='0.1.0',
    author='Harsha Srinivas',
    author_email='95harsha95@gmail.com',
    packages=['pypilist'],
    package_data={
        "pypilist": ["packages.json"],
    },
    include_package_data=True,
    entry_points={
        'console_scripts': ['pypilist=pypilist:show'],
    },
    url='https://github.com/harshasrinivas/pypilist/',
    keywords=[ 'CLI', 'python'],
    install_requires=['future'],
    classifiers=[
        'Operating System :: POSIX',
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules',
  ],)
