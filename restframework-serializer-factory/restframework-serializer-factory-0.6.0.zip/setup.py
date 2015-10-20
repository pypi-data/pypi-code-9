from distutils.core import setup

from setuptools import find_packages



setup(name='restframework-serializer-factory',
      version="0.6.0",
      packages=find_packages(),
      requires=['djangorestframework'],
      install_requires=['djangorestframework'],
      tests_require=[
          'Django>=1.5',
          ],
      url='https://github.com/arpheno/django-rest-framework-serializer-factory/',
      author='Sebastian Wozny',
      author_email='sswozny@gmail.com',
      keywords='django serializer factory rest framework',
      description=('Factories for creating instances of restframework.serializers.ModelSerializer on demand.',),
      license='GPL',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Framework :: Django',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Natural Language :: English',
          ('License :: OSI Approved :: '
           'GNU General Public License v3 or later (GPLv3+)'),
          'Topic :: Software Development :: Libraries',
          ],
      )
