from setuptools import setup

setup(name='weebly',
    version='0.2',
    description='Python functions to interface with Weebly Cloud Api',
    url='http://github.com/tkwon/weebly',
    author='T Kwon',
    author_email='tdkwon@gmail.com',
    license='MIT',
    packages=['weebly'],
    install_requires=[
        'requests',
    ],
    zip_safe=False)