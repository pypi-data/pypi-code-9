from setuptools import setup, find_packages


setup(
  name='blahblah',
  packages=find_packages(),
  version='0.5.2',
  description='Fake data generator for district42 schema',
  url='https://github.com/nikitanovosibirsk/blahblah',
  author='Nikita Tsvetkov',
  author_email='nikitanovosibirsk@yandex.com',
  license='MIT',
  install_requires=[
    'district42==0.5.2'
  ]
)
