from setuptools import setup, find_packages


setup(
  name='blahblah',
  version='0.5.4',
  description='Fake data generator for district42 schema',
  url='https://github.com/nikitanovosibirsk/blahblah',
  author='Nikita Tsvetkov',
  author_email='nikitanovosibirsk@yandex.com',
  license='MIT',
  packages=find_packages(),
  install_requires=[
    'district42==0.5.4',
    'exrex==0.9.3'
  ]
)
