from setuptools import setup

setup(name='lifecycle',
      version='0.6',
      description='Easily identify and track users with minimal code.',
      url='https://github.com/TeamLifecycle/lifecycle-python',
      author='Jake Mooney',
      author_email='jrmooney@gmail.com',
      license='MIT',
      packages=['lifecycle'],
      install_requires=[
          'unirest',
      ],
      zip_safe=False)
