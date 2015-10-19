from setuptools import setup, Extension

setup(
    name='gc-ua-parser',
    version='1.0.2',
    author='Travis Thieman',
    author_email='travis@gc.io',
    packages=['ua_parser'],
    package_dir={'': '.'},
    zip_safe=False,
    url='https://github.com/gamechanger/uap-python',
    ext_modules = [Extension("ua_parser/user_agent_parser", ["ua_parser/user_agent_parser.c"])]
)
