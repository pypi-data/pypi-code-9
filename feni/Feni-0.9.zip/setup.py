from setuptools import setup, find_packages

setup(
    name = "Feni",
    description='A simple static site generator.',
    url='http://bitbucket.org/sras/feni',
    author='Sandeep.C.R',
    author_email='sandeepcr2@gmail.com',
    license='MIT',
    version = "0.9",
    packages = ['feni'],
    entry_points = {
        "console_scripts":['feni=feni.feni:main']
    },
    install_requires=[
      'lesscpy',
      'markdown',
      'pyyaml'
    ]
)
