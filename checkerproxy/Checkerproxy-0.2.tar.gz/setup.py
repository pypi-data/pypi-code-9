from setuptools import setup

setup(name='Checkerproxy',
      version='0.2',
      description='Get active proxies from checkerproxy.net',
      url='https://github.com/MorrisCasper/Checkerproxy',
      author='MorrisCasper',
      author_email='',
      license='MIT',
      packages=['Checkerproxy'],
      install_requires=['requests',
                        'beautifulsoup4'],
      zip_safe=False)