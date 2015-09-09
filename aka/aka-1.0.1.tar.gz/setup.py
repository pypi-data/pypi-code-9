from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='aka',
      version='1.0.1',
      description='Rename/copy files using Python code',
      long_description=readme(),
      url='https://notabug.org/Uglemat/aka',
      scripts = ['scripts/aka'],
      author='Mattias Ugelvik',
      author_email='uglemat@gmail.com',
      license='GPL3+',
      packages=['aka'],
      install_requires=['contex'],
      classifiers=[
          'Environment :: Console',
          'Intended Audience :: System Administrators',
          'Intended Audience :: Developers',
          'Intended Audience :: End Users/Desktop',
          'Topic :: System :: Systems Administration',
          'Topic :: Utilities',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Programming Language :: Python :: 3',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      package_data={
          'readme': ['README.rst'],
      },
      include_package_data=True,
      zip_safe=False)
