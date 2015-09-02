import os
from setuptools import setup, find_packages

version = '0.1.10'

description = "Docker Utils with Python"
cur_dir = os.path.dirname(__file__)
try:
    long_description = open(os.path.join(cur_dir, 'README.rst')).read()
except:
    long_description = description

try:
    import pypandoc
    long_description = lambda f: pypandoc.convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    long_description = lambda f: open(f, 'r').read()

setup(
    name = "pyocker",
    version = version,
    url = 'https://github.com/AkihikoITOH/docker_tools/tree/master/pyocker',
    license = 'MIT',
    description = description,
    long_description = long_description('README.md'),
    author = 'ITOH Akihiko',
    # author_email = 'jhmsmits@gmail.com',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    scripts = ['src/pyocker/pyocker_modules/build.py','src/pyocker/pyocker_modules/parse.py','src/pyocker/pyocker_modules/push.py','src/pyocker/pyocker_modules/validate.py'],
    # package_data={ 'src': ['*.py']},
    install_requires = ['setuptools', 'pypandoc'],
    entry_points="""
    [console_scripts]
    pyocker = pyocker.pyocker:main
    """,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        # 'License :: OSI Approved :: BSD License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        # 'Topic :: Software Development :: Bug Tracking',
    ],
    # test_suite = 'nose.collector',
)
