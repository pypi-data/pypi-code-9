from setuptools import setup, find_packages

with open('requirements.txt') as fd:
    requires = fd.readlines()

with open('requirements.txt') as fd:
    setup(name='xpcs',
          author='Lars Kellogg-Stedman',
          author_email='lars@oddbit.com',
          url='https://github.com/larsks/xpcs',
          version='0.2',
          packages=find_packages(),
          install_requires=requires,
          entry_points={'console_scripts': ['xpcs = xpcs.main:cli',],})
