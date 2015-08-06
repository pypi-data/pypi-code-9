from setuptools import setup

def readme():
	with open('README.md') as f:
		return f.read()

setup(name='janeliasig',
      version='0.93',
      description='Rudimentary Simulations/Manipulations of PMT Outputs',
      long_description = readme(),
      classifiers = [
      'Development Status :: 3 - Alpha',
      'License :: OSI Approved :: MIT License',
      'Natural Language :: English',
      'Programming Language :: Python :: 2.7',
      'Topic :: Scientific/Engineering :: Information Analysis'],
      url='http://github.com/SpenceyHong/janeliasig',
      author='Spencer Hong',
      author_email='spencer.hongx@gmail.com',
      license='MIT',
      packages=['janeliasig'],
      install_requires=[
      'matplotlib',
      'numpy',
      'scipy',
      'sklearn'
      ],
      include_package_data = True,
      zip_safe=False)
