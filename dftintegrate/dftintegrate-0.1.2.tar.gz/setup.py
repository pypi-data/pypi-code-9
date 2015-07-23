#!/usr/bin/env python3


from setuptools import setup

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, "
          "could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(name='dftintegrate',
      version='0.1.2',
      description='Integrate DFT data',
      long_description=read_md('README.md'),
      author='Matthew M Burbidge',
      author_email='mmburbidge@gmail.com',
      url='https://github.com/mmb90/dftintegrate',
      license='MIT',
      install_requires=[
          "argparse",
          "termcolor",
          "numpy",
          "matplotlib",
          "scipy",
      ],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Science/Research',
          'Natural Language :: English',
          'License :: OSI Approved :: MIT License',
          'Operating System :: MacOS',
          'Programming Language :: Python :: 3.4',
          'Topic :: Scientific/Engineering :: Information Analysis'],
      entry_points={
          'console_scripts': [
              'dftintegrate = dftintegrate.main:main']},
      packages=['dftintegrate', 'dftintegrate.fourier'],
      scripts=['dftintegrate/main.py'],
      package_data={},
      include_package_data=True)
