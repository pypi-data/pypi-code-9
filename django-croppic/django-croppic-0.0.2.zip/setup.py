from setuptools import setup

long_description = (open('README.md').read() + '\n\n' +
                    open('CHANGES.rst').read() + '\n\n' +
                    open('TODO.rst').read())


def _static_files(prefix):
    return [prefix+'/'+pattern for pattern in [
        'croppic/*.*',
        'croppic/*/*.*',
    ]]

setup(
    name='django-croppic',
    version='0.0.2',
    description='A Django package which uses Croppic.net to upload and crop images.',
    author='Aamir Adnan',
    author_email='s33k.n.d3str0y@gmail.com',
    url='https://github.com/intellisense/django-croppic',
    license='MIT',
    packages=['croppic', ],
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Programming Language :: Python :: 2.7',
    ],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'django>=1.4.2',
        'pillow',
    ],
    package_data={'croppic': _static_files('static')}
)
