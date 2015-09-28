from setuptools import setup

setup(name='batchly_sdk',
      version='0.2.3',
      description='Service provider interface for the batchly processor system',
      url='http://www.batchly.net',
      author='Batchly Support',
      author_email='support@batchly.net',
      license='Proprietary',
      packages=['batchly_sdk', 'batchly_sdk.request', 'batchly_sdk.response'],
      zip_safe=False,
      keywords='batchly processor sdk')
