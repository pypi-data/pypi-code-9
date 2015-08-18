from setuptools import setup

version = '0.0.2'

desc = '''
A pbk2 hasher implementation that is compatible with django's auth.hashers.
'''


setup(
    name='pbk2_hasher',
    version=version,
    description=desc,
    url='http://github.com/bcho/pbk2_hasher',
    author='hbc',
    author_email='bcxxxxxx@gmail.com',
    license='MIT',
    py_modules=['pbk2_hasher'],
    zip_safe=False,
    include_package_data=True,
    test_suite='test_pbk2_hasher',

    classifiers=[
        'Programming Language :: Python :: 3.4',
    ]
)
