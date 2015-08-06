from setuptools import setup

with open('postcodeinfo.py', 'r') as f:
    version = reduce(
        lambda a, l: l.startswith('__version__') and l[15:-2] or a, f, '')

with open('README.rst', 'r') as f:
    readme = f.read()

setup(
    name='postcodeinfo',
    version=version,
    py_modules=['postcodeinfo'],
    description=(
        'API client for https://github.com/ministryofjustice/postcodeinfo'),
    long_description=readme,
    author='MOJ Digital Services',
    author_email='andy.driver@digital.justice.gov.uk',
    maintainer='Andy Driver',
    maintainer_email='andy.driver@digital.justice.gov.uk',
    keywords=['python', 'ministryofjustice', 'govuk'],
    platforms=['any'],
    url='https://github.com/ministryofjustice/postcodeinfo-client-python',
    license='LICENSE',
    install_requires=['requests>=2.7,<3'],
    test_suite="tests",
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'])
