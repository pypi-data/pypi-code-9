from setuptools import find_packages, setup

setup(
    name='baluhn-redux',
    version='0.2',
    license='Public Domain',
    description='A base-agnostic implementation of the Luhn Algorithm for '
        'Python. Useful for generating and verifying check digits.',
    packages=find_packages(),
    include_package_data=True,
    py_modules=['baluhn'],
    obsoletes=['baluhn'],
    url='http://github.com/obsidiancard/baluhn',
    author='Ben Hodgson',
    author_email='ben@benhodgson.com',
    maintainer='Joey Wilhelm',
    maintainer_email='jwilhelm@opay.io',
    keywords = ['luhn', 'mod10', 'check digit', 'luhn mod N'],
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
