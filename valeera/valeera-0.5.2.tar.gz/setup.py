from setuptools import setup, find_packages


setup(
  name='valeera',
  packages=find_packages(),
  version='0.5.2',
  description='Validator for district42 schema',
  url='https://github.com/nikitanovosibirsk/valeera',
  author='Nikita Tsvetkov',
  author_email='nikitanovosibirsk@yandex.com',
  license='MIT',
  install_requires=[
    'district42==0.5.2'
  ]
)
