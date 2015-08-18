from setuptools import setup, find_packages

version = '0.0.1'
packages = find_packages(exclude=['test*', 'htmlcov'])

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
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    test_suite='test_pbk2_hasher',

    classifiers=[
        'Programming Language :: Python :: 3.4',
    ]
)
