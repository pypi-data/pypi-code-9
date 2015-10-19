from setuptools import setup
from Cython.Build import cythonize

setup(
    name='gc-ua-parser',
    version='1.0.0',
    packages=['ua_parser'],
    package_dir={'': '.'},
    zip_safe=False,
    url='https://github.com/gamechanger/uap-python',
    ext_modules = cythonize("ua_parser/user_agent_parser.pyx")
)
