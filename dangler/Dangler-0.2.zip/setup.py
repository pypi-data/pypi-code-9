from setuptools import setup

setup(
    name = "Dangler",
    description='A python script to convert html written with un-closed tags (like Hamlet templates) to html with closed tags.',
    url='http://bitbucket.org/sras/dangler',
    author='Sandeep.C.R',
    author_email='sandeepcr2@gmail.com',
    license='MIT',
    version = "0.2",
    packages = ['dangler'],
    entry_points = {
        "console_scripts":['dangler=dangler.dangler:main']
    },
    install_requires=[
      'beautifulsoup4',
      'html5lib'
    ]
)
