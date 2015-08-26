from setuptools import setup

setup(name='pnr',
      version='0.1',
      description='PNR CHECKER',
      url='https://github.com/vikas-parashar/django-project-generator',
      author='Akash Nimare',
      author_email='svnitakash@gmai.com',
      license='MIT',
      packages=['pnr'],
      entry_points = {
        'console_scripts': ['pnr=pnr.auto:main'],
        },
      install_requires=[
            'requests','BeautifulSoup'
      ],
      zip_safe=False)
