from setuptools import setup

requires = ['numpy', 'scipy', 'statsmodels', 'pandas', 'matplotlib', 'emcee', 'pymultinest', 'corner', 'astropy']

setup(name='fitting_utilities',
      version='0.1.0',
      description='Various useful classes for fitting stuff.',
      author='Kevin Gullikson',
      author_email='kevin.gullikson@gmail.com',
      license='MIT',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Topic :: Scientific/Engineering :: Astronomy',
      ],
      packages=['fitters'],
      install_requires=requires)
