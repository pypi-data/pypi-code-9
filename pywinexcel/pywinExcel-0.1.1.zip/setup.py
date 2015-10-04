from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='pywinExcel',
      version='0.1.1',
      description='Python API to Excel ',
	  keywords='python windows MsExcel Excel',
	  classifiers=[
        'Development Status :: 3 - Alpha',
		'Operating System :: Microsoft :: Windows',
        'Environment :: Win32 (MS Windows)',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      author='Tan Kok Hua',
      author_email='kokhua81@gmail.com',
	  url = 'https://github.com/spidezad/pywinexcel',
      packages=['pywinexcel'],
      zip_safe=False)